---
title: 探索基于pion开发的WebRTC应用的建连过程
url: https://tonybai.com/2024/12/26/exploring-the-connection-establish-process-of-webrtc-app-built-with-pion/
published: '2024-12-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探索基于pion开发的WebRTC应用的建连过程

![](../../assets/90b8cece83632964.png)


[本文永久链接](https://tonybai.com/2024/12/26/exploring-the-connection-establish-process-of-webrtc-app-built-with-pion) – https://tonybai.com/2024/12/26/exploring-the-connection-establish-process-of-webrtc-app-built-with-pion

在《[WebRTC第一课：从信令、ICE到NAT穿透的连接建立全流程](https://tonybai.com/2024/12/14/webrtc-first-lesson-how-connection-estabish/)》一文中，我们从理论层面全面细致地了解了WebRTC连接建立的完整流程。这个流程大致可以分为以下几个阶段：

- 与信令服务器的交互
- ICE候选项的采集、交换与排序
- 形成ICE候选检查表、进行连通性检查，并最终确定最优候选路径

这个过程的复杂性不言而喻。即便多次阅读全文，读者可能仍难以形成深入的理解。因此，如果能够配上一个真实的示例，相信会更有助于读者全面把握这一过程的细节和原理。

在这篇文章中，我就为大家呈现一个真实的示例，我将使用Go语言开源WebRTC项目[pion/webrtc](https://github.com/pion/webrtc)来实现一个基于datachannel的WebRTC演示版程序，通过将pion/webrtc的日志级别设置为TRACE级，输出更多pion/webrtc实现层面的日志，以帮助大家理解WebRTC建连过程。同时，我还会实现一个简易版的基于“Room抽象模型”的信令服务器，供WebRTC通信两端交换信息使用。希望该示例能帮助大家更好的理解WebRTC端到端的建连流程。

按照WebRTC建连的流程，我们先来实现一个简易版的信令服务器。

注：提醒各位读者，本文中所有例子均以演示和帮助大家理解为目的，不建议在生产中使用示例中的代码。


## 1. 信令服务器(signaling-server)

下面是一个基于WebSocket的WebRTC信令服务器的简化实现，使用WebSocket进行WebRTC信令交换可以提供更快速、更高效和更灵活的通信体验，同时WebSocket生态丰富，可复用的代码库有很多，实现起来也比较简单。

这个信令服务器是基于Room抽象模型的，因此其主要结构是一个Room结构体，代表一个聊天室。我们具体看一下该信令服务器的实现代码：

```
// webrtc-first-lesson/part2/signaling-server/main.go
package main
import (
"encoding/json"
"fmt"
"log"
"net/http"
"sync"
"github.com/gorilla/websocket"
)
type Room struct {
Clients map[*websocket.Conn]bool
mu sync.Mutex
}
var (
upgrader = websocket.Upgrader{
CheckOrigin: func(r *http.Request) bool {
return true
},
}
rooms = make(map[string]*Room)
roomMu sync.Mutex
)
func main() {
http.HandleFunc("/ws", handleWebSocket)
log.Println("Signaling server starting on :28080")
log.Fatal(http.ListenAndServe(":28080", nil))
}
func handleWebSocket(w http.ResponseWriter, r *http.Request) {
conn, err := upgrader.Upgrade(w, r, nil)
if err != nil {
log.Println("Error upgrading to WebSocket:", err)
return
}
defer conn.Close()
remoteAddr := conn.RemoteAddr().String()
log.Println("New WebSocket connection from:", remoteAddr)
roomID := r.URL.Query().Get("room")
if roomID == "" {
roomID = fmt.Sprintf("room_%d", len(rooms)+1)
log.Printf("Created new room: %s\n", roomID)
}
roomMu.Lock()
room, exists := rooms[roomID]
if !exists {
room = &Room{Clients: make(map[*websocket.Conn]bool)}
rooms[roomID] = room
}
roomMu.Unlock()
room.mu.Lock()
room.Clients[conn] = true
room.mu.Unlock()
log.Printf("Client[%v] joined room %s\n", remoteAddr, roomID)
for {
messageType, message, err := conn.ReadMessage()
if err != nil {
log.Println("Error reading message:", err)
break
}
var msg map[string]interface{}
if err := json.Unmarshal(message, &msg); err != nil {
log.Println("Error unmarshaling message:", err)
continue
}
msg["roomId"] = roomID
updatedMessage, _ := json.Marshal(msg)
room.mu.Lock()
for client := range room.Clients {
if client != conn {
clientAddr := client.RemoteAddr().String()
if err := client.WriteMessage(messageType, updatedMessage); err != nil {
log.Println("Error writing message:", err)
} else {
log.Printf("writing message to client[%v] ok\n", clientAddr)
}
}
}
room.mu.Unlock()
}
room.mu.Lock()
delete(room.Clients, conn)
room.mu.Unlock()
log.Printf("Client[%v] left room %s\n", remoteAddr, roomID)
}
```


我们看到：Room结构体包含一个WebSocket连接的map和一个互斥锁。演示程序使用全局变量rooms（房间map）和相应的互斥锁管理房间和加入房间的连接，并在房间内进行消息广播，以保证消息能转发到参与通信的所有端(Peer)。当然，如果仅有两端在一个房间中，那么这就变成了一对一的实时通信。

这个信令服务器程序启动后，默认监听28080端口，当客户端连接时，会根据URL参数来将客户端连接加入到某个房间，如果房间号参数为空，则代表该客户端期望创建一个房间。先创建房间并加入的客户端作为answer端，等待offer端的连接。当从某个客户端连接收到消息后，会广播给房间内的其他客户端。当客户端断开连接时，便将其从房间中移除。

当然这仅是一个演示版程序，并未对历史建立的房间进行回收，同时也没有进行身份认证等安全方面的控制。

接下来，我们再来看看借助信令服务器进行端到端实时通信的端侧WebRTC应用的实现。

## 2. 端侧WebRTC应用(webrtc-peer)

WebRTC应用的代码通常都很“样板化”。在开发WebRTC应用程序时，信令连接、设置本地和远程描述、收集ICE候选以及转发信令消息等步骤都是一些常见且重复性较高的任务。这些步骤在不同的WebRTC应用程序中通常都大同小异。以下是这些重复性任务的一些具体步骤示例：

1) 信令连接处理

– 创建信令通道(如WebSocket连接)

– 监听连接建立、断开等事件

– 通过信令通道交换offer/answer等信令消息

2) 本地和远程描述设置

– 创建c实例

– 设置本地描述(createOffer/createAnswer)

– 设置远程描述(setRemoteDescription)

3) ICE 候选收集与交换

– 监听ICE候选事件，收集本地ICE候选

– 通过信令通道交换ICE候选信息

– 将远程ICE候选添加到RTCPeerConnection实例

4) 信令消息转发

– 接收来自远程的信令消息

– 根据消息类型，转发给本地RTCPeerConnection实例

这些基本步骤在大多数WebRTC应用程序中都是必需的。我们的示例代码也不例外，下面就是webrtc-peer程序源码，有些长，也很繁琐：

```
// webrtc-first-lesson/part2/webrtc-peer/main.go
package main
import (
"encoding/json"
"flag"
"fmt"
"log"
"time"
"github.com/gorilla/websocket"
"github.com/pion/logging"
"github.com/pion/webrtc/v3"
)
type signalMsg struct {
Type string `json:"type"`
Data string `json:"data"`
}
var (
signalingServer string
roomID string
)
func init() {
flag.StringVar(&signalingServer, "server", "ws://localhost:28080/ws", "Signaling server WebSocket URL")
flag.StringVar(&roomID, "room", "", "Room ID (leave empty to create a new room)")
flag.Parse()
}
func main() {
// Connect to signaling server
signalingURL := fmt.Sprintf("%s?room=%s", signalingServer, roomID)
conn, _, err := websocket.DefaultDialer.Dial(signalingURL, nil)
if err != nil {
log.Fatal("Error connecting to signaling server:", err)
}
defer conn.Close()
log.Println("connect to signaling server ok")
// Create a new RTCPeerConnection
config := webrtc.Configuration{
ICEServers: []webrtc.ICEServer{
{
URLs: []string{"stun:stun.l.google.com:19302"},
},
},
}
// 创建一个自定义的日志工厂
loggerFactory := logging.NewDefaultLoggerFactory()
loggerFactory.DefaultLogLevel = logging.LogLevelTrace
//loggerFactory.DefaultLogLevel = logging.LogLevelInfo
//loggerFactory.DefaultLogLevel = logging.LogLevelDebug
// Enable detailed logging
s := webrtc.SettingEngine{}
s.LoggerFactory = loggerFactory
s.SetICETimeouts(5*time.Second, 5*time.Second, 5*time.Second)
api := webrtc.NewAPI(webrtc.WithSettingEngine(s))
peerConnection, err := api.NewPeerConnection(config)
if err != nil {
log.Fatal(err)
}
// Create a datachannel
dataChannel, err := peerConnection.CreateDataChannel("test", nil)
if err != nil {
log.Fatal(err)
}
dataChannel.OnOpen(func() {
log.Println("Data channel is open")
go func() {
for {
err := dataChannel.SendText("Hello from " + roomID)
if err != nil {
log.Println(err)
}
time.Sleep(5 * time.Second)
}
}()
})
dataChannel.OnMessage(func(msg webrtc.DataChannelMessage) {
log.Printf("Received message: %s\n", string(msg.Data))
})
// Set the handler for ICE connection state
peerConnection.OnICEConnectionStateChange(func(connectionState webrtc.ICEConnectionState) {
log.Printf("ICE Connection State has changed: %s\n", connectionState.String())
})
// Set the handler for Peer connection state
peerConnection.OnConnectionStateChange(func(s webrtc.PeerConnectionState) {
log.Printf("Peer Connection State has changed: %s\n", s.String())
})
// Set the handler for Signaling state
peerConnection.OnSignalingStateChange(func(s webrtc.SignalingState) {
log.Printf("Signaling State has changed: %s\n", s.String())
})
// Register data channel creation handling
peerConnection.OnDataChannel(func(d *webrtc.DataChannel) {
log.Printf("New DataChannel %s %d\n", d.Label(), d.ID())
d.OnOpen(func() {
log.Printf("Data channel '%s'-'%d' open.\n", d.Label(), d.ID())
})
d.OnMessage(func(msg webrtc.DataChannelMessage) {
log.Printf("Message from DataChannel '%s': '%s'\n", d.Label(), string(msg.Data))
})
})
// Set the handler for ICE candidate generation
peerConnection.OnICECandidate(func(i *webrtc.ICECandidate) {
if i == nil {
return
}
candidateString, err := json.Marshal(i.ToJSON())
if err != nil {
log.Println(err)
return
}
if writeErr := conn.WriteJSON(&signalMsg{
Type: "candidate",
Data: string(candidateString),
}); writeErr != nil {
log.Println(writeErr)
}
})
// Handle incoming messages from signaling server
go func() {
for {
_, rawMsg, err := conn.ReadMessage()
if err != nil {
log.Println("Error reading message:", err)
return
}
log.Println("recv msg from signaling server")
var msg signalMsg
if err := json.Unmarshal(rawMsg, &msg); err != nil {
log.Println("Error parsing message:", err)
continue
}
log.Println("recv msg is", msg)
switch msg.Type {
case "offer":
log.Println("recv a offer msg")
offer := webrtc.SessionDescription{}
if err := json.Unmarshal([]byte(msg.Data), &offer); err != nil {
log.Println("Error parsing offer:", err)
continue
}
if err := peerConnection.SetRemoteDescription(offer); err != nil {
log.Println("Error setting remote description:", err)
continue
}
answer, err := peerConnection.CreateAnswer(nil)
if err != nil {
log.Println("Error creating answer:", err)
continue
}
if err := peerConnection.SetLocalDescription(answer); err != nil {
log.Println("Error setting local description:", err)
continue
}
answerString, err := json.Marshal(answer)
if err != nil {
log.Println("Error encoding answer:", err)
continue
}
if err := conn.WriteJSON(&signalMsg{
Type: "answer",
Data: string(answerString),
}); err != nil {
log.Println("Error sending answer:", err)
}
log.Println("send answer ok")
case "answer":
log.Println("recv a answer msg")
answer := webrtc.SessionDescription{}
if err := json.Unmarshal([]byte(msg.Data), &answer); err != nil {
log.Println("Error parsing answer:", err)
continue
}
if err := peerConnection.SetRemoteDescription(answer); err != nil {
log.Println("Error setting remote description:", err)
}
log.Println("set remote desc for answer ok")
case "candidate":
candidate := webrtc.ICECandidateInit{}
if err := json.Unmarshal([]byte(msg.Data), &candidate); err != nil {
log.Println("Error parsing candidate:", err)
continue
}
if err := peerConnection.AddICECandidate(candidate); err != nil {
log.Println("Error adding ICE candidate:", err)
}
log.Println("adding ICE candidate:", candidate)
}
}
}()
// Create an offer if we are the peer to join the room
if roomID != "" {
offer, err := peerConnection.CreateOffer(nil)
if err != nil {
log.Fatal(err)
}
if err := peerConnection.SetLocalDescription(offer); err != nil {
log.Fatal(err)
}
offerString, err := json.Marshal(offer)
if err != nil {
log.Fatal(err)
}
if err := conn.WriteJSON(&signalMsg{
Type: "offer",
Data: string(offerString),
}); err != nil {
log.Fatal(err)
}
log.Printf("send offer to signaling server ok\n")
}
// Wait forever
select {}
}
```


通过代码，我们看到：这个使用Go实现的WebRTC对等连接示例程序通过WebSocket与信令服务器通信，创建和管理RTCPeerConnection，处理ICE候选、offer和answer，并实现了数据通道功能。程序支持创建新房间或加入现有房间，展示了完整的WebRTC连接建立流程，包括信令交换和ICE处理。它通过对pion/webrtc的日志级别设置让其具有详细的日志记录能力，这为我们后续通过日志分别WebRTC建连各个阶段奠定了基础。

## 3. 建立连接流程的日志分析

下面是实验环境的拓扑图：

![](../../assets/54f1b07691040d7b.png)


webrtc-peer分别位于两台服务器上，其中Host A是一台位于NAT后面的内网主机，而HOST B则是一台位于美国的公网主机，信令服务器搭建在HOST B上，stun服务器使用的是Google提供的公网免费stun server。

下面是信令服务器和两端peer服务器的编译和启动步骤：

我们先启动信令服务器：

```
//在Host B上signaling-server目录下
$make
$./signaling-server
2024/08/20 21:45:50 Signaling server starting on :28080
```


接下来，启动Host A上的webrtc-peer程序：

```
//在Host A上webrtc-peer目录下
$make
$./webrtc-peer -server ws://206.189.166.16:28080/ws
```


这时信令服务器就会发现有新的websocket连入，并创建了room_6(这只是多次运行中的某一次的room id罢了)：

```
2024/08/20 21:48:52 New WebSocket connection from: 47.93.3.95:17355
2024/08/20 21:48:52 Created new room: room_6
2024/08/20 21:48:52 Client[47.93.3.95:17355] joined room room_6
```


然后我们启动Host B上的webrtc-peer程序，将这一端加入到上面创建的room_6中：

```
//在Host B上webrtc-peer目录下
$make
$./webrtc-peer -room room_6 -server ws://206.189.166.16:28080/ws
```


这之后，信令服务器也会发现Host B上的webrtc-peer的连接。之后便开始从信令交互开始逐步实现端到端的建连。以下是对各个阶段产生的详细日志的分析：

### 3.1 信令服务连接（房间加入）和SDP 交互

- 信令连接

```
"2024/08/20 21:45:48 connect to signaling server ok"
```


以上日志表示成功连接到信令服务器。如果房间号为空，则该peer(answer)先启动并在信令服务器建立房间，然后另一个peer(offer)加入该房间，通过信令服务器交换信息。

- SDP交互

下面日志则是表示接收到另一个peer的offer SDP：

```
"2024/08/20 21:45:55 recv msg is {offer {"type":"offer","sdp":"v=0\r\no=- 2149168073199454578 1724143555 IN IP4 0.0.0.0\r\ns=-\r\nt=0 0\r\na=msid-semantic:WMS*\r\na=fingerprint:sha-256 A6:D6:AE:F3:30:0D:D8:07:D2:23:C9:A5:69:27:F2:CC:B1:8C:A4:DB:30:79:E7:62:9B:09:87:B7:68:1F:55:A7\r\na=extmap-allow-mixed\r\na=group:BUNDLE 0\r\nm=application 9 UDP/DTLS/SCTP webrtc-datachannel\r\nc=IN IP4 0.0.0.0\r\na=setup:actpass\r\na=mid:0\r\na=sendrecv\r\na=sctp-port:5000\r\na=ice-ufrag:TYfjBFmqpgGEtKbh\r\na=ice-pwd:NGdAyXsOgVwFfzXnlLmNrcWrBgJWFceB\r\n"}}
```


其中”recv a offer msg”表示程序识别到收到了offer消息。而”offer := webrtc.SessionDescription{}”及后续代码则是处理offer，创建answer并发送回给另一个peer。

在WebRTC中，信令服务器用于交换SDP（Session Description Protocol）信息，SDP描述了连接的媒体信息，如编解码器、IP 地址、端口等。先启动的peer创建房间，等待offer，后加入的peer发送offer后，等待answer的回复，双方通过信令服务器交换这些信息以建立连接。

接下来，便是两端的ICE流程。

### 3.2 ice Candidate Gathering、Candidate Priorization以及candidate的排序列表

下面一行日志表示开始收集ICE 候选者，这里是一个host类型的候选者：

```
"2024/08/20 21:45:55 adding ICE candidate: {candidate:3384150427 1 udp 2130706431 206.189.166.16 52256 typ host 0xc000210230 0xc0002121fe <nil>}"
```


后续有多个类似的日志，分别添加不同类型的候选者，如 host、srflx（Server Reflexive）等：

```
2024/08/20 21:45:55 adding ICE candidate: {candidate:604015337 1 udp 2130706431 10.46.0.5 38367 typ host 0xc000210260 0xc000212250 <nil>}
2024/08/20 21:45:55 adding ICE candidate: {candidate:3019421960 1 udp 2130706431 2604:a880:2:d0::2094:3001 48394 typ host 0xc000210290 0xc000212298 <nil>}
2024/08/20 21:45:55 adding ICE candidate: {candidate:2090009598 1 udp 2130706431 10.0.0.1 58895 typ host 0xc0002102d0 0xc0002122e0 <nil>}
2024/08/20 21:45:55 adding ICE candidate: {candidate:233762139 1 udp 2130706431 172.17.0.1 58343 typ host 0xc000210300 0xc000212328 <nil>}
2024/08/20 21:45:55 adding ICE candidate: {candidate:2943811937 1 udp 1694498815 2604:a880:2:d0::2094:3001 40480 typ srflx raddr :: rport 40480 0xc00038c070 0xc00038e050 <nil>}
2024/08/20 21:45:55 adding ICE candidate: {candidate:2614874796 1 udp 1694498815 206.189.166.16 38534 typ srflx raddr 0.0.0.0 rport 38534 0xc000210760 0xc000212b98 <nil>}
```


不过，在输出的日志中，我们看到并没有明确输出我们期待的经过 Candidate Priorization（候选者优先级排序）后的候选者排序列表。

注：重温一下ICE（Interactive Connectivity Establishment），这是一种用于在两个peer之间建立连接的协议，通过收集各种类型的候选者（如 host 表示本机地址、srflx 表示通过 NAT 反射得到的地址等），增加连接成功的可能性。


### 3.3 ice connectivity check的各个子阶段

- 子阶段1：输出每一端的角色

在ICE连接中，会确定一个controlling方和一个controlled方，用于决定连接的发起和响应顺序。 下面这行输出日志表示本端不是controlling方：

```
"ice DEBUG: 21:45:55.401065 agent.go:395: Started agent: isControlling? false, remoteUfrag: "TYfjBFmqpgGEtKbh", remotePwd: "NGdAyXsOgVwFfzXnlLmNrcWrBgJWFceB"
```


- 子阶段2：每端输出形成的检查列表(Forming checklist)

这个阶段日志中没有明确输出检查列表，但日志中有大量的“Ping STUN from… to…”表示正在进行连接检查，这些日志汇总在一起可以看成是形成的检查列表。例如：

```
ice TRACE: 21:45:55.401676 agent.go:999: Ping STUN from udp4 host 172.17.0.1:7115 to udp4 host 206.189.166.16:52256。
```


每一端都会通过发送STUN请求来检查不同候选者之间的连接性。

- 子阶段3： 输出针对每个列表项的连接检查结果

日志中有很多类似的日志表示收到了来自特定候选者的成功响应：

```
"ice TRACE: 21:45:55.563530 selection.go:229: Inbound STUN (SuccessResponse) from udp4 host 206.189.166.16:52256 to udp4 host 172.17.0.1:7115"
```


根据连接检查的结果，如果发现Peer Reflexive 候选，也会有相应的日志输出，比如：

```
ice DEBUG: 21:45:25.771665 agent.go:1147: Adding a new peer-reflexive candidate: 192.168.0.124:61194
ice DEBUG: 21:45:25.772355 agent.go:1147: Adding a new peer-reflexive candidate: 192.168.0.124:26408
ice DEBUG: 21:45:25.775320 agent.go:1147: Adding a new peer-reflexive candidate: 192.168.0.124:40491
ice DEBUG: 21:45:25.776894 agent.go:1147: Adding a new peer-reflexive candidate: 192.168.0.124:5767
ice DEBUG: 21:45:25.777018 agent.go:1147: Adding a new peer-reflexive candidate: 192.168.0.124:61432
... ...
```


### 3.4 NAT穿透尝试并输出最终的最佳候选者对

日志中大量的”Ping STUN”和”Inbound STUN (SuccessResponse)”表示正在进行 NAT 穿透尝试。例如：

```
ice TRACE: 21:45:55.401676 agent.go:999: Ping STUN from udp4 host 172.17.0.1:7115 to udp4 host 206.189.166.16:52256
ice TRACE: 21:45:55.563530 selection.go:229: Inbound STUN (SuccessResponse) from udp4 host 206.189.166.16:52256 to udp4 host 172.17.0.1:7115
```


通过STUN请求和响应来确定是否能够穿透NAT，如果穿透失败，则将其标记为failed：

```
ice TRACE: 21:45:56.274839 agent.go:550: Maximum requests reached for pair prio 9151314440652587007 (local, prio 2130706431) udp4 host 172.18.0.1:59520 <-> udp4 host 10.0.0.1:58895 (remote, prio 2130706431), state: in-progress, nominated: false, nominateOnBindingSuccess: false, marking it as failed
```


如果能够成功穿透，则可以建立连接。下面的日志表示选出了最终的最佳候选者对：

```
ice TRACE: 21:45:56.656900 agent.go:524: Set selected candidate pair: prio 9151314440652587007 (local, prio 2130706431) udp4 host 192.168.10.1:60662 <-> udp4 host 206.189.166.16:52256 (remote, prio 2130706431), state: succeeded, nominated: true, nominateOnBindingSuccess: false
ice TRACE: 21:45:56.823017 selection.go:239: Found valid candidate pair: prio 9151314440652587007 (local, prio 2130706431) udp4 host 192.168.10.1:60662 <-> udp4 host 206.189.166.16:52256 (remote, prio 2130706431), state: succeeded, nominated: true, nominateOnBindingSuccess: false
```


一旦确定了最佳候选者对，连接就算建立成功了！

接下来，就是打开datachannel通道并进行数据传输了！

### 3.5 data channel打开以及定时(5秒一次)的数据传输

下面日志表示数据通道已打开：

```
"Data channel is open"
```


下面日志表示创建了一个名为“test”的数据通道：

```
"New DataChannel test 824638605290"
```


下面日志表示数据通道打开成功：

```
"Data channel 'test'-'824638605290' open"
```


示例代码中，启动一个goroutine用于定时向data channel发送数据，当出现下面日志时，表示接收到来自另一个 peer 的数据：

```
"Message from DataChannel 'test': 'Hello from room_6'"
```


## 4. 小结

在这篇文章中，我通过使用Go语言开源项目pion/webrtc实现的webrtc端侧应用，为大家详细展示了WebRTC应用的建连过程。

首先，我实现了一个基于WebSocket的简易信令服务器。这个信令服务器基于Room抽象模型，使用全局变量来管理房间和连接，并进行消息广播。

接下来，我介绍了端侧WebRTC应用的实现。这个应用通过与信令服务器通信，创建RTCPeerConnection，处理ICE候选、offer和answer，以及实现数据通道功能。我还通过设置TRACE日志级别，展示了详细的建连流程。

之后，我在实验环境的实际执行了上述程序，并通过对日志的分析展示了建连过程。这些分析涵盖了信令服务连接和SDP交互、ICE候选收集与优先级排序、ICE 连通性检查各子阶段、NAT穿透尝试及最佳候选者对确定，以及数据通道打开和数据传输。希望这样的分析可以帮助大家更深刻的理解和体会建连过程。

WebRTC网络结构和建连就先讲到这里，后面的系列文章中，我们会开始聚焦WebRTC技术栈的另外一个主要方面：音视频质量，包括编码器以及媒体流处理等。

本文涉及的Go源码在[这里](https://github.com/bigwhite/experiments/blob/master/webrtc-first-lesson/part2)可以下载到 – https://github.com/bigwhite/experiments/blob/master/webrtc-first-lesson/part2

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

可以教写一个基于webrtc的p2p下载库吗

p2p下载用webrtc?

不是BT那种大范围的，小范围或内部用，主要用到webrtc的打洞标准。

那实际上就是通过webrtc建立p2p的datachannel连接后，在data channel上传文件数据呗。如果还要对文件传输的状态进行管理的话，可能需要在datachannel之上设计一个简单的文件传输协议。不知道有没有现成的类似于ftp over webrtc datachannel的实现。

差不多这个意思。

如同一个http下载链接，既可以用http源下载，又可以通过webrtc建立p2p的datachannel连接跟同时在下载的人分享已下载的数据。

白哥能讲一下如何学习pion/webrtc吗，网上的相关教程比较少，只找到api doc

如果是做webrtc应用层开发，就看自己使用的语言（比如go、c++等）对应的webrtc框架如何使用。

如果要下沉到webrtc原理，那就需要结合着webrtc的spec看具体的webrtc实现（最初的实现是c++的）了。webrtc不是一种技术，而是一系列成熟技术的组合。spec有在RFC站点的，也要其他的（比如mozilla官网上的）。

如果还要学习媒体编解码，ffmpeg相关书籍和资料是不错的参考。