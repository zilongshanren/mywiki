---
title: 如何在Go语言中使用Websockets：最佳工具与行动指南
url: https://tonybai.com/2019/09/28/how-to-build-websockets-in-go/
published: '2019-09-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 如何在Go语言中使用Websockets：最佳工具与行动指南

如今，在不刷新页面的情况下发送消息并获得即时响应在我们看来是理所当然的事情。但是曾几何时，启用实时功能对开发人员来说是一个真正的挑战。开发社区在HTTP长轮询(http long polling)和[AJAX](https://en.wikipedia.org/wiki/Ajax_%28programming%29)上走了很长一段路，但终于还是找到了一种构建真正的实时应用程序的解决方案。

该解决方案以[WebSockets](https://en.wikipedia.org/wiki/WebSocket)的形式出现，这使得在用户浏览器和服务器之间开启一个交互式会话成为可能。WebSocket支持浏览器将消息发送到服务器并接收事件驱动的响应，而不必使用长轮询服务器的方式去获取响应。

就目前而言，WebSockets是构建实时应用程序的首选解决方案，包括在线游戏，即时通讯程序，跟踪应用程序等均在使用这一方案。本文将说明WebSockets的操作方式，并说明我们如何使用[Go语言](https://tonybai.com/tag/go)构建WebSocket应用程序。我们还将比较最受欢迎的WebSocket库，以便您可以根据选择出最适合您的那个。

## 网络套接字(network socket)与WebSocket

在Go中使用WebSockets之前，让我们在网络套接字和WebSockets之间划清一条界限。

### 网络套接字

网络套接字（或简称为套接字）充当内部端点，用于在同一计算机或同一网络上的不同计算机上运行的应用程序之间交换数据。

套接字是Unix和Windows操作系统的关键部分，它们使开发人员更容易创建支持网络的软件。应用程序开发人员不可以直接在程序中包含套接字，而不是从头开始构建网络连接。由于网络套接字可用于许多不同的网络协议（如[HTTP](https://tonybai.com/2015/04/30/go-and-https/)，FTP等），因此可以同时使用多个套接字。

套接字是通过一组函数调用创建和使用的，这些函数调用有时称为套接字的应用程序编程接口（API）。正是由于这些函数调用，套接字可以像常规文件一样被打开。

网络套接字有如下几种类型：

-
数据报套接字（SOCK_DGRAM），也称为无连接套接字，使用用户数据报协议（UDP）。数据报套接字支持双向消息流并保留记录边界。

-
流套接字（SOCK_STREAM），也称为面向连接的套接字，使用传输控制协议（TCP），流控制传输协议（SCTP）或数据报拥塞控制协议（DCCP）。这些套接字提供了没有记录边界的双向，可靠，有序且无重复的数据流。

-
原始套接字（或原始IP套接字）通常在路由器和其他网络设备中可用。这些套接字通常是面向数据报的，尽管它们的确切特性取决于协议提供的接口。大多数应用程序不使用原始套接字。提供它们是为了支持新的通信协议的开发，并提供对现有协议更深层设施的访问。


#### 套接字通信

首先，让我们弄清楚如何确保每个套接字都是唯一的。否则，您将无法建立可靠的沟通通道(channel)。

为每个进程(process)提供唯一的PID有助于解决本地问题。但是，这种方法不适用于网络。要创建唯一的套接字，我们建议使用TCP / IP协议。使用TCP / IP，网络层的IP地址在给定网络内是唯一的，并且协议和端口在主机应用程序之间是唯一的。

TCP和UDP是用于主机之间通信的两个主要协议。让我们看看您的应用程序如何连接到TCP和UDP套接字。

- 连接到TCP套接字

为了建立TCP连接，Go客户端使用net程序包中的DialTCP函数。DialTCP返回一个TCPConn对象。建立连接后，客户端和服务器开始交换数据：客户端通过TCPConn向服务器发送请求，服务器解析请求并发送响应，TCPConn从服务器接收响应。

![img{512x368}](../../assets/db1cb3ba9e12ba53.png)


图:TCP Socket

该连接将持续保持有效，直到客户端或服务器将其关闭。创建连接的函数如下：

客户端：

```
// init
tcpAddr, err := net.ResolveTCPAddr(resolver, serverAddr)
if err != nil {
// handle error
}
conn, err := net.DialTCP(network, nil, tcpAddr)
if err != nil {
// handle error
}
// send message
_, err = conn.Write({message})
if err != nil {
// handle error
}
// receive message
var buf [{buffSize}]byte
_, err := conn.Read(buf[0:])
if err != nil {
// handle error
}
```


服务端：

```
// init
tcpAddr, err := net.ResolveTCPAddr(resolver, serverAddr)
if err != nil {
// handle error
}
listener, err := net.ListenTCP("tcp", tcpAddr)
if err != nil {
// handle error
}
// listen for an incoming connection
conn, err := listener.Accept()
if err != nil {
// handle error
}
// send message
if _, err := conn.Write({message}); err != nil {
// handle error
}
// receive message
buf := make([]byte, 512)
n, err := conn.Read(buf[0:])
if err != nil {
// handle error
}
```


- 连接到UDP套接字

与TCP套接字相反，使用UDP套接字，客户端只是向服务器发送数据报。没有Accept函数，因为服务器不需要接受连接，而只是等待数据报到达。

![img{512x368}](../../assets/f3fcf34b7b45d624.png)


图:UDP Socket

其他TCP函数都具有UDP对应的函数；只需在上述函数中将TCP替换为UDP。

客户端：

```
// init
raddr, err := net.ResolveUDPAddr("udp", address)
if err != nil {
// handle error
}
conn, err := net.DialUDP("udp", nil, raddr)
if err != nil {
// handle error
}
.......
// send message
buffer := make([]byte, maxBufferSize)
n, addr, err := conn.ReadFrom(buffer)
if err != nil {
// handle error
}
.......
// receive message
buffer := make([]byte, maxBufferSize)
n, err = conn.WriteTo(buffer[:n], addr)
if err != nil {
// handle error
}
```


服务端：

```
// init
udpAddr, err := net.ResolveUDPAddr(resolver, serverAddr)
if err != nil {
// handle error
}
conn, err := net.ListenUDP("udp", udpAddr)
if err != nil {
// handle error
}
.......
// send message
buffer := make([]byte, maxBufferSize)
n, addr, err := conn.ReadFromUDP(buffer)
if err != nil {
// handle error
}
.......
// receive message
buffer := make([]byte, maxBufferSize)
n, err = conn.WriteToUDP(buffer[:n], addr)
if err != nil {
// handle error
}
```


### 什么是WebSocket

WebSocket通信协议通过单个TCP连接提供全双工通信通道。与HTTP相比，WebSocket不需要您发送请求即可获得响应。它们允许双向数据流，因此您只需等待服务器响应即可。可用时，它将向您发送一条消息。

对于需要连续数据交换的服务（例如即时通讯程序，在线游戏和实时交易系统），WebSockets是一个很好的解决方案。您可以在[RFC 6455规范](https://tools.ietf.org/html/rfc6455)中找到有关WebSocket协议的完整信息。

WebSocket连接由浏览器请求发起，并由服务器响应，之后连接就建立起来了。此过程通常称为[握手](https://en.wikipedia.org/wiki/Handshaking)。WebSockets中的特殊标头仅需要浏览器与服务器之间的一次握手即可建立连接，该连接将在其整个生命周期内保持活动状态。

WebSockets解决了许多实时Web开发的难题，与传统的HTTP相比，它具有许多优点：

- 轻量级报头减少了数据传输开销。
- 单个Web客户端仅需要一个TCP连接。
- WebSocket服务器可以将数据推送到Web客户端。

![img{512x368}](../../assets/33a64dfba2c4efad.png)


图:WebSocket

WebSocket协议实现起来相对简单。它使用HTTP协议进行初始握手。成功握手后，连接就建立起来了，并且WebSocket实质上使用原始TCP(raw tcp)来读取/写入数据。

客户端请求如下所示：

```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
Origin: http://example.com
```


这是服务器响应：

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
Sec-WebSocket-Protocol: chat
```


### 如何在Go中创建WebSocket应用

要基于该net/http 库编写简单的WebSocket echo服务器，您需要：

- 发起握手
- 从客户端接收数据帧
- 发送数据帧给客户端
- 关闭握手

首先，让我们创建一个带有WebSocket端点的HTTP处理程序：

```
// HTTP server with WebSocket endpoint
func Server() {
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
ws, err := NewHandler(w, r)
if err != nil {
// handle error
}
if err = ws.Handshake(); err != nil {
// handle error
}
…
```


然后初始化WebSocket结构。

初始握手请求始终来自客户端。服务器确定了WebSocket请求后，需要使用握手响应进行回复。

请记住，您无法使用http.ResponseWriter编写响应，因为一旦开始发送响应，它将关闭基础TCP连接。

因此，您需要使用HTTP劫持(hijack)。通过劫持，您可以接管基础的TCP连接处理程序和bufio.Writer。这使您可以在不关闭TCP连接的情况下读取和写入数据。

```
// NewHandler initializes a new handler
func NewHandler(w http.ResponseWriter, req *http.Request) (*WS, error) {
hj, ok := w.(http.Hijacker)
if !ok {
// handle error
} .....
}
```


要完成握手，服务器必须使用适当的头进行响应。

```
// Handshake creates a handshake header
func (ws *WS) Handshake() error {
hash := func(key string) string {
h := sha1.New()
h.Write([]byte(key))
h.Write([]byte("258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))
return base64.StdEncoding.EncodeToString(h.Sum(nil))
}(ws.header.Get("Sec-WebSocket-Key"))
.....
}
```


“Sec-WebSocket-key”是随机生成的，并且是Base64编码的。接受请求后，服务器需要将此密钥附加到固定字符串。假设您有x3JJHMbDL1EzLkh9GBhXDw== 钥匙。在这个例子中，可以使用SHA-1计算二进制值，并使用Base64对其进行编码。假设你得到HSmrc0sMlYUkAGmm5OPpG2HaGWk=。使，用它作为Sec-WebSocket-Accept 响应头的值。

#### 传输数据帧

握手成功完成后，您的应用程序可以从客户端读取数据或向客户端写入数据。[WebSocket规范](https://tools.ietf.org/html/rfc6455#section-5.2)定义了的一个客户机和服务器之间使用的特定帧格式。这是框架的位模式：

![img{512x368}](../../assets/c1c0d0a49028217c.png)


图:传输数据帧的位模式

使用以下代码对客户端有效负载进行解码：

```
// Recv receives data and returns a Frame
func (ws *WS) Recv() (frame Frame, _ error) {
frame = Frame{}
head, err := ws.read(2)
if err != nil {
// handle error
}
```


反过来，这些代码行允许对数据进行编码：

```
// Send sends a Frame
func (ws *WS) Send(fr Frame) error {
// make a slice of bytes of length 2
data := make([]byte, 2)
// Save fragmentation & opcode information in the first byte
data[0] = 0x80 | fr.Opcode
if fr.IsFragment {
data[0] &= 0x7F
}
.....
```


#### 关闭握手

当各方之一发送状态为关闭的关闭帧作为有效负载时，握手将关闭。可选地，发送关闭帧的一方可以在有效载荷中发送关闭原因。如果关闭是由客户端发起的，则服务器应发送相应的关闭帧作为响应。

```
// Close sends a close frame and closes the TCP connection
func (ws *Ws) Close() error {
f := Frame{}
f.Opcode = 8
f.Length = 2
f.Payload = make([]byte, 2)
binary.BigEndian.PutUint16(f.Payload, ws.status)
if err := ws.Send(f); err != nil {
return err
}
return ws.conn.Close()
}
```


## WebSocket库列表

有几个第三方库可简化开发人员的开发工作，并极大地促进使用WebSockets。

- STDLIB（golang.org/x/net/websocket）

此WebSocket库是标准库的一部分。如RFC 6455规范中所述，它为WebSocket协议实现了客户端和服务器。它不需要安装并且有很好的[官方文档](https://godoc.org/golang.org/x/net/websocket)。但是，另一方面，它仍然缺少其他WebSocket库中可以找到的某些功能。/x/net/websocket软件包中的Golang WebSocket实现不允许用户以明确的方式重用连接之间的I/O缓冲区。

让我们检查一下STDLIB软件包的工作方式。这是用于执行基本功能（如创建连接以及发送和接收消息）的代码示例。

首先，要安装和使用此库，应将以下代码行添加到您的：

```
import "golang.org/x/net/websocket"
```


客户端：

```
// create connection
// schema can be ws:// or wss://
// host, port – WebSocket server
conn, err := websocket.Dial("{schema}://{host}:{port}", "", op.Origin)
if err != nil {
// handle error
}
defer conn.Close()
.......
// send message
if err = websocket.JSON.Send(conn, {message}); err != nil {
// handle error
}
.......
// receive message
// messageType initializes some type of message
message := messageType{}
if err := websocket.JSON.Receive(conn, &message); err != nil {
// handle error
}
.......
```


服务器端：

```
// Initialize WebSocket handler + server
mux := http.NewServeMux()
mux.Handle("/", websocket.Handler(func(conn *websocket.Conn) {
func() {
for {
// do something, receive, send, etc.
}
}
.......
// receive message
// messageType initializes some type of message
message := messageType{}
if err := websocket.JSON.Receive(conn, &message); err != nil {
// handle error
}
.......
// send message
if err := websocket.JSON.Send(conn, message); err != nil {
// handle error
}
........
```


- GORILLA

[Gorilla Web工具包](https://www.gorillatoolkit.org/pkg/websocket)中的WebSocket软件包拥有WebSocket协议的完整且经过测试的实现以及稳定的软件包API。WebSocket软件包文档齐全，易于使用。您可以在Gorilla官方网站上找到文档。

安装

```
go get github.com/gorilla/websocket
Examples of code
Client side:
// init
// schema – can be ws:// or wss://
// host, port – WebSocket server
u := url.URL{
Scheme: {schema},
Host: {host}:{port},
Path: "/",
}
c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
if err != nil {
// handle error
}
.......
// send message
err := c.WriteMessage(websocket.TextMessage, {message})
if err != nil {
// handle error
}
.......
// receive message
_, message, err := c.ReadMessage()
if err != nil {
// handle error
}
.......
```


服务器端：

```
// init
u := websocket.Upgrader{}
c, err := u.Upgrade(w, r, nil)
if err != nil {
// handle error
}
.......
// receive message
messageType, message, err := c.ReadMessage()
if err != nil {
// handle error
}
.......
// send message
err = c.WriteMessage(messageType, {message})
if err != nil {
// handle error
}
.......
```


- GOBWAS

这个微小的WebSocket封装具有强大的功能列表，例如零拷贝升级(zero-copy upgrade)和允许构建自定义数据包处理逻辑的低级API。GOBWAS在I/O期间不需要中间做额外分配操作。它还在wsutil软件包中提供了围绕API的高级包装API和帮助API，使开发人员可以快速使用，而无需深入研究协议的内部。该库具有灵活的API，但这是以可用性和清晰度为代价的。

可在GoDoc网站上找到[文档](https://godoc.org/github.com/gobwas/ws)。您可以通过下面代码行来安装它：

```
go get github.com/gobwas/ws
```


客户端：

```
// init
// schema – can be ws or wss
// host, port – ws server
conn, _, _, err := ws.DefaultDialer.Dial(ctx, {schema}://{host}:{port})
if err != nil {
// handle error
}
.......
// send message
err = wsutil.WriteClientMessage(conn, ws.OpText, {message})
if err != nil {
// handle error
}
.......
// receive message
msg, _, err := wsutil.ReadServerData(conn)
if err != nil {
// handle error
}
.......
```


服务器端：

```
// init
listener, err := net.Listen("tcp", op.Port)
if err != nil {
// handle error
}
conn, err := listener.Accept()
if err != nil {
// handle error
}
upgrader := ws.Upgrader{}
if _, err = upgrader.Upgrade(conn); err != nil {
// handle error
}
.......
// receive message
for {
reader := wsutil.NewReader(conn, ws.StateServerSide)
_, err := reader.NextFrame()
if err != nil {
// handle error
}
data, err := ioutil.ReadAll(reader)
if err != nil {
// handle error
}
.......
}
.......
// send message
msg := "new server message"
if err := wsutil.WriteServerText(conn, {message}); err != nil {
// handle error
}
.......
```


- GOWebsockets

该工具提供了广泛的易于使用的功能。它允许并发控制，数据压缩和设置请求标头。GoWebsockets支持代理和子协议，用于发送和接收文本和二进制数据。开发人员还可以启用或禁用SSL验证。

您可以在[GoDoc网站](https://godoc.org/github.com/sacOO7/GoWebsocket)和项目的[GitHub页面](https://github.com/sacOO7/gowebsocket/)上找到有关如何使用GOWebsockets的文档和示例。通过添加以下代码行来安装软件包：

```
go get github.com/sacOO7/gowebsocket
```


客户端：

```
// init
// schema – can be ws or wss
// host, port – ws server
socket := gowebsocket.New({schema}://{host}:{port})
socket.Connect()
.......
// send message
socket.SendText({message})
or
socket.SendBinary({message})
.......
// receive message
socket.OnTextMessage = func(message string, socket gowebsocket.Socket) {
// hande received message
};
or
socket.OnBinaryMessage = func(data [] byte, socket gowebsocket.Socket) {
// hande received message
};
.......
```


服务器端：

```
// init
// schema – can be ws or wss
// host, port – ws server
conn, _, _, err := ws.DefaultDialer.Dial(ctx, {schema}://{host}:{port})
if err != nil {
// handle error
}
.......
// send message
err = wsutil.WriteClientMessage(conn, ws.OpText, {message})
if err != nil {
// handle error
}
.......
// receive message
msg, _, err := wsutil.ReadServerData(conn)
if err != nil {
// handle error
}
```


## 比较现有解决方案

我们已经描述了Go中使用最广泛的四个WebSocket库。下表包含这些工具的详细比较。

![img{512x368}](../../assets/7be19f7ab55f4d67.png)


图 Websocket库比较

为了更好地分析其性能，我们还进行了一些基准测试。结果如下：

![img{512x368}](../../assets/ab160003cab55bb3.png)


-
如您所见，GOBWAS与其他库相比具有明显的优势。每个操作分配的内存更少，每个分配使用的内存和时间更少。另外，它的I/O分配为零。此外，GOBWAS还具有创建WebSocket客户端与服务器的交互并接收消息片段所需的所有方法。您也可以使用它轻松地使用TCP套接字。

-
如果您真的不喜欢GOBWAS，则可以使用Gorilla。它非常简单，几乎具有所有相同的功能。您也可以使用STDLIB，但由于它缺少许多必要的功能，并且在生产中表现不佳，而且正如您在基准测试中所看到的那样，它的性能较弱。GOWebsocket与STDLIB大致相同。但是，如果您需要快速构建原型或MVP，则它可能是一个合理的选择。


除了这些工具之外，还有几种替代实现可让您构建强大的流处理解决方案。其中有：

流技术的不断发展以及WebSockets等文档较好的可用工具的存在，使开发人员可以轻松创建真正的实时应用程序。 如果您需要使用WebSockets创建实时应用程序的建议或帮助，请给我们写信。希望本教程对您有所帮助。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

抄袭国外文章，作者是不是可以写个“译”

朋友，我真没见过国内那本译著在标题上写上”译“这个大字的。所有译文都在正文标明了原文出处。另外这个不叫”抄袭“，是分享。如果你觉得涉及版权问题，可以让原作者联系我，我会及时撤掉文章的。

本文的源码能否公开一下？有些片段文中没有展示……

文中有标注：这是一篇译文。原文在https://yalantis.com/blog/how-to-build-websockets-in-go 因此，我这里并没有原文中涉及的全部源码。

Gorilla 在上个月宣布不再维护相关库了，我看声明里写的主要原因是主要维护人员离开，社区其他参与者贡献很少。想请教博主怎么看一个开源软件的发展历程呢？

任何一个开源软件都有其生命周期，生命周期长短视其性质、主要维护人/团队的个人喜好、项目知名度、社区参与度以及技术发展趋势等都有关。

像gorilla的websocket、mux等那样的小型库，随着时间的推移逐渐成熟，同时其社区规模肯定也无法与像k8s、linux这样的社区相比，并且也有其他替代品。

像mux开源已有10年，收获18k stars，已经是这个规模层次上非常成功的项目了。多数人在使用过程中都不会遇到什么问题了，即便有问题，自己fork一下，改改应该也没问题。作者这时将其archive也情有可原。

项目连接变成非法网站了,最好看一下,别被请去喝茶了,业余项目那个 https://51smspush.com/

感谢提醒。

做了个临时修改，每篇文章打开时做一次search & replace。这样一段时间后，应该就会替换完了。缺点：影响一些页面加载速度。