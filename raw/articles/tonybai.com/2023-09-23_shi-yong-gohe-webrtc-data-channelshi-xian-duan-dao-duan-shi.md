---
title: 使用Go和WebRTC data channel实现端到端实时通信
url: https://tonybai.com/2023/09/23/p2p-rtc-implementation-with-go-and-webrtc-data-channel/
published: '2023-09-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Go和WebRTC data channel实现端到端实时通信

![](../../assets/edcf1e76fb9ba788.png)


[本文永久链接](https://tonybai.com/2023/09/23/p2p-rtc-implementation-with-go-and-webrtc-data-channel) – https://tonybai.com/2023/09/23/p2p-rtc-implementation-with-go-and-webrtc-data-channel

关于实时通信(RTC，Real-Time Communication)，我和大多数人一样，是用的多(比如网络电话、音视频会议等)，但对RTC概念和其底层技术原理了解的却不多。近期，一项目恰用到了RTC技术，我就顺便翻阅了一些资料，并用Go建立了一个端到端数据通信的小demo，这里给大家分享一下。

## 1. RTC与WebRTC

### 1.1 实时通信(Real-Time Communication)

实时通信（RTC）是实时发生的任何在线通信。生活中，最常见的采用实时通信方式的例子就是电话：一旦双方接通后，**数据便直接从发送方即时发送到接收方，不会存储在前往目的地的途中**。

而传统的邮件以及互联网电子邮件则并非实时通信，因为在邮件/电邮的场景下，**我们发送数据后，对方通常要等待一段时间才能收到数据，同时我们也需要等待一段时间才能收到回复**。相信这个反例可以更好地帮助大家理解实时通信的特点。

总结一下，实时通信具有以下特点(想象一下打电话的过程)：

- 存在接通的过程
- 点对点(通常没有中间存储或处理节点)
- 传输低延迟

### 1.2 WebRTC技术的诞生

显然RTC技术是一种能给人们生活带来极大便捷的技术，尤其是在音视频实时传输方面，但很长时间以来，实时通信技术都十分复杂，还有专利门槛，将实时通信技术与业务结合既非常困难，又十分耗时，并且即便大力投入也未必能取得很好的效果，通常只有大厂才有这个能力实现稍完善的RTC方案和产品。

此外，随着Web技术的兴起、移动互联网时代的到来、4G/5G和宽带技术的蓬勃发展，人们都迫切希望将实时通信技术与Web等技术融合在一起，通过浏览器或智能终端即可快速建立音视频的实时数据通信。

于是2009年谷歌出手了！

- 2009年，谷歌提出了创建WebRTC的概念，作为Adobe Flash以及无法在浏览器中运行的桌面应用程序的替代方案。
- 2010年，谷歌收购了大量提供RTC技术授权的公司。
- 2011年，
[谷歌开源了WebRTC项目](https://webrtc.googlesource.com/src)。 - 2011年末，
[W3C](https://www.w3.org/)发布第一个WebRTC规范草案。 - 2013年，谷歌和Mozilla展示了基于WebRTC的异构浏览器之间的视频通话。
- 2017年，WebRTC进入候选推荐标准（Candidate Recommendation，CR）阶段。
- 2021年初，
[WebRTC成为W3C正式推荐标准及IETF标准](https://www.w3.org/zh-hans/press-releases/2021/webrtc-rec/)。

如今，WebRTC已经广泛用在了在线教育、电商直播、泛娱乐社交等应用领域。

### 1.3 WebRTC简明介绍

WebRTC(Web Real-Time Communication)是一套开源的点对点实时通信技术，最初为Web打造，旨在让Web应用可以直接在浏览器中进行实时的音视频通信和数据交换，而无需安装第三方插件。WebRTC具体体现为一组开源协议、引擎和API。

下面是W3C出品的WebRTC的技术栈的架构图(来自https://webrtc.github.io/webrtc-org/architecture/)：

![](../../assets/b96a5e2bb5b668e2.png)


我们看到WebRTC还是蛮复杂的，涉及到多类API、会话/信令管理、音频编解码算法引擎、视频编解码算法引擎、包含多种协议的传输层以及底层音视频捕捉和渲染等。全面掌握WebRTC全技术栈是很困难的，好在上面的架构图将不同领域的开发者的关注点做了标记，**大多数开发者关注WebRTC API和Web API即可**。并且，随着WebRTC自身的演进，目前WebRTC已经不局限于浏览器，可以应用于其他各种应用程序。在Go社区，最知名的WebRTC类项目莫过于[pion](https://github.com/pion/)了，它提供了[纯Go的WebRTC API实现](https://github.com/pion/webrtc)，任何Go应用都可以使用pion的WebRTC API开发点对点实时通信应用。

### 1.4 WebRTC相关的协议

WebRTC并没有全部另立炉灶从头建立很多新协议，而是复用了很多成熟的网络协议和应用协议，尤其是涉及数据传输的协议。下图是[WebRTC中使用的一些重要协议](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols)分布图：

![](../../assets/10f2f67fecae0bd5.png)



很多协议大家都非常熟悉，比如HTTP、WebSocket、TLS、TCP、UDP等，但也有些协议是大家比较陌生的，如RTP/SRTP、SCTP等，针对这些陌生协议，我们下面简要介绍一下：

#### 1.4.1 RTP(Real-time Transport Protocol，实时传输协议)和SRTP(Secure RTP)

RTP协议支持通过IP网络实时传输音频和视频。RTP常用于流媒体服务的通信系统，例如网络电话、视频电话会议等系统。RTP也是WebRTC使用的最重要的协议之一，在WebRTC中，RTP用于在WebRTC客户端(比如浏览器)之间传输音频和视频媒体(media)数据包。

RTP是专为流媒体的端到端实时传输设计的，更关注信息的实时性，可以避免出现因网络传输丢失数据造成通话质量下降的情况。并且，如上图所示，RTP都是基于UDP构建的，并额外提供抖动补偿、包丢失检测和无序传递检测的功能。

此外，RTP在传递媒体流时会为每个媒体流建立一个会话，即音频和视频流各自使用单独的RTP会话，这样接收端就能有选择性地接收媒体流(音频、视频或音视频)。

基础的RTP没有内置任何安全机制，因此不能保证传输数据的安全性，这样端与端之间通信传输未加密的数据时，都有可能被第三方拦截并窃取。为此，WebRTC规范明确禁止使用未加密的RTP，而是使用安全增强后的SRTP(Secure RTP)。SRTP可以为单播和多播应用程序中的RTP数据提供加密、消息身份验证和完整性以及重放攻击保护等安全功能。

注：对于非音频或视频数据，WebRTC不使用RTP，而是在通信的两端建立一个data channel用于交换任意格式的数据。


#### 1.4.2 SCTP(Stream Control Transmission Protocol，SCTP）

WebRTC的端与端建立连接后，音视频数据的交互由RTP/SRTP协议完成，但非音视频数据，则由两端之间建立的数据通道(data channel)完成。数据通道支持传输字符串、文件、图片等数据。

数据通道API的使用方式与[WebSocket](https://tonybai.com/2019/09/28/how-to-build-websockets-in-go/)非常相似，但是WebSocket运行于TCP之上，而WebRTC数据通道的底层传输使用了DTLS/UDP，具有较高的安全性，上层则是使用SCTP，默认使用可靠且有序的方式进行数据传输。

[SCTP](https://www.rfc-editor.org/rfc/rfc9260)是在2000年由IETF的SIGTRAN工作组定义的一个传输层协议。它是面向连接、端到端、全双工、带有流量和拥塞控制的可靠传输协议，本来与TCP和UDP处于同一级别，可以直接运行在IP之上。只是在WebRTC中，它被用在了应用层。

WebRTC充分利用了SCTP的面向消息(非tcp那样的面向流)的、带有拥塞控制算法的可靠传输机制，同时SCTP支持在一个传输通道中关联多个流的特性，这样每个流可以单独处理，甚至可以具有不同的可靠性属性。流与流之间不存在线头阻塞问题。流由流编号标识，可以在一定程度上提供多路复用功能，而无需开多个SCTP连接。

#### 1.4.3 SDP(Session Description Protocol, 会话描述协议)

[SDP](https://developer.mozilla.org/en-US/docs/Glossary/SDP)是一种文本形式的会话描述协议，用于描述多媒体会话的参数。

SDP是WebRTC端与端建立连接过程中必须要使用的协议。WebRTC使用SDP来描述对等连接的两端的媒体特征，包括会话属性、会话活动的时间、会话包含的媒体信息、媒体编/解码器、媒体地址和端口信息以及网络带宽的信息等。

下面是SDP协议内容的一个典型例子(来自https://developer.mozilla.org/en-US/docs/Glossary/SDP)：

```
v=0
o=alice 2890844526 2890844526 IN IP4 host.anywhere.com
s=
c=IN IP4 host.anywhere.com
t=0 0
m=audio 49170 RTP/AVP 0
a=rtpmap:0 PCMU/8000
m=video 51372 RTP/AVP 31
a=rtpmap:31 H261/90000
m=video 53000 RTP/AVP 32
a=rtpmap:32 MPV/90000
```


WebRTC的两个端在使用RTP/SRTP传输音视频数据或使用SCTP传输data channel数据之前，需要先建立连接。建立连接的过程类似于传统电话从拨号、呼叫等待、到接通的过程。这个过程通常会有一个叫信令服务器(signaling server)的中间角色(好比文首配图的人工电话交换机)参与。而SDP在建连过程中起着重要作用，信令服务器会将两端的SDP转发给另一方，直到两端都拥有了自己和对方的会话描述信息(SDP承载)，并在媒体交换格式方面达成了一致，这是两端连接成功的前提。

注：SDP不是WebRTC专属的，SDP在很多领域有广泛应用，最常见的就是即时通信(IM)领域。


#### 1.4.4 STUN、TURN和ICE

使用WebRTC进行实时通信的两端通常都位于防火墙或NAT之后的“内网”，只有很少部分主机能够拥有独立的公网IP而直接接入Internet。也就是说，尝试建立连接的双方由于位于NAT网络之中，不能直接使用内网IP地址建立网络连接。WebRTC于是使用“NAT穿透技术(俗称打洞)”来帮助两端建立连接。

STUN就是一种最常见的NAT穿透协议，其全称是“Simple Traversal of UDP Through NATs”，即简单的用UDP穿透NAT。STUN本质上是一种公网地址及端口的发现协议，客户端向STUN服务器发送请求，STUN服务器返回客户端的公网地址及NAT网络信息。这些信息用于构建在ICE打洞时的候选地址，并由信令服务器转发给另一端。

不过STUN无法应对所有NAT网路情形，在对称NAT(映射的外网地址端口号不固定，会随着目的地址的变化而变化)情况下，WebRTC用户无法使用STUN协议建立P2P连接，这种情况就需要借助TURN协议提供的服务进行流量中转。

TURN（Traversal Using Relays around NAT）是一种通过数据转发的方式穿透NAT的，解决了防火墙和对称NAT的问题。TURN支持UDP和TCP协议。

注：使用STUN建立的是P2P的网络模型，网络连接直接建立在通信两端，没有中间服务器介入；而使用TURN建立的是流量中继的网络模型，用户两端都与TURN服务建立连接，用户的网络数据包通过TURN服务进行转发 — 《WebRTC技术详解》


我们看到，TURN与STUN的共同点都是通过修改应用层中的私网地址达到NAT穿透的效果，不同点是TURN是通过两方通讯的“中间人”方式实现穿透。但TURN与其他中继控制协议也有不同，它能够允许一个客户端使用一个中继地址与多个对端连接。

ICE(Interactive Connectivity Establishment, 交互式连接建立)跟STUN和TURN不一样，ICE不是一种协议，而是一个框架（Framework），它整合了STUN和TURN，并利用STUN和TURN服务器来帮助两端建立起连接。

WebRTC的一端通过ICE获得的每个网络信息都会被包装成一个ICE候选者(candidate)。ICE候选者描述了用于建立网络连接的网络信息，包含网络协议、IP地址、端口等。如果设备上有多个IP地址，那么每个IP地址都会对应一个候选。例如设备A上有内网IP地址IP-1，还有公网IP地址IP-2，A通过IP-1可以直接与B进行通信，但是WebRTC不会判断优先使用哪个IP地址，而是同样从两个IP地址收集候选，并将候选信息通过信令服务器转发给另一端。

ICE候选者有多种类型(以基于UDP传输为例)，包括host（本机候选）、srflx（映射候选）、relay（中继候选）和prflx（来自对称NAT的映射候选）。类型有优先级次序，其中host优先级最高，relay优先级最低。比如WebRTC收集到了两个候选者，一个是host类型，另一个是srflx类型，那么WebRTC一定会先尝试与host类型的Candidate建立连接，如果不成功，才会使用srflx类型的Candidate。

当两端都得到自己和对方的ICE候选信息后，就会进行ICE候选配对，并最终选出一个用于建立端与端连接的**ICE候选者对(pair)**，最终两端将基于这个候选者对中的网络信息建立了P2P的连接。

有了上面协议这层铺垫后，接下来我们再来看WebRTC建立连接的流程就容易多了。

### 1.5 WebRTC的建连流程

下面是WebRTC的典型建连流程图：

![](../../assets/376ef956fcd2e55c.png)


如图所示，WebRTC端到端建立连接的**第一步**是与信令服务器建立连接并交换SDP信息。

信令服务器通常位于两端都能访问到的公网。当WebRTC一端启动后，它可能不知道要与谁通信，或者仅知道对方的极少的信息（比如一个ID），信令服务器可以帮助参与通信的两端解决这个问题。就像前面说的，你可以**将信令服务器看作是电话人工交换机及其操作员**，它可以帮助参与通信的两端找到彼此。WebRTC并未将信令服务器以及信令协议标准化，因为信令服务器是“业务相关”的，究竟是建立一对一连接，还是建立群聊，这些由信令服务器的业务来决定。承载信令的协议可以是普通的HTTP，也可以是WebSocket，亦可是像XMPP那样的专用信令协议。

在WebRTC中，主动发起连接的一方会创建offer，并通过信令服务器将offer转发给另一方；另一方收到offer后会创建answer，并同样通过信令服务器转发给发起方。无论是offer，还是answer，都包含了各自的SDP信息。

第二步，当交换SDP后，两端各自发起ICE过程，向STUN/TURN服务器发起请求，获取各自NAT后的公网信息，并形成ICE候选者。

第三步，双方通过信令服务器交换ICE候选者信息

当ICE候选者配对成功后，就来到了第四步，WebRTC两端直接建立连接。连接建立成功后，便可以进行数据传输交换了。

## 2. WebRTC data channel

上面提到过，WebRTC除了提供了音视频媒体实时通信能力外，还支持可以传输非媒体流数据的[数据通道(data channel)](https://w3c.github.io/webrtc-pc/#rtcdatachannel)。

和音视频数据一样，经由WebRTC数据通道进行的数据交换不经过服务器，不受服务器性能及带宽瓶颈的限制，同时减少了数据被拦截的概率。数据通道底层传输使用了DTLS，具有较高的安全性。上层使用SCTP，默认使用可靠且有序的方式进行数据传输。此外，data channel的建连过程与音视频的建连过程也是一致的。

下面我们就来用一个实际的例子展示一下如何使用Go建立基于WebRTC data channel的端到端实时通信。

## 3. 基于Go和Pion的WebRTC data channel应用示例

通过前面的介绍，我们知道了WebRTC技术栈十分复杂，日常WebRTC应用开发时，我们一般会基于开源的实现进行开发。Go语言在WebRTC开发领域也有比较成熟的开源项目，如Pion。[Pion](https://github.com/pion)提供了纯Go实现的WebRTC API实现以及WebRTC相关组件实现，使用Pion可以帮助我们快速高效开发WebRTC服务器和客户端应用。

### 3.1 pion: 纯Go的WebRTC实现

根据pion之父的说法，pion的诞生源于用WebRTC构建东西的挫败感，这种挫败感来源于Google开源的首个webrtc实现[libwebrtc](https://webrtc.googlesource.com/src/)，因为将libwebrtc构建和运行起来似乎十分困难。

pion就是根据libwebrtc的教训而设计的，pion给开发者的第一印象就是它十分容易构建和运行起来。这一定程度要归功于pion是用Go编写的，更模块化，也更透明，并且pion之父最初便考虑了将其用在Chromium之外的应用中。

pion是一个纯粹的WebRTC软件的Go集合, 涵盖了WebRTC项目中需要的所有主要元素：

![](../../assets/91ec961b2f895afb.png)


同时，pion项目还为WebRTC开发者贡献了一本非常好的WebRTC资料[《WebRTC For The Curious》](https://webrtcforthecurious.com)，很值得一读。另外，[pion项目的examples](https://github.com/pion/webrtc/blob/master/examples/README.md)也十分丰富，非常利于初学者快速掌握WebRTC以及如何使用pion开发WebRTC应用。

下面我们就基于pion的webrtc实现项目开发一个基于data channel的端到端实时通信示例。

根据之前对WebRTC建立过程的说明，我们首先需要设计一下这个示例的信令服务器以及信令协议。

### 3.2 信令服务与协议设计

信令服务器在WebRTC通信中扮演协调者的角色。它传递客户端的媒体参数和连接候选信息。

我们的业务模型是，信令服务器维护一个被动连接的peer集合，这个集合中的peer是在这些peer在启动时通过register信令注册到信令服务器中的，每个peer有一个唯一的ID，我称这个集合为**answer peer集合**吧。主动连接方(这里称为offer peer)则通过ID去连接answer peer。一旦建立与某个peer的连接后，它们便可以通过建立的data channel全双工的实时通信了。下面是信令服务与offer peer和answer peer的信令交互图：

![](../../assets/71c71f9d78f706af.png)


参照前面提到的WebRTC建连过程，你可以很容易的看懂这个协议设计。

这里我设计了一个Message抽象来表示信令服务可以收发的消息：

```
//webrtc-data-channel/signaling/proto/proto.go
type Message struct {
Cmd int `json:"command"`
Payload []byte `json:"payload"` // carry all kinds of request and response
}
```


其中的Cmd字段标识Message类型，可选值如下：

```
//webrtc-data-channel/signaling/proto/proto.go
const (
// originated from answer peer
CmdInit = iota + 1
CmdAnswer
// originated from answer peer
CmdOffer
// from both peer
CmdCandidate
)
const (
CmdInitResp = iota + 101 // CmdInit + 100
CmdAnswerResp
CmdOfferResp
CmdCandidateResp
)
```


Message既可以承载Request，亦可以承载Response。Message的Payload字段中存放的是Request或Response序列化后的结果。Request和Response结构如下：

```
//webrtc-data-channel/signaling/proto/proto.go
// Request is one kind of payload for Message
type Request struct {
SourceID string `json:"source"`
TargetID string `json:"target"`
Body []byte `json:"body"` // carry register, offer, answer, candidate
}
// Request is another payload for Message
type Response struct {
Code int `json:"code"`
Msg string `json:"msg"`
}
```


Request类型的Body中存放的是WebRTC Offer/Answer的SDP以及ICE Candidate序列化后的结果。

此外，在这个示例中，我们使用[WebSocket](https://tonybai.com/2019/09/28/how-to-build-websockets-in-go/)来作为信令协议的载体，便于信令服务器与offer peer/answer peer进行双向通信。

### 3.3 信令服务器的实现

按照上述设计，我们的信令服务器就是一个websocket的server：

```
//webrtc-data-channel/signaling/main.go
func main() {
flag.Parse()
log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds)
http.HandleFunc("/register", register) // for peerAnswer
http.HandleFunc("/offer", offer) // for peerOffer
log.Fatal(http.ListenAndServe(*addr, nil))
}
```


在这个server中我们提供了两个endpoint，一个是/register，供answer peer建立连接使用；另外一个是/offer，供offer peer与信令服务器建连并通信的。

两个endpoint对应的Handler的处理模式也相对一致，都是进入一个event loop中。

```
//webrtc-data-channel/signaling/main.go
func register(w http.ResponseWriter, r *http.Request) {
c, err := upgrader.Upgrade(w, r, nil) // *websocket.Conn
if err != nil {
log.Print("signaling: websocket upgrade error:", err)
return
}
defer c.Close()
err = answerPeerEventLoop(c, w)
if err != nil {
log.Println("signaling: answerPeerEventLoop error:", err)
return
}
log.Println("signaling: answerPeerEventLoop exit")
}
func offer(w http.ResponseWriter, r *http.Request) {
c, err := upgrader.Upgrade(w, r, nil) // *websocket.Conn
if err != nil {
log.Print("signaling: websocket upgrade error:", err)
return
}
defer c.Close()
err = offerPeerEventLoop(c, w)
if err != nil {
log.Println("signaling: offerPeerEventLoop error:", err)
return
}
log.Println("signaling: offerPeerEventLoop exit")
}
```


注：offer和register这两个Handler都会在单独的goroutine中执行。


offerPeerEventLoop和answerPeerEventLoop的代码都比较长，这里就不贴出来了。这两个函数的代码也都比较模式化，基本处理流程就是读取一个Message，判断Message的Cmd类型，然后根据Cmd类型分别处理，处理的逻辑参见上面信令服务器的信令处理流程：基本上就是转发、转发、转发。

### 3.4. answer peer的实现

answer peer启动后会建立RTCPeerConnection类型实例，并设置RTCPeerConnection实例的事件处理函数：

- OnICECandidate

本地收集到ICE候选者信息，处理动作是将这些ICE候选者信息通过信令服务转发到对端。

- OnConnectionStateChange

当与对端的连接状态发生变化时触发，比如连接建立、连接断开时。处理动作仅为输出相应的日志。

- OnDataChannel

当与对端的Data Channel创建成功时，处理逻辑是注册DataChannel.OnOpen和DataChannel.OnMessage两个事件处理函数。

完成这些后，answer peer会向上面设计的那样，与信令服务器建立连接，并发送请求到信令服务的/register端点，然后进入event loop。在event loop中负责处理信令服务器转发过来的Offer、Candidate等信息，以及各种信令服务器返回的Response。

当收到Offer时，answer peer会创建Answer并发给信令服务器；当收到Candidate时，会调用AddICECandidate将Candidate信息添加到peerConnection中，供后续配对使用。后续WebRTC连接自动建立后，便可以通过data channel收发数据了。

answer peer的代码较长，大家可以自行到https://github.com/bigwhite/experiments/tree/master/webrtc-data-channel/answer阅读。

注：answer peer的代码改编自

[pion/webrtc项目]的[pion-to-pion/answer示例]。

### 3.5. offer peer的实现

offer peer的实现与answer相似。

offer peer启动后会建立RTCPeerConnection类型实例，并设置RTCPeerConnection实例的事件处理函数：

- OnICECandidate
- OnConnectionStateChange
- DataChannel的OnOpen
- DataChannel的OnMessage

offer peer会主动创建DataChannel，然后与信令服务器建立连接，并发送请求到信令服务的/offer端点并主动向信令服务器发送Offer，最后进入event loop。在event loop中负责处理信令服务器转发过来的Answer、Candidate等信息，以及各种信令服务器返回的Response。

当收到Answer时，offer peer会将Answer中携带的SDP传给SetRemoteDescription，同时调用SetLocalDescription开启ICE候选者的收集过程；当收到Candidate时，会调用AddICECandidate将Candidate信息添加到peerConnection中，供后续配对使用。后续WebRTC连接自动建立后，便可以通过data channel收发数据了。

offer peer的代码较长，大家可以自行到https://github.com/bigwhite/experiments/tree/master/webrtc-data-channel/offer阅读。

注：offer peer的代码改编自

[pion/webrtc项目]的[pion-to-pion/offer示例]。

### 3.6 运行示例

下面我们来运行一下这个示例。

先来启动信令服务器：

```
$cd webrtc-data-channel/signaling
$go run main.go
```


启动answer peer：

```
$cd webrtc-data-channel/answer
$go run main.go
2023/09/23 21:24:45.201213 answer: NewPeerConnection ok
2023/09/23 21:24:45.201256 answer: connecting to ws://localhost:18080/register
2023/09/23 21:24:45.203993 answer: recv resp[101]: proto.Response{Code:0, Msg:"ok"}
```


这时我们会从信令服务器的输出日志中看到：

```
2023/09/23 21:24:45.203702 signaling: add answer peer: answer-peer-1
```


我们看到，answer peer成功注册到信令服务器中了，其ID为answer-peer-1。

下面我们来启动offer peer，其要连接的target为answer-peer-1：

```
$cd webrtc-data-channel/offer
$go run main.go -target answer-peer-1
2023/09/23 21:25:26.462845 offer: new peerConnection ok
2023/09/23 21:25:26.462880 offer: create new channel
2023/09/23 21:25:26.462890 offer: connecting to ws://localhost:18080/offer
2023/09/23 21:25:26.464863 offer: create offer
2023/09/23 21:25:26.465131 offer: recv resp[103]: proto.Response{Code:0, Msg:"ok"}
2023/09/23 21:25:26.465957 offer: recv answer(sdp) message from answer-peer-1
2023/09/23 21:25:26.466064 offer: set local desc
2023/09/23 21:25:26.466099 offer: set remote desc
2023/09/23 21:25:26.466201 offer: Peer Connection State has changed: connecting
2023/09/23 21:25:26.466297 offer: recv candidate message from answer-peer-1
2023/09/23 21:25:26.466344 offer: invoke peerConnection.OnICECandidate: webrtc.ICECandidate{statsID:"candidate:KsXlIk2JNeiDqK3l+znsoB3sDwuh1/2x", Foundation:"4104056053", Priority:0x7effffff, Address:"192.168.1.105", Protocol:1, Port:0xc2b1, Typ:1, Component:0x1, RelatedAddress:"", RelatedPort:0x0, TCPType:""}
2023/09/23 21:25:26.466506 offer: recv resp[104]: proto.Response{Code:0, Msg:"ok"}
2023/09/23 21:25:26.468342 offer: Peer Connection State has changed: connected
2023/09/23 21:25:26.469105 offer: Data channel 'data'-'824634439080' open. Random messages will now be sent to any connected DataChannels every 5 seconds
2023/09/23 21:25:26.859774 offer: recv candidate message from answer-peer-1
2023/09/23 21:25:31.469811 offer: Sending 'offer-1013426535'
2023/09/23 21:25:31.470846 offer: Message from DataChannel 'data': 'answer-695102175'
2023/09/23 21:25:36.469653 offer: Sending 'offer-2065047193'
2023/09/23 21:25:36.470495 offer: Message from DataChannel 'data': 'answer-750781464'
2023/09/23 21:25:41.469603 offer: Sending 'offer-153497802'
2023/09/23 21:25:41.469938 offer: Message from DataChannel 'data': 'answer-2102723687'
2023/09/23 21:25:46.469504 offer: Sending 'offer-1287609150'
2023/09/23 21:25:46.470097 offer: Message from DataChannel 'data': 'answer-645051512'
2023/09/23 21:25:51.470078 offer: Sending 'offer-1486812657'
2023/09/23 21:25:51.470572 offer: Message from DataChannel 'data': 'answer-1325372035'
```


offer peer的启动引发了“连锁反应”，在信令服务器的帮助下，offer peer与answer peer成功建立了连接，并在打开的Data Channel进行着“定时”的双工实时通信。

信令服务器的输出日志如下：

```
2023/09/23 21:25:26.465049 signaling: recv request[3] from offer peer
2023/09/23 21:25:26.465070 signaling: send offer resp ok
2023/09/23 21:25:26.465073 signaling: add offer peer: offer-peer-1
2023/09/23 21:25:26.465085 signaling: forward request[3] to answer peer ok
2023/09/23 21:25:26.465247 signaling: recv offer response from answer peer
2023/09/23 21:25:26.465868 signaling: recv request[2] from answer peer
2023/09/23 21:25:26.465896 signaling: forward request[2] to offer peer[offer-peer-1] ok
2023/09/23 21:25:26.466003 signaling: recv answer response from offer peer
2023/09/23 21:25:26.466218 signaling: recv request[4] from answer peer
2023/09/23 21:25:26.466245 signaling: forward request[4] to offer peer[offer-peer-1] ok
2023/09/23 21:25:26.466363 signaling: recv candidate response from offer peer
2023/09/23 21:25:26.466415 signaling: recv request[4] from offer peer
2023/09/23 21:25:26.466429 signaling: send offer resp ok
2023/09/23 21:25:26.466435 signaling: add offer peer: offer-peer-1
2023/09/23 21:25:26.466445 signaling: forward request[4] to answer peer ok
2023/09/23 21:25:26.466526 signaling: recv candidate response from answer peer
2023/09/23 21:25:26.859520 signaling: recv request[4] from answer peer
2023/09/23 21:25:26.859609 signaling: forward request[4] to offer peer[offer-peer-1] ok
2023/09/23 21:25:26.859951 signaling: recv candidate response from offer peer
```


answer peer的输出日志如下：

```
2023/09/23 21:25:26.465182 answer: recv offer message from offer-peer-1
2023/09/23 21:25:26.465823 answer: send sdp answer
2023/09/23 21:25:26.465834 answer: Peer Connection State has changed: connecting
2023/09/23 21:25:26.465925 answer: set local desc
2023/09/23 21:25:26.465928 answer: recv resp[102]: proto.Response{Code:0, Msg:"ok"}
2023/09/23 21:25:26.466108 answer: invoke peerConnection.OnICECandidate: 192.168.1.105
2023/09/23 21:25:26.466285 answer: recv resp[104]: proto.Response{Code:0, Msg:"ok"}
2023/09/23 21:25:26.466481 answer: recv candidate message from offer-peer-1
2023/09/23 21:25:26.468475 answer: Peer Connection State has changed: connected
2023/09/23 21:25:26.469002 answer: New DataChannel data 824634440046
2023/09/23 21:25:26.469049 answer: Data channel 'data'-'824634440046' open. Random messages will now be sent to any connected DataChannels every 5 seconds
2023/09/23 21:25:26.859199 answer: invoke peerConnection.OnICECandidate: 175.160.224.151
2023/09/23 21:25:26.859770 answer: recv resp[104]: proto.Response{Code:0, Msg:"ok"}
2023/09/23 21:25:31.470331 answer: Sending 'answer-695102175'
2023/09/23 21:25:31.470366 answer: message from DataChannel 'data': 'offer-1013426535'
2023/09/23 21:25:36.470028 answer: Sending 'answer-750781464'
2023/09/23 21:25:36.470123 answer: message from DataChannel 'data': 'offer-2065047193'
2023/09/23 21:25:41.469624 answer: Sending 'answer-2102723687'
2023/09/23 21:25:41.469978 answer: message from DataChannel 'data': 'offer-153497802'
2023/09/23 21:25:46.469606 answer: Sending 'answer-645051512'
2023/09/23 21:25:46.469883 answer: message from DataChannel 'data': 'offer-1287609150'
2023/09/23 21:25:51.470303 answer: Sending 'answer-1325372035'
2023/09/23 21:25:51.470421 answer: message from DataChannel 'data': 'offer-1486812657'
```


这次运行是在本地同一主机下运行的。你也可以将信令服务器搭建在公网主机上，然后将answer peer和offer peer分别放到不同的公有云虚机上，你看看是否依然可以连通！我在阿里云上的测试结果是ok的(信令服务器放在美国)。

注：示例中使用的stun server：74.125.137.127:19302实际上就是stun.l.google.com:19302。


## 4. 小结

通过本文的讲解和示例，我们看到：基于WebRTC数据通道可以实现低延迟的P2P实时通信。Go语言通过Pion等项目库提供了对开发WebRTC的支持。通过信令服务器协调Offer/Answer模型，可以建立起端到端的数据通道。未来WebRTC数据通道可用于更多像实时协同、远程控制等应用场景。

本文代码示例可在[这里](https://github.com/bigwhite/experiments/tree/master/webrtc-data-channel)下载。

注：本文示例仅是用作展示如何使用Go进行WebRTC应用的开发，对异常处理等方面并未做太多考虑，不要将示例代码用作生产环境。另外gorilla的websocket.Conn并非始终是goroutine safe的，示例中代码对websocket.Conn的保护并不那么充分。


## 5. 参考资料

[WebRTC for the Curious](https://webrtcforthecurious.com/)– https://webrtcforthecurious.com/[WebRTC: Real-Time Communication in Browsers](https://w3c.github.io/webrtc-pc/)– https://w3c.github.io/webrtc-pc/[WebRTC音视频实时互动技术](https://book.douban.com/subject/35543112/)– https://book.douban.com/subject/35543112/[WebRTC权威指南](https://book.douban.com/subject/26915289/)– https://book.douban.com/subject/26915289/[Learning WebRTC中文版-用WebRTC开发交互实时通信应用](https://book.douban.com/subject/26820574/)– https://book.douban.com/subject/26820574/[Real-Time Communication (RTC): The Ultimate Guide](https://www.agora.io/en/blog/real-time-communication-tools-for-online-messaging/)– https://www.agora.io/en/blog/real-time-communication-tools-for-online-messaging/[WebRTC加入了W3C和IETF标准](https://web.dev/webrtc-standard-announcement/)– https://web.dev/webrtc-standard-announcement/[Introduction to WebRTC protocols](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols)– https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Protocols[How Go-based Pion attracted WebRTC Mass – Q&A with Sean Dubois](https://webrtchacks.com/how-go-based-pion-attracted-webrtc-mass-qa-with-sean-dubois/)– https://webrtchacks.com/how-go-based-pion-attracted-webrtc-mass-qa-with-sean-dubois/[FOSDEM 2020: How can we make WebRTC Easier?](https://www.slideshare.net/SeanDuBois3/how-can-we-make-webrtc-easier)– https://www.slideshare.net/SeanDuBois3/how-can-we-make-webrtc-easier

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这篇文章不错，一直想用WebRTC建立p2p数据传输通道。