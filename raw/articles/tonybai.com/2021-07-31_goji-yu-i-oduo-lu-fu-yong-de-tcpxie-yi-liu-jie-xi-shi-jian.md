---
title: Go基于I/O多路复用的TCP协议流解析实践
url: https://tonybai.com/2021/07/31/io-multiplexing-model-tcp-stream-protocol-parsing-practice-in-go/
published: '2021-07-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go基于I/O多路复用的TCP协议流解析实践

![](../../assets/f27ff6c2161f48d2.png)


[本文永久链接](https://tonybai.com/2021/07/31/io-multiplexing-model-tcp-stream-protocol-parsing-practice-in-go) – https://tonybai.com/2021/07/31/io-multiplexing-model-tcp-stream-protocol-parsing-practice-in-go

在[《Go经典阻塞式TCP协议流解析的实践》](https://mp.weixin.qq.com/s/NG3f-KkjtJBTVdRHQKLXOg)一文中，我们基于Go经典的阻塞I/O模型实现了一个基于TCP流的自定义协议的解析。这种**one-connection-per-goroutine**模型的优点就是**简单、好写以及好理解**，降低开发者心智负担。但一旦连接数上来，goroutine的数量就会线性增加。当面对海量连接的场景，这种模型将力不从心：系统中将存在大量goroutine，goroutine调度和切换的开销过多。

那么面对海量连接场景，应该如何解决呢？业界成熟方案：**使用I/O多路复用模型**。了解Go net包实现的朋友想必都知晓Go在运行时底层使用的也是I/O多路复用，其实现为runtime中的[netpoll](https://github.com/golang/go/tree/master/src/runtime/netpoll.go)。goroutine层面获得的net.Conn(无论是Accept的，还是Dial得到的)都展现出“阻塞”的特征，但这些net.Conn底层实现的fd(文件描述符)在netpoll中都是non-blocking(非阻塞)的，Go运行时负责调用epoll等多路复用机制监视这些fd是否可读或可写，并适时唤醒goroutine继续网络I/O操作，这种方式减少了系统调用，也减少了运行Goroutine的M(操作系统线程)因系统调用陷入内核态等待的频率以及因阻塞失去M而不得不去创建新线程的数量。

那么在用户层面建立自己的I/O多路复用的不足在哪里呢？**复杂，不好写，不好理解**。但似乎也没有其他更好的办法。除非换语言，否则就得硬着头皮上^_^。好在，Go社区已经有几个不错的Go用户层面非阻塞I/O多路复用的开发框架库可供选择，比如：[evio](https://github.com/tidwall/evio)、[gnet](https://github.com/panjf2000/gnet)、[easygo](https://github.com/mailru/easygo)等。我们选择gnet。但注意：选择不代表推荐，这里仅是来做这个实践而已，是否使用gnet开发上生产的程序，需要你自己评估确定。

### 1. 基于gnet开发TCP流协议解析程序

**用框架的一个门槛就是你要去学习框架本身**。好在[gnet提供了几个很典型的examples](https://github.com/gnet-io/gnet-examples)，我们可以基于其中的[custom_codec](https://github.com/gnet-io/gnet-examples/tree/master/examples/custom_codec)来快速开发我们的TCP流协议解析程序。

下面是基于gnet框架实现custom codec的一个关键循环，了解这个循环，我们就知道在什么位置调用Frame编解码以及packet编解码了，这样决定了后续demo程序的结构：

![](../../assets/6b40b35a879c7f12.png)


上面图中右边虚框中的frame编解码、packet编解码以及React是用户需要自己实现的，gnet框架的eventloop.loopRead方法会循环调用frame编解码和React以实现TCP流的处理以及响应的返回。有了这样一张“地图”，我们就可以明确demo程序中各个包的大致位置了。

我们的demo改自gnet的例子[custom_codec](https://github.com/gnet-io/gnet-examples/tree/master/examples/custom_codec)，其main包结构来自于custom_codec：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo4/cmd/server/main.go
type customCodecServer struct {
*gnet.EventServer
addr string
multicore bool
async bool
codec gnet.ICodec
workerPool *goroutine.Pool
}
func (cs *customCodecServer) OnInitComplete(srv gnet.Server) (action gnet.Action) {
log.Printf("custom codec server is listening on %s (multi-cores: %t, loops: %d)\n",
srv.Addr.String(), srv.Multicore, srv.NumEventLoop)
return
}
func customCodecServe(addr string, multicore, async bool, codec gnet.ICodec) {
var err error
codec = frame.Frame{}
cs := &customCodecServer{addr: addr, multicore: multicore, async: async, codec: codec, workerPool: goroutine.Default()}
err = gnet.Serve(cs, addr, gnet.WithMulticore(multicore), gnet.WithTCPKeepAlive(time.Minute*5), gnet.WithCodec(codec))
if err != nil {
panic(err)
}
}
func main() {
var port int
var multicore bool
// Example command: go run server.go --port 8888 --multicore=true
flag.IntVar(&port, "port", 8888, "server port")
flag.BoolVar(&multicore, "multicore", true, "multicore")
flag.Parse()
addr := fmt.Sprintf("tcp://:%d", port)
customCodecServe(addr, multicore, false, nil)
}
```


针对上面代码，有两点要注意：

- customCodecServe的第三个参数我们传入了false，即我们选择同步回复应答，而不是异步回复。
- 我们将自定义的frame编解码器(实现了gnet.ICodec接口)实例传给了customCodecServer实例，这样后续gnet loopRead调用的就是我们自定义的frame编解码器了。

按上面流程图的顺序，gnet从conn读取的字节流将传递给我们的frame解码器，下面我们看看基于gnet的Frame解码器的实现(我们的自定义协议定义可以参考《Go经典阻塞式TCP协议流解析的实践》一文)：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo4/pkg/frame/frame.go
type Frame []byte
func (cc Frame) Decode(c gnet.Conn) ([]byte, error) {
// read length
var frameLength uint32
if n, header := c.ReadN(4); n == 4 {
byteBuffer := bytes.NewBuffer(header)
_ = binary.Read(byteBuffer, binary.BigEndian, &frameLength)
if frameLength > 100 {
c.ResetBuffer()
return nil, errors.New("length value is wrong")
}
if n, wholeFrame := c.ReadN(int(frameLength)); n == int(frameLength) {
c.ShiftN(int(frameLength)) // shift frame length
return wholeFrame[4:], nil // return frame payload
} else {
return nil, errors.New("not enough frame payload data")
}
}
return nil, errors.New("not enough frame length data")
}
```


上面Frame的Decode实现既负责frame解码，同时也会对frame的当前数据完整性进行校验，如果一个完整的frame尚未就绪，Decode会返回错误，之后gnet还会在连接(conn)可读时再次调用该Decode函数。这里实现的关键就是gnet.Conn.ReadN这个方法，这个方法本质上是一个Peek操作(gnet称之为lazyRead)，即只预览数据, 不挪动数据流中的“读指针”的位置。frame未完全就绪时，gnet在底层会使用RingBuffer存放已经到位的frame的部分数据。如果frame所有数据都就绪了，那么Decode会调用gnet.Conn.ShiftN方法来挪动底层RingBuffer的“读指针”的位置，表明这段数据已经被上层读取了。

如果预读取到的frame长度过长（这里代码中的100是一个魔数，仅做demo演示之用，你可以根据实际情况使用frame可能的最大值），则会清空当前缓存并返回错误。(但gnet并没有因此而断开与客户端的连接，这块儿gnet的机制是否合理还有待商榷。)

如果解码顺利，根据我们自定义的协议spec，我们会将frame的payload返回，即从frame的第五个字节开始返回。

从上图看到，frame Decode返回的payload将作为输入数据传给eventHandler.React方法，这个方法也是我们自己实现的：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo4/cmd/server/main.go
func (cs *customCodecServer) React(framePayload []byte, c gnet.Conn) (out []byte, action gnet.Action) {
var p packet.Packet
var ackFramePayload []byte
p, err := packet.Decode(framePayload)
if err != nil {
fmt.Println("react: packet decode error:", err)
action = gnet.Close // close the connection
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
action = gnet.Close // close the connection
return
}
out = []byte(ackFramePayload)
return
default:
return nil, gnet.Close // close the connection
}
}
```


在React中，我们利用packet包对传入的frame payload进行Decode并处理得到的Packet，处理后将packet响应进行编码(encode)，编码后得到的字节序列（ackFramePayload)将作为React的第一个返回值out返回。

frame会对React返回的ackFramePayload进行Encode，编码后的字节序列将被gnet写入outbound的tcp流中去：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo4/pkg/frame/frame.go
func (cc Frame) Encode(c gnet.Conn, framePayload []byte) ([]byte, error) {
result := make([]byte, 0)
buffer := bytes.NewBuffer(result)
// encode frame length(4+ framePayload length)
length := uint32(4 + len([]byte(framePayload)))
if err := binary.Write(buffer, binary.BigEndian, length); err != nil {
s := fmt.Sprintf("Pack length error , %v", err)
return nil, errors.New(s)
}
// encode frame payload
n, err := buffer.Write(framePayload)
if err != nil {
s := fmt.Sprintf("Pack frame payload error , %v", err)
return nil, errors.New(s)
}
if n != len(framePayload) {
s := fmt.Sprintf("Pack frame payload length error , %v", err)
return nil, errors.New(s)
}
return buffer.Bytes(), nil
}
```


这样一个loopRead循环就完成了。我们可以使用《Go经典阻塞式TCP协议流解析的实践》一文中的client对该程序进行测试：

```
// demo2的client
$./client
2021/07/25 16:35:34 dial ok
send submit id = 00000001, payload=full-bluestreak-207e
the result of submit ack[00000001] is 0
send submit id = 00000002, payload=cosmic-spider-ham-2985
the result of submit ack[00000002] is 0
send submit id = 00000003, payload=true-forge-3552
the result of submit ack[00000003] is 0
// demo4的server
$./server
2021/07/25 16:35:31 custom codec server is listening on :8888 (multi-cores: true, loops:
```

recv submit: id = 00000001, payload=full-bluestreak-207e
recv submit: id = 00000002, payload=cosmic-spider-ham-2985
recv submit: id = 00000003, payload=true-forge-3552


### 2. 压测对比

gnet针对内存分配、缓存重用等做了很多优化，我们来将其与阻塞I/O模型程序在性能上做一下简单比较(由于资源有限，我们这里的压测也和上一文中一样，采用100个client连接尽力(best effort)发送，而不是海量连接)。

下面是demo1(阻塞I/O模型未优化）、demo3(阻塞I/O模型优化后)以及demo4(io多路复用模型）的性能对比：

![](../../assets/562764c0cc26ec38.png)


粗略来看，采用gnet I/O多路复用模型的程序(demo4)在性能上平均比阻塞I/O模型优化后的程序(demo3)高出15%~20%。

不仅如此，通过dstat采集的系统监控数据也表明跑demo4时，cpu系统时间(sys)占用也比demo3少了5个点左右：

跑demo3时的dstat -tcdngym输出:

```
----system---- ----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system-- ------memory-usage-----
time |usr sys idl wai hiq siq| read writ| recv send| in out | int csw | used buff cach free
23-07 17:03:17| 2 1 97 0 0 0|3458B 19k| 0 0 | 0 0 | 535 2475 |1921M 225M 5354M 8386M
23-07 17:03:18| 40 45 5 0 0 11| 0 0 | 66B 54B| 0 0 | 11k 15k|1922M 225M 5354M 8384M
23-07 17:03:19| 39 46 6 0 0 9| 0 0 | 66B 1158B| 0 0 | 12k 18k|1922M 225M 5354M 8384M
23-07 17:03:20| 35 48 7 0 0 11| 0 0 | 66B 462B| 0 0 | 12k 22k|1922M 225M 5354M 8385M
23-07 17:03:21| 39 44 7 0 0 10| 0 12k| 66B 462B| 0 0 | 11k 16k|1922M 225M 5354M 8385M
23-07 17:03:22| 38 45 6 0 0 10| 0 0 | 66B 102B| 0 0 | 11k 16k|1923M 225M 5354M 8384M
23-07 17:03:23| 38 45 7 0 0 10| 0 0 | 66B 470B| 0 0 | 12k 20k|1923M 225M 5354M 8384M
23-07 17:03:24| 39 46 6 0 0 9| 0 0 | 66B 462B| 0 0 | 11k 19k|1923M 225M 5354M 8384M
```


跑demo4时的dstat -tcdngym输出：

```
----system---- ----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system-- ------memory-usage-----
time |usr sys idl wai hiq siq| read writ| recv send| in out | int csw | used buff cach free
24-07 20:28:38| 43 42 7 0 0 8| 0 20k|1050B 14k| 0 0 | 11k 18k|1954M 234M 5959M 7738M
24-07 20:28:39| 44 41 9 0 0 7| 0 16k| 396B 7626B| 0 0 | 11k 17k|1954M 234M 5959M 7739M
24-07 20:28:40| 43 42 6 0 0 8| 0 0 | 132B 7044B| 0 0 | 11k 16k|1954M 234M 5959M 7738M
24-07 20:28:41| 42 42 8 0 0 8| 0 0 | 630B 12k| 0 0 | 12k 20k|1955M 234M 5959M 7738M
24-07 20:28:42| 45 41 7 0 0 7| 0 0 | 726B 9980B| 0 0 | 11k 16k|1955M 234M 5959M 7738M
```


### 2. 异步回应答

在上面的例子中，我们采用的是gnet同步回应答的方式，gnet还支持异步回应答的方式，即将React中得到的ackFramePayload提交给gnet创建的一个goroutine Worker池，由worker池中的某个空闲goroutine在后续将ackFramePayload编码为一个完整的ackFrame后返回给client端。

要支持异步回应答，我们需要对demo4做几处修改（见demo5），主要修改点都在cmd/server/main.go中。

第一处：main函数调用customCodecServe时，将第三个参数async设置为true：

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo5/cmd/server/main.go
func main() {
... ...
customCodecServe(addr, multicore, true, nil)
}
```


第二处：在customCodecServer的React方法中，我们得到编码后的ackFramePayload后，不要立即将其赋值给out并返回，而是判断是否要异步返回应答。如果异步返回应答，则将ackFramePayload提交给workerpool，workerPool后续会分配goroutine，并通过gnet.Conn的AsyncWrite将应答写回client。如果非异步，在将ackFramePayload赋值给out并返回。

```
// github.com/bigwhite/experiments/tree/master/tcp-stream-proto/demo5/cmd/server/main.go
func (cs *customCodecServer) React(framePayload []byte, c gnet.Conn) (out []byte, action gnet.Action) {
... ...
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
action = gnet.Close // close the connection
return
}
default:
return nil, gnet.Close // close the connection
}
if cs.async {
data := append([]byte{}, ackFramePayload...)
_ = cs.workerPool.Submit(func() {
fmt.Println("handleConn: async write ackFramePayload")
c.AsyncWrite(data)
})
return
}
out = ackFramePayload
return
}
```


除此之外，其他包的代码不变。我们依然还做个压测，看看异步回应答的demo5性能究竟如何！

![](../../assets/7e3e9480f171c14e.png)


从上图来看，在这个场景下通过异步回应答的方式，性能反而下降很多，甚至还不如阻塞式I/O模型的程序。对此没有做深究，但猜测可能是应答过多且同时集中回复时workerpool创建了很多goroutine，不仅没有起到池化的作用，还带来的goroutine创建和调度的开销。

### 3. 小结

在本文中，我们将阻塞式I/O模型换成了I/O多路复用模型，并基于gnet框架重新实现了自定义TCP流协议的解析程序。在同步回应答的策略下，基于gnet开发TCP流协议解析程序相比于阻塞I/O模型程序的性能有一定提升。

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