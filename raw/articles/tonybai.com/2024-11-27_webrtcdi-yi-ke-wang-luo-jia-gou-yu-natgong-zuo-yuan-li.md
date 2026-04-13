---
title: WebRTC第一课：网络架构与NAT工作原理
url: https://tonybai.com/2024/11/27/webrtc-first-lesson-network-architecture-and-how-nat-work/
published: '2024-11-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# WebRTC第一课：网络架构与NAT工作原理

![](../../assets/65cf11f55a5473a4.png)


[本文永久链接](https://tonybai.com/2024/11/27/webrtc-first-lesson-network-architecture-and-how-nat-work) – https://tonybai.com/2024/11/27/webrtc-first-lesson-network-architecture-and-how-nat-work

2023年下旬，[OpenAI与Livekit的合作](https://blog.livekit.io/open-source-realtime-multimodal-ai/)在科技圈引起了不小的轰动。这两家公司联手，通过WebRTC技术和大型语言模型（LLM）的结合，[使AI模型具有了看、听和说话的能力](https://openai.com/index/chatgpt-can-now-see-hear-and-speak/)。这一举动不仅彰显了WebRTC在现代通信技术中的重要地位，也为我们揭示了AI与实时通信融合的无限可能。WebRTC技术在大流行后再一次进入技术人的视野，恰好在我们今年打造的产品中，WebRTC也是技术栈的核心。

在去年9月份，我写了一篇WebRTC入门科普的文章：[使用Go和WebRTC data channel实现端到端实时通信](https://tonybai.com/2023/09/23/p2p-rtc-implementation-with-go-and-webrtc-data-channel)，在那篇文章中，我对WebRTC技术做了一些概述说明，并通过一个基于Go语言的实例，展示了如何实现端到端的实时通信。大家可以通过那篇文章了解**WebRTC技术的基础概念和核心架构**。

WebRTC端到端实时通信的效果主要取决于两个重要因素，一个**通信质量**，一个是**音视频编解码质量**。对于入门类文章来说，改进通信质量或音视频编解码质量还为时尚早，我们亟需了解的是其背后的原理。

在这篇文章以及后续的几篇文章中，我们先来关注一下“WebRTC网络通信”。我们会先了解一下WebRTC网络架构，然后对WebRTC中的难点，诸如NAT打洞、基于信令与ICE的建连等做深入分析。

在这篇文章中，我们先来学习NAT的工作原理，探讨不同类型的NAT网络行为是如何影响点对点通信的，为后续理解WebRTC的NAT打洞(也称为NAT穿透)和端到端建连做准备。

## 1. WebRTC网络架构

我们知道WebRTC（Web Real-Time Communication）是一种支持网页浏览器/应用进行端到端实时语音对话或视频对话的技术，其中支持端到端建立连接和后续数据传输的网络架构是十分重要的，这也是理解WebRTC技术栈的一个重点。下面是WebRTC网络架构图的示意图：

![](../../assets/4afbc55b3c839b21.png)


这个架构包含以下主要组件：

-
浏览器/App：这是进行WebRTC的端(Peer)，可以是浏览器，也可以是App。WebRTC API在浏览器中实现，使得web应用能够直接访问媒体设备和建立点对点连接。App也可以利用WebRTC的实现(比如

[Pion](https://github.com/pion/webrtc))与对端进行RTC通信。 -
信令服务器(Signaling Server）：虽然不是WebRTC标准的一部分，但对于WebRTC建立连接至关重要，任何non-trivial的基于WebRTC的系统都会有专属的信令服务器，它会帮助通信双方交换会话描述协议（SDP）信息和ICE候选地址。这个在

[使用Go和WebRTC data channel实现端到端实时通信](https://tonybai.com/2023/09/23/p2p-rtc-implementation-with-go-and-webrtc-data-channel)一文中介绍过，在后续的文章中还会有系统说明。 -
STUN服务器（Session Traversal Utilities for NAT）：该服务器可以帮助客户端发现自己的公网IP地址和端口，这个服务器是NAT打洞时所必须的。

-
TURN服务器（Traversal Using Relays around NAT）：当通过常规方式点对点连接失败时(通常是NAT打洞失败)，可以使用TURN服务器作为媒体数据的中继服务器使用。两端发送的数据都会要通过TURN的中继才能转发给对端。

-
ICE框架（Interactive Connectivity Establishment）：综合使用各种NAT打洞技术来协助两端建立连接，这个我们会在后面文章中系统说明。


我们看到这个架构略有些复杂，但该架构允许WebRTC应用在复杂的网络环境中建立直接的点对点连接，即使**客户端位于NAT或防火墙后面**。

## 2. 网络世界的真相：我们都在NAT后面

在理想的网络世界中，每个设备都有一个唯一的公网IP地址，可以直接相互连接和通信。这种理想状态下，网络是完全开放和对等的，没有任何障碍阻止设备之间的直接交互。

但现实情况却很骨感，出于IPv4地址空间的限制(IPv4地址的数量不够了)、网络管理以及网络安全的考虑，大多数设备都隐藏在NAT(网络地址转换)后面。

NAT（网络地址转换）技术于1994年由Egevang等人在[RFC 1631](https://datatracker.ietf.org/doc/html/rfc1631)中提出，旨在作为缓解IPv4地址不足问题的临时技术方案。通过将私有IP地址和端口映射到公共IP地址和端口，NAT使得在私有网络中的设备可以使用公共地址(共享一个或多个)访问互联网。

![](../../assets/24f97545ac10a251.png)



这种技术的出现大大缓解了IPv4地址的紧张状况，并成为当时乃至现在(IPv6的推广与使用未及预期)网络地址管理的重要手段。不过，NAT技术的广泛应用也意味着大部分设备只有**私网IP**，无法从外网直接访问，这一定程度上限制了端到端的直接通信。另外，由于不同类型的NAT行为有所不同，进一步增加了端到端网络连接的复杂性。

注：私网IP地址是指在局域网（LAN）中使用的IP地址，这些地址不能在公共互联网(公网)中被路由。私网IP地址主要用于内部网络中设备之间的通信，通常用于家庭、企业或组织的网络。根据IETF的标准，私网IP地址的范围包括(以CIDR（无类域间路由）格式表示)：10.0.0.0/8、172.16.0.0/12和192.168.0.0/16。


于是便有了NAT打洞技术(NAT hole punching)。NAT打洞技术为在NAT环境中实现设备间直接通信提供了一种有效的解决方案，它允许位于不同NAT后面的设备建立直接的点对点（P2P）连接，而无需手工配置端口转发。在P2P文件共享、VoIP通信、在线游戏、即时通信以及视频会议系统等领域，NAT打洞都有着广泛的应用。

不过，要理解NAT打洞，我们需要要先得弄清楚NAT的工作原理、主要的NAT类型以及它们的行为差异。

## 3. NAT的工作原理与主要类型的行为差异

我们先来看看NAT工作原理。

### 3.1 NAT的工作原理

网络地址转换（NAT）的核心工作原理还是比较好理解的，就是在请求数据包通过NAT设备时修改其源IP和源端口信息。以下图为例，即将内网主机通过X1:x1发往外网主机Y1:y1的网络请求中的源IP和源端口从X1:x1修改为X1′:x1′后，再发给目的端点(Y1:y1)。NAT设备会维护一个映射表(也叫会话表)，记录X1:x1与X1′:x1′的映射关系。当请求的应答包回来时(Y1:y1 -> X1′:x1′)，NAT设备将根据映射表将X1′:x1′再替换回X1:x1，这样应答包就可以正常回到X1:x1了。

![](../../assets/371c3de875be460e.png)


为了管理资源(每个NAT的对外端口数量有限)，NAT设备会内置超时机制，它会为每个会话/映射设置一个生存时间（TTL）。如果在TTL内没有新的数据包，这个映射会被删除。

随着NAT技术的演进，同时考虑到网络管理和网络安全因素，NAT设备出现了不同的映射表管理方式，与之相对应的就出现了不同的NAT类型与行为特征。接下来，我们就来看看NAT的主要类型、映射表的管理方式以及它们的行为差异。

注：NAT打洞的主流方式是通过UDP包，因此下面的关于NAT类型和行为的描述都是基于UDP的。UDP是面向数据报的传输层协议，相对于面向连接的TCP，它更加灵活，延迟更低，在实时性要求更高的场景，比如视频会议、语音通信等。


### 3.2 NAT的主要类型

根据2003年[RFC 3489](https://datatracker.ietf.org/doc/html/rfc3489)中对市面上NAT实现类型的归纳，NAT可以分为完全锥形(Full Cone)、受限锥形(Restricted Cone)、端口受限锥形(Port Restricted Cone)和对称型(Symmetric)四种主要类型。下面我们分别来说一下这四种类型的NAT映射表构成以及行为特征。

#### 3.2.1 完全锥型NAT

完全锥型是最宽松的NAT类型，它在NAT映射表中只存储了一个四元组：(内网ip(internal_ip), 内网端口(internal_port), 映射ip(external_ip), 映射端口(external_port))。我们看下图中的完全锥形类型的NAT：：

![](../../assets/f97c06f34945a248.png)


在上图中，内部地址X1:x1被映射到了外部地址E:x1′，所有从X1:x1发到外部的数据都由E:x1′向外发送。相应的外部应答(比如: Y1:y1 -> E:x1′)的流量会在NAT设备上被转换回到X1:x1的流量。

那么为什么这个类型的NAT会被称为完全锥形呢？这就要从NAT设备对外部流量的限制来说了。对于NAT设备来说，一旦建立了X1:x1->E:x1′的映射规则，就好比**X1在该NAT设备上“打了一个洞”**，内部来自X1:x1的流量可以从该洞发送出去，但**NAT设备是否允许外部流量从该洞回到X1:x1以及允许哪些流量从该洞返回到X1:x1就决定了该NAT的类型**。

如果任何外部主机都可以通过上面的洞E:x1′向内部主机X1:x1发送数据包，那么这个NAT就是完全锥形。我们再用一副示意图来说明一下完全锥形NAT的行为特点：

![](../../assets/229ac111921507c6.png)


这里故意将右侧的外部主机排列成像圆锥的形状，位于锥子范围内的所有主机都能通过图中的“洞”将数据包发到内部主机X1:x1上。

很显然完全锥形NAT虽然管理简单，也具有很好的开放性，但它在安全性上较弱，外部很容易利用NAT上的洞向内部主机上的服务发起攻击。

为此，后面的几种NAT都是为了增强NAT安全性的，而且一个比一个更严格，我们先来看受限锥形NAT。

#### 3.2.2 受限锥型NAT

受限锥形NAT又被称为**IP受限锥型NAT**，它在完全锥形NAT的映射表的基础上，增加了“IP白名单(如下图中的allowed_external_ips)”，下面是受限锥形NAT的示意图：

![](../../assets/f64f7b846b86f362.png)


我们看到：X1主机通过X1:x1在向Y1:y1和Y2:y2分别发起请求后，NAT设备上便有了一条映射规则(一个洞)：X1:x1被映射到了外部地址E:x1′，但映射表也记录了两个请求的目标主机的IP，记录在规则的allowed_external_ips中。

规则中的这个allowed_external_ips对后续外部主机通过E:x1′向X1:x1发送数据包会做出限制，如下图：

![](../../assets/76a72d77ab45a4dc.png)


我们看到：只有在“白名单”中的IP对应的主机（如Y1、Y2）才可以在“洞”建立后，通过E:x1′向内部主机X1:x1成功发送数据包，其它主机发送的数据包都会被拦截和丢弃。

我们看到上述的限制是限制是基于IP地址的，而位于Y1和Y2上的服务，可以使用任意端口向E:x1′成功发送数据包，这显然也是一个安全隐患。于是便有了下面限制更为严格的端口受限锥形NAT。

#### 3.2.3 端口受限锥型NAT

端口受限锥型NAT在受限锥形NAT映射表的基础上，又进一步限制了端口，通过allowed_external_endpoints实现对外部端点的限制，如面示意图：

注：IP:port合在一起称为一个端点(endpoint)。


![](https://tonybai.com/wp-content/uploads/webrtc-first-lesson-network-architecture-and-how-nat-work-9.png)


我们看到：X1主机通过X1:x1在向Y1:y1和Y2:y2分别发起请求后，NAT设备上便有了一条映射规则(一个洞)：X1:x1被映射到了外部地址E:x1′，映射表同时记录了两个请求的目标主机的端点(ip:port)，记录在规则的allowed_external_endpoints中。

规则中的这个allowed_external_pointss对后续外部主机通过E:x1′向X1:x1发送数据包会做出更严格的限制，如下图：

![](../../assets/5cc62196e9d27c97.png)


我们看到：只有在“allowed_external_endpoints”中的端点（如Y1:y1、Y2:y2）发起的请求才可以在“洞”建立后，通过E:x1′向内部主机X1:x1成功发送数据包，其它主机或Y1、Y2上其他端口发送的数据包都会被拦截和丢弃。

下面我们再来看看最严格的NAT类型：对称型NAT。

#### 3.2.4 对称型NAT

和上面由X1:x1发出的数据包(无论目的端点是什么)在NAT上只建立一条映射规则不同，在对称型NAT中，由X1:x1向不同端点发送数据会在NAT上建立多条映射规则，如下图所示：

![](../../assets/2cb85bdd72038477.png)


我们看到每条规则中还包含了目的端点的信息(dest_ip和dest_port)，也正因为如此，对称型NAT对外部请求的限制也是最严格的，如下图所示：

![](https://tonybai.com/wp-content/uploads/webrtc-first-lesson-network-architecture-and-how-nat-work-12.png)


我们看到：只有来自规则中dest_ip和dest_port组成的端点的数据包才能进入内部，即**只有那些收到数据的外部主机才能够“顺原路返回”地回送数据**。

### 3.3 新的分类

上面提到的四种NAT类型是stun的RFC在早期对NAT实现的分类(基于UDP传输)，一直沿用至今，也是目前使用最多的一种分类方法。不过这种分类方法将NAT的两个正交的行为混在一起说了，即分配行为Assignment Behavior和过滤行为Filtering Behavior。其实我们更多关注的使其过滤行为的特征。

在较新的[RFC 4787](https://datatracker.ietf.org/doc/html/rfc4787)中，NAT的行为被细分为两个独立的维度：**分配行为**（Assignment Behavior）和**过滤行为**（Filtering Behavior）。这两种行为的各自分类描述了NAT在处理映射和过滤时的不同方式。以下是这两种行为的分类及其对应的早期NAT类型的对照。

#### 3.3.1 分配行为（Assignment Behavior）

分配行为定义了NAT设备如何为内网设备的流量分配外部端口和地址。RFC 4787将其分为三类：

- Endpoint-Independent Mapping（端点独立映射）

不管内网设备与哪个外部设备通信，只要内网设备使用同一个源IP和源端口，NAT都会为其分配相同的外部IP和端口。这意味着内网设备的源IP和源端口在外部网络上呈现为固定的外部IP和端口组合，独立于目标设备的地址和端口，即独立于目标设备的端点。

端点独立映射这种类别对应的早期NAT类型是完全锥形NAT（Full Cone NAT），前面我们讲过，在完全锥形NAT中，无论内网设备的通信目标是什么，NAT设备都会使用相同的外部端口映射，因此完全符合端点独立映射的定义。

- Address-Dependent Mapping（地址依赖映射）

在地址依赖映射中，内网设备的外部端口是根据其通信的目标IP地址来分配的。如果内网设备改变了目标IP地址，即使源IP和源端口不变，NAT设备也会为其分配一个新的外部端口。

在分配行为上，我们似乎无法找到与早期分类一模一样的类型，它有些类似于对称NAT，但对称NAT不仅考虑目标IP，还考虑目标端口。

- Address and Port-Dependent Mapping（地址和端口依赖映射）

在这种映射行为中，内网设备的外部端口是根据其通信的目标IP地址和目标端口组合来分配的。如果内网设备改变了目标IP或端口，即使源IP和源端口不变，NAT设备仍会分配一个新的外部端口。该类型对应的是早期NAT类型中的对称NAT（Symmetric NAT）。对称NAT的行为正是基于目标IP和端口的组合来分配外部端口，因此它完全符合地址和端口依赖映射的定义。

#### 3.3.2 过滤行为（Filtering Behavior）

过滤行为描述了NAT设备如何决定是否允许外部设备通过NAT与内网设备通信。RFC 4787将其分为三类：

- Endpoint-Independent Filtering（端点独立过滤）

这种类型的NAT设备不考虑外部设备的地址或端口，只要内网设备先发起了一个会话，任何外部设备都可以通过NAT设备与内网设备的相同源IP和源端口通信。这和早期NAT类型中的完全锥形NAT完全契合。

- Address-Dependent Filtering（地址依赖过滤）

这种类型的NAT设备只允许内网设备已经与之通信的外部IP地址与其通信。换句话说，只有内网设备先与某个特定的外部IP地址通信后，该外部IP地址的设备才能通过NAT与内网设备通信。这和早期NAT类型中的限制锥形NAT（Restricted Cone NAT）在过滤行为的特征上是一致的。

- Address and Port-Dependent Filtering（地址和端口依赖过滤）

这种类型的NAT设备要求外部设备的IP地址和端口都与内网设备已经建立连接的目标IP地址和端口匹配，才能允许通信。这意味着，只有内网设备先与某个特定的外部IP和端口组合通信后，该组合才能与内网设备通信。这与早期NAT类型中的端口限制锥形NAT（Port Restricted Cone NAT）以及对称NAT的行为特征是一致的。

可以看出，RFC 4787中的分类方法更为细致地将NAT的分配行为和过滤行为分开讨论，使得对NAT的行为理解更加明确。这种分类不仅帮助理解了不同NAT类型的工作机制，也为更精确地描述NAT行为提供了标准化的术语。

当然对于NAT打洞来说，我们**更关心的显然是过滤行为**。

## 4. 小结

好了，这篇文章到这里就告一段落了。

在这篇文章中，我们探讨了WebRTC网络架构和NAT的工作原理。

我们首先了解了WebRTC的网络架构，包括信令服务器、STUN服务器、TURN服务器和ICE框架等组件和其作用。

然后，我们讨论了为什么需要NAT，包括解决IPv4地址短缺、提高安全性和简化网络管理等原因。

接着，我们详细解释了NAT的工作原理，以及完全圆锥型、受限圆锥型、端口受限圆锥型和对称型这四种主要的早期NAT类型。

最后，我们介绍了RFC 4787中对NAT行为的新分类方法，将NAT行为分为分配行为和过滤行为两个维度。

了解WebRTC网络架构以及NAT工作原理是理解NAT打洞机制以及WebRTC端到端建立连接过程的前提，在后续文章中，我们会继续WebRTC网络部分的内容，比如NAT打洞以及端到端建连过程。

## 5. 参考资料

[How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works)– https://tailscale.com/blog/how-nat-traversal-works[Implementing NAT Hole Punching with QUIC](https://arxiv.org/abs/2408.01791)– https://arxiv.org/abs/2408.01791[Network Address Translation (NAT) Behavioral Requirements for Unicast UDP](https://tools.ietf.org/html/rfc4787)– https://tools.ietf.org/html/rfc4787[WebRTC 1.0: Real-time Communication Between Browsers](https://www.w3.org/TR/webrtc/)– https://www.w3.org/TR/webrtc/[Interactive Connectivity Establishment (ICE): A Protocol for Network Address Translator (NAT) Traversal](https://datatracker.ietf.org/doc/html/rfc8445)– https://tools.ietf.org/html/rfc8445[Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5389)– https://datatracker.ietf.org/doc/html/rfc5389[Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN)](https://datatracker.ietf.org/doc/html/rfc5766)– https://datatracker.ietf.org/doc/html/rfc5766[Traditional IP Network Address Translator (Traditional NAT)](https://datatracker.ietf.org/doc/html/rfc3022)– https://datatracker.ietf.org/doc/html/rfc3022[IP Network Address Translator (NAT) Terminology and Considerations](https://datatracker.ietf.org/doc/html/rfc2663)– https://datatracker.ietf.org/doc/html/rfc2663

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论