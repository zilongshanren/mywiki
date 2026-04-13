---
title: Go经典阻塞式TCP协议流解析的实践
url: https://tonybai.com/2021/07/28/classic-blocking-network-tcp-stream-protocol-parsing-practice-in-go/
published: '2021-07-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go经典阻塞式TCP协议流解析的实践

![](../../assets/0326a0b1702fe017.png)


[本文永久链接](https://tonybai.com/2021/07/28/classic-blocking-network-tcp-stream-protocol-parsing-practice-in-go) – https://tonybai.com/2021/07/28/classic-blocking-network-tcp-stream-protocol-parsing-practice-in-go

### 1. Go经典阻塞I/O的TCP网络编程模型

[Go语言诞生十多年](https://mp.weixin.qq.com/s/woQeEQUhOLJ7KSE5rm5q6g)来取得了飞速发展，并得到了全世界开发者的广泛接纳和应用，其应用领域广泛，包括：Web服务、数据库、网络编程、系统编程、DevOps、安全检测与管控、数据科学以及人工智能等。下面是2020年Go官方开发者调查的部分结果：

![](../../assets/834596f2c1b7e427.png)



我们看到**“Web编程”**和**“网络编程”**分别位列第一名和第四名，这个应用领域数据分布与Go语言最初的面向大规模分布式网络服务的设计目标十分契合。**网络通信**这块是服务端程序必不可少也是至关重要的一部分。Go标准库的net包是在Go中进行网络编程的基础。即便您没有直接使用到net包中有关[TCP Socket](https://tonybai.com/2015/11/17/tcp-programming-in-golang/)方面的函数/方法或接口，但net/http包想必大家总是用过的，http包实现的是HTTP这个应用层协议，其在传输层使用的依旧是TCP Socket。

Go是自带运行时的跨平台编程语言，由于Go运行时调度的需要，Go基于**I/O多路复用**机制(linux上使用epoll，macOS和freebsd上使用kqueue)设计和实现了一套适合自己的TCP Socket网络编程模型。并且，Go秉承了自己一贯的[追求简单的设计哲学](https://www.imooc.com/read/87/article/2321)，Go向语言使用者暴露了简单的TCP Socket API接口，而将Go TCP socket网络编程的“复杂性”留给了自己并隐藏在Go运行时的实现中。这样，大多数情况下，Go开发者无需关心Socket是否是阻塞的，也无需亲自将Socket文件描述符的回调函数注册到类似epoll这样的系统调用中，而只需在每个连接对应的goroutine中以最简单最易用的**“阻塞I/O模型”**的方式进行Socket操作即可(像下图所示)，这种设计大大降低了网络应用开发人员的心智负担。

![](../../assets/b58499ad5c8ad800.png)


这是经典的Go tcp网络编程模型。由于TCP是全双工模型，每一端(peer)都可以单独在已经建立的连接上进行读写，因此在Go中，我们常常针对一个已建立的TCP连接建立两个goroutine，一个负责从连接上读取数据(如需响应(ack)，也可以由该read goroutine直接回复)，一个负责将新生成的业务数据写入连接。

以**read goroutine**为例，其典型的程序结构如下：

```
func handleConn(c net.Conn) {
defer c.Close()
for {
// read from the connection c
... ...
// write ack to the connection c
... ...
}
}
func main() {
l, err := net.Listen("tcp", ":8888")
if err != nil {
fmt.Println("listen error:", err)
return
}
for {
c, err := l.Accept()
if err != nil {
fmt.Println("accept error:", err)
break
}
// start a new goroutine to handle
// the new connection.
go handleConn(c) // start a read goroutine
}
}
```


从上面代码，我们看到，针对每一个向server建立成功的连接，程序都会启动一个reader goroutine负责从连接读取数据，并在处理后，返回(向连接写入)响应(ack)。这样的程序结构已经直白到无法再直白了，即便你是网络编程小白，看懂这样的程序想必也不会费多少脑细胞。

我们知道，TCP传输控制协议是一种面向连接的、可靠的、基于字节流的传输层通信协议，因此TCP socket编程多为流数据(streaming)处理。这种数据的特点是按序逐个字节传输，在传输层没有明显的数据边界(只有应用层能识别出协议数据的边界，这个依赖应用层协议的定义)。TCP发送端发送了1000个字节，TCP接收端就会接收到1000个字节。发送端可能通过一次发送操作就发送了这1000个字节，但接收端可能通过10次读取操作才读完这1000个字节，也就是说**发送端的发送动作与接收端的接收动作并没有严格的一一对应关系**。这与UDP协议基于数据报(diagram)形式的数据传输形式有本质差别(更多关于tcp与udp差别的内容可以详见[《TCP/IP详解卷1：协议》](https://book.douban.com/subject/26825411/)一书)。

本文我们就来了解一下基于经典Go阻塞式网络I/O模型对基于TCP流的自定义协议进行解析的基本模式。

### 2. 自定义协议简述

为了便于后续内容展开，我们现在这里说明一下我们即将解析的自定义流协议。基于TCP的自定义应用层流协议有两种常见的定义模式：

- 二进制模式

采用长度字段分隔，常见的包括：mqtt(物联网最常用的应用层协议之一)、[cmpp(中国移动互联网短信网关接口协议)](https://github.com/bigwhite/gocmpp)等。

- 文本模式

采用特定分隔符分割和识别，常见的包括http等。

这里我们使用二进制模式来定义我们即将解析的应用层协议，下面是协议的定义：

![](../../assets/7277c0f98feea7ff.png)


这是一个请求应答协议，请求包和应答包的第一个字段都是包总长度，这也是在应用层用于“分割包”的最重要字段。第二个字段则是用于标识包类型，这里我们定义四种类型：

```
onst (
CommandConn = iota + 0x01 // 0x01，连接请求包
CommandSubmit // 0x02，消息发送请求包
)
const (
CommandConnAck = iota + 0x80 // 0x81，连接请求的响应包
CommandSubmitAck //0x82，消息发送请求的响应包
)
```


ID是每个连接上请求的消息流水，多用于请求发送方后续匹配响应包之用。请求包与响应包唯一的不同之处在于最后一个字段，请求包定义了有效载荷(payload)，而响应包则定义了请求包的响应状态字段(result)。

明确了应用层协议包的定义后，我们就来看看如何解析这样的一个流协议吧。

### 3. 建立Frame和Packet抽象

在真正开始编写代码前，我们先来针对上述应用层协议建立两个抽象概念：Frame和Packet。

首先，我们设定无论是从client到server，还是server到client，数据流都是由一个接一个Frame组成的，上述的协议就封装在这一个个的Frame中。我们可以通过特定的方法将Frame与Frame分割开来：

![](../../assets/bfb0d011648e9826.png)


每个Frame由一个totalLength和frame payload构成，如下图左侧Frame结构所示：

![](../../assets/731708fb5852abde.png)


这样，我们通过Frame header: totalLength即可将Frame之间隔离开来。我们将Frame payload定义为一个packet，每个Packet的结构如上图右侧所示。每个packet包含commandID、ID和payload(packet payload)字段。

这样我们就将上述的协议转换为由Frame和Packet两个抽象组成的TCP流了。

### 4. 阻塞式TCP流协议解析的基本程序结构

建立完抽象后，我们就要开始解析这个协议了！下图是该阻塞式TCP流协议解析的server流程图：

![](../../assets/8ac3f3826e003601.png)


我们看到tcp流数据先后经由frame decode和packet decode后得到应用层所需的packet数据，应用层回复的响应则先后经过packet的encode与frame的encode后写入tcp响应流中。

下面我们就先来看看frame编解码的代码。我们首先定义frame编码器的接口类型：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/frame/frame.go
type FramePayload []byte
type StreamFrameCodec interface {
Encode(io.Writer, FramePayload) error // data -> frame，并写入io.Writer
Decode(io.Reader) (FramePayload, error) // 从io.Reader中提取frame payload，并返回给上层
}
```


我们将流数据的输入定义为io.Reader，将流数据输出定义为io.Writer。和上图中的设计意义，Decode方法返回framePayload，而Encode会将输入的framePayload编码为frame并写入outbound的tcp流。

一旦确定好接口方法集，我们就来给出一个StreamFrameCodec接口的实现：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/frame/frame.go
type myFrameCodec struct{}
func NewMyFrameCodec() StreamFrameCodec {
return &myFrameCodec{}
}
func (p *myFrameCodec) Encode(w io.Writer, framePayload FramePayload) error {
var f = framePayload
var totalLen int32 = int32(len(framePayload)) + 4
err := binary.Write(w, binary.BigEndian, &totalLen)
if err != nil {
return err
}
// make sure all data will be written to outbound stream
for {
n, err := w.Write([]byte(f)) // write the frame payload to outbound stream
if err != nil {
return err
}
if n >= len(f) {
break
}
if n < len(f) {
f = f[n:]
}
}
return nil
}
func (p *myFrameCodec) Decode(r io.Reader) (FramePayload, error) {
var totalLen int32
err := binary.Read(r, binary.BigEndian, &totalLen)
if err != nil {
return nil, err
}
buf := make([]byte, totalLen-4)
_, err = io.ReadFull(r, buf)
if err != nil {
return nil, err
}
return FramePayload(buf), nil
}
```


在上面在这段实现中，有三点要注意：

- 网络字节序使用
[大端字节序(BigEndian)](https://tonybai.com/2011/01/21/encounter-byte-order-problem-again/)，因此无论是Encode还是Decode，我们都是用binary.BigEndian； - binary.Read或Write会根据参数的宽度读取或写入对应的字节个数的字节，这里totalLen使用int32，那么Read或Write只会操作流中的4个字节；
- 这里没有设置deadline，因此io.ReadFull一般会读满你所需的字节数，除非遇到EOF或ErrUnexpectedEOF。

接下来，我们再看看Packet的编解码。和Frame不同，Packet有多种类型(这里仅定义了Conn, submit，connack, submit ack)。因此我们首先抽象一下这些类型需要遵循的共同接口：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/packet/packet.go
type Packet interface {
Decode([]byte) error // []byte -> struct
Encode() ([]byte, error) // struct -> []byte
}
```


其中Decode是将一段字节流数据解码为一个Packet类型，可能是conn，可能是submit等(根据解码出来的commandID判断)。而Encode则是将一个Packet类型编码为一段字节流数据。下面是submit和submitack类型的Packet接口实现：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/packet/packet.go
type Submit struct {
ID string
Payload []byte
}
func (s *Submit) Decode(pktBody []byte) error {
s.ID = string(pktBody[:8])
s.Payload = pktBody[8:]
return nil
}
func (s *Submit) Encode() ([]byte, error) {
return bytes.Join([][]byte{[]byte(s.ID[:8]), s.Payload}, nil), nil
}
type SubmitAck struct {
ID string
Result uint8
}
func (s *SubmitAck) Decode(pktBody []byte) error {
s.ID = string(pktBody[0:8])
s.Result = uint8(pktBody[8])
return nil
}
func (s *SubmitAck) Encode() ([]byte, error) {
return bytes.Join([][]byte{[]byte(s.ID[:8]), []byte{s.Result}}, nil), nil
}
```


不过上述各种类型的编解码被调用的前提是明确数据流是什么类型的，因此我们需要在包级提供一个对外的函数Decode，该函数负责从字节流中解析出对应的类型(根据commandID)，并调用对应类型的Decode方法：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/packet/packet.go
func Decode(packet []byte) (Packet, error) {
commandID := packet[0]
pktBody := packet[1:]
switch commandID {
case CommandConn:
return nil, nil
case CommandConnAck:
return nil, nil
case CommandSubmit:
s := Submit{}
err := s.Decode(pktBody)
if err != nil {
return nil, err
}
return &s, nil
case CommandSubmitAck:
s := SubmitAck{}
err := s.Decode(pktBody)
if err != nil {
return nil, err
}
return &s, nil
default:
return nil, fmt.Errorf("unknown commandID [%d]", commandID)
}
}
```


同样，我们也需要包级的Encode函数，根据传入的packet类型调用对应的Encode方法实现对象的编码：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/pkg/packet/packet.go
func Encode(p Packet) ([]byte, error) {
var commandID uint8
var pktBody []byte
var err error
switch t := p.(type) {
case *Submit:
commandID = CommandSubmit
pktBody, err = p.Encode()
if err != nil {
return nil, err
}
case *SubmitAck:
commandID = CommandSubmitAck
pktBody, err = p.Encode()
if err != nil {
return nil, err
}
default:
return nil, fmt.Errorf("unknown type [%s]", t)
}
return bytes.Join([][]byte{[]byte{commandID}, pktBody}, nil), nil
}
```


好了，万事俱备只欠东风！下面我们就来编写程序结构，将tcp conn与Frame、Packet连接起来：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1/cmd/server/main.go
package main
import (
"fmt"
"net"
"github.com/bigwhite/tcp-stream-proto/demo1/pkg/frame"
"github.com/bigwhite/tcp-stream-proto/demo1/pkg/packet"
)
func handlePacket(framePayload []byte) (ackFramePayload []byte, err error) {
var p packet.Packet
p, err = packet.Decode(framePayload)
if err != nil {
fmt.Println("handleConn: packet decode error:", err)
return
}
switch p.(type) {
case *packet.Submit:
submit := p.(*packet.Submit)
fmt.Printf("recv submit: id = %s, payload=%s\n", submit.ID, string(submit.Payload))
submitAck := &packet.SubmitAck{
ID: submit.ID,
Result: 0,
}
ackFramePayload, err = packet.Encode(submitAck)
if err != nil {
fmt.Println("handleConn: packet encode error:", err)
return nil, err
}
return ackFramePayload, nil
default:
return nil, fmt.Errorf("unknown packet type")
}
}
func handleConn(c net.Conn) {
defer c.Close()
frameCodec := frame.NewMyFrameCodec()
for {
// read from the connection
// decode the frame to get the payload
// the payload is undecoded packet
framePayload, err := frameCodec.Decode(c)
if err != nil {
fmt.Println("handleConn: frame decode error:", err)
return
}
// do something with the packet
ackFramePayload, err := handlePacket(framePayload)
if err != nil {
fmt.Println("handleConn: handle packet error:", err)
return
}
// write ack frame to the connection
err = frameCodec.Encode(c, ackFramePayload)
if err != nil {
fmt.Println("handleConn: frame encode error:", err)
return
}
}
}
func main() {
l, err := net.Listen("tcp", ":8888")
if err != nil {
fmt.Println("listen error:", err)
return
}
for {
c, err := l.Accept()
if err != nil {
fmt.Println("accept error:", err)
break
}
// start a new goroutine to handle
// the new connection.
go handleConn(c)
}
}
```


在上面这个程序中，main函数是标准的“one connection per goroutine”的结构，重点逻辑都在handleConn中。在handleConn中，我们看到十分清晰的代码结构：

```
read conn
->frame decode
-> handle packet
-> packet decode
-> packet(ack) encode
->frame(ack) encode
write conn
```


到这里，一个经典阻塞式TCP流解析的demo就完成了(你可以将demo中提供的client和server run起来验证一下)。

### 5. 可能的优化点

在上面的demo1中，我们直接将net.Conn实例传给frame.Decode作为io.Reader参数的实参，这样我们每次调用Read方法都是直接从Conn中读取数据。不过Go runtime使用net poller将net.Conn.Read转换为io多路复用的等待，避免了每次从net.Conn直接读取都转换为一次系统调用。但即便如此，也可能会多一次goroutine的上下文切换(在数据尚未ready的情况下)。虽然goroutine的上下文切换代价相较于线程切换要小许多，但毕竟这种切换并不是免费的，我们要减少这种切换。我们可以通过缓存读的方式来减少net.Conn.Read真实调用的频率。我们可以像下面这样改造demo1的例子：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo2/cmd/server/main.go
func handleConn(c net.Conn) {
defer c.Close()
frameCodec := frame.NewMyFrameCodec()
rbuf := bufio.NewReader(c) // 为io增加缓存
for {
// read from the connection
// decode the frame to get the payload
// the payload is undecoded packet
framePayload, err := frameCodec.Decode(rbuf) // 使用bufio，减少直接read conn.Conn的次数
if err != nil {
fmt.Println("handleConn: frame decode error:", err)
return
}
... ...
}
... ...
}
```


bufio内部每次从net.Conn尝试读取其内部缓存(buf)大小的数据，而不是用户传入的希望读取的数据大小。这些数据缓存在内存中，这样后续Read就可以直接从内存中得到数据，而不是每次都从net.Conn读取，从而降低goroutine上下文切换的频率。

除此之外，我们在frame包中的frame Decode实现如下：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo2/pkg/frame/frame.go
func (p *myFrameCodec) Decode(r io.Reader) (FramePayload, error) {
var totalLen int32
err := binary.Read(r, binary.BigEndian, &totalLen)
if err != nil {
return nil, err
}
buf := make([]byte, totalLen-4)
_, err = io.ReadFull(r, buf)
if err != nil {
return nil, err
}
return FramePayload(buf), nil
}
```


我们看到每次调用这个方法都会分配一个buf，并且buf是不定长的，这些在程序关键路径上的堆内存对象分配会给GC带来压力，我们要尽量避免或减小其频度，一个可行的办法是尽量重用对象，在Go中一提到重用内存对象，我们就想到了sync.Pool，但这里还有一个问题，那就是“不定长”，这给sync.Pool的使用增加了难度。

[mcache](https://github.com/bytedance/gopkg/tree/master/lang/mcache)是字节技术团队开源的多级sync.Pool包，它可以根据你所要分配的对象大小选择不同的sync.Pool池，有些类似tcmalloc的多级(class)内存对象管理，与Go runtime的mcache也是类似的，mcache一共分为46个等级，每个等级一个sync.Pool：

```
// github.com/bytedance/gopkg/tree/master/lang/mcache/mcache.go
const maxSize = 46
// index contains []byte which cap is 1<<index
var caches [maxSize]sync.Pool
```


我们可以从mcache中分配内存来换掉每次都申请一个[]byte的动作以达到内存对象重用，降低GC压力的目的：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo3/pkg/frame/frame.go
func (p *myFrameCodec) Decode(r io.Reader) (FramePayload, error) {
var totalLen int32
err := binary.Read(r, binary.BigEndian, &totalLen)
if err != nil {
return nil, err
}
buf := mcache.Malloc(int(totalLen - 4)) // 这里我们重用mcache中的内存对象
_, err = io.ReadFull(r, buf)
if err != nil {
return nil, err
}
return FramePayload(buf), nil
}
```


有了mcache.Malloc，我们就需要在特定位置调用mcache.Free归还内存对象，而packet中的Decode就是最好的位置：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo3/pkg/packet/packet.go
func Decode(packet []byte) (Packet, error) {
defer mcache.Free(packet) // 在decode结束后，释放对象回mcache
commandID := packet[0]
pktBody := packet[1:]
... ...
}
```


上面是两个在不动用pprof这样的工具的前提下就能识别出的较为明显的可优化的点，可优化的点可能还有很多，这里不一一列举了。

### 6. 简单的压力测试

既然给出了优化的点，我们就来粗略压测一下优化前和优化后的程序。我们为两个版本程序添加上基于标准库expvar的计数器(以优化前的demo1为例)：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1-with-metrics/cmd/server/main.go
func handleConn(c net.Conn) {
defer c.Close()
frameCodec := frame.NewMyFrameCodec()
for {
// read from the connection
... ...
// write ack frame to the connection
err = frameCodec.Encode(c, ackFramePayload)
if err != nil {
fmt.Println("handleConn: frame encode error:", err)
return
}
monitor.SubmitInTotal.Add(1) // 每处理完一条消息，计数器+1
}
}
```


在monitor包中，我们每秒计算一下处理性能：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo1-with-metrics/pkg/monitor/monitor.go
func init() {
// register statistics index
SubmitInTotal = expvar.NewInt("submitInTotal")
submitInRate = expvar.NewInt("submitInRate")
go func() {
var lastSubmitInTotal int64
ticker := time.NewTicker(time.Second)
defer ticker.Stop()
for {
select {
case <-ticker.C:
newSubmitInTotal := SubmitInTotal.Value()
submitInRate.Set(newSubmitInTotal - lastSubmitInTotal) // 两秒处理的消息量之差作为处理速度
lastSubmitInTotal = newSubmitInTotal
}
}
}()
}
```


有了基于expvar的计数器，我们就可以通过[带有导出csv功能的expvarmon工具](https://mp.weixin.qq.com/s/cr2JeUq5HOYQC0qji_Ip5g)获取程序每秒的处理性能了（压测客户端可以使用demo1-with-metrics的client)。下面的性能对比图是在一个4核8g的云主机上获得的（条件有限，压测client与server放在一台机器上了，必然相互干扰）：

![](../../assets/771a89140f007c04.png)


我们看到，优化后的程序从趋势上看略微好于优化前的(虽然不是很稳定)。

如果你觉得采集瞬时值太够专业^_^，也可以在被测程序上添加基于[go-metrics](ttps://mp.weixin.qq.com/s/pFTLGOsyl5DgohbSTBSr-w)的metric，这个作业就留给大家了:)

### 7. 小结

在本文中，我们简单说明了Go经典阻塞I/O的TCP网络编程模型，这种模型最大的好处就是简单，降低开发人员在处理网络I/O时的心智负担，将更多关注集中在业务层面。文中基于这种模型，给出了一个自定义流协议的解析实现框架，并说明了一些可优化的点。在非超大连接数量的场景下，这类模型会有不错性能和开发效率。一旦连接数量猛增，相应的处理这些连接的goroutine数量就会线性增加，Goroutine调度的开销就会显著增加，这个时候我们就要考虑是否使用其他模型应对了，这个我们在后续篇章再说。

本文涉及的所有代码可以从[这里下载](https://github.com/bigwhite/experiments/tree/master/tcp-stream-proto)：https://github.com/bigwhite/experiments/tree/master/tcp-stream-proto

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论