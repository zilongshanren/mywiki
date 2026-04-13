---
title: WebRTC第一课：从信令、ICE到NAT穿透的连接建立全流程
url: https://tonybai.com/2024/12/14/webrtc-first-lesson-how-connection-estabish/
published: '2024-12-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# WebRTC第一课：从信令、ICE到NAT穿透的连接建立全流程

![](../../assets/d6b2e580f15abae4.png)


[本文永久链接](https://tonybai.com/2024/12/14/webrtc-first-lesson-how-connection-estabish) – https://tonybai.com/2024/12/14/webrtc-first-lesson-how-connection-estabish

在上一篇文章《[WebRTC第一课：网络架构与NAT工作原理](https://tonybai.com/2024/11/27/webrtc-first-lesson-network-architecture-and-how-nat-work)》中，我们介绍了WebRTC的网络架构和NAT的基本概念，学习了WebRTC采用端对端（P2P）的通信模型，知道了NAT（网络地址转换）的概念以及给像WebRTC这样的直接P2P通信带来的挑战。

在实际的网络环境中，建立WebRTC这样的端到端连接的确并非易事。因此，在这篇文章中，我将继续上一篇文章的内容，全面探讨一下WebRTC连接建立的全流程，涵盖信令交换、ICE候选信息采集和选择、NAT穿透的各个关键步骤，希望能给大家理解WebRTC技术栈带去帮助。

## 1. WebRTC连接建立概览

在深入细节之前，我们先用一个时序图来概览WebRTC连接建立的主要步骤：

![](../../assets/a0da4f0bc49b23f4.png)


注：上图由

[mermaid]生成，对应的脚本在webrtc-first-lesson/part2/process-overview.mermaid。

这个过程可以概括为以下几个主要步骤：

- 信令交换：客户端通过信令服务器交换必要的连接信息，包括会话描述协议（SDP）数据。
- ICE候选收集：每个客户端收集可能的连接方式（称为ICE候选）。
- 候选交换：通过信令服务器交换ICE候选信息。
- 连通性检查：客户端尝试各种可能的连接方式。
- 建立P2P连接：选择最佳的连接路径，建立直接的端到端连接。

在这个过程中，我们会涉及到几个关键概念：

- 信令（Signaling）：用于协调通信并交换元数据的过程。
- ICE（Interactive Connectivity Establishment）：一种用于在各种网络情况下协助建立端到端连接的框架。
- NAT穿透（NAT Traversal）：克服网络地址转换带来的通信障碍的技术。

接下来，我们将详细探讨这些概念，并基于这些概念详细说明WebRTC建连的全流程。

我们先来看看信令(Signaling)。

## 2. 信令：WebRTC连接的基础

WebRTC技术栈中**唯一没有标准化的就是信令(Signaling)**，但信令却又是WebRTC连接的基础和必不可少的部分。

信令是WebRTC中用于协调通信过程的“指令”，它负责在对等端之间交换建立连接所需的元数据，但不会直接传输音视频数据。信令的主要作用包括：

- 交换会话描述协议（SDP）信息
- 交换网络配置信息（ICE候选）
- 协调会话的开始和结束
- 处理错误和会话状态变化

WebRTC本身并未定义信令协议标准，这主要考虑的是**信令的设计与实现依赖于具体应用的需求**，同时也有兼容性方面的考虑，比如：使WebRTC能够与现有的通信系统集成。在安全性方面，自定义信令也可以允许应用层来控制如何交换敏感信息。

目前用于WebRTC信令协议实现的常见方案主要包括基于WebSocket的自定义协议、SIP协议(Session Initiation Protocol)以及一些像XMPP(eXtensible Messaging and Presence Protocol)这样的成熟的即时通讯协议等。

就我个人而言，SIP和XMPP这样的传统协议都太重了，协议自身理解起来就有门槛！基于WebSocket的自定义协议，既简单又灵活，适合大多数业务不那么复杂的场景，在本文中，我们的信令协议就基于WebSocket自定义协议来实现。

Why Websocket？用WebSocket承载自定义信令协议的主要原因是**几乎所有现代浏览器和后端框架都支持WebSocket**，并且它是全双工通信，允许服务器和客户端随时发送消息，并且建立连接后，消息交换的开销也很小。

在设计信令语义时，我们通常会采用“Room”这个抽象模型来管理参与通信的客户端，这与WebRTC常用于互联网音视频应用不无关系。Room模型有助于组织和管理多个参与者，控制消息的广播范围，并可以实现更复杂的通信场景（如多人会议系统）。

下面是基于Room模型设计的信令交互的典型流程：

![](../../assets/2d6bab806651fc2f.png)


注：上图由

[mermaid]生成，对应的脚本在webrtc-first-lesson/part2/signaling-room-model-flow.mermaid。

下面对图中几个关键流程做一些简要说明：

- 房间创建

Client1向SignalingServer发送**创建房间**的请求，SignalingServer创建房间并返回房间ID给Client1。

- 客户端加入

Client2使用房间ID向SignalingServer发送**加入房间**的请求，SignalingServer通知Client1有新客户端加入。SignalingServer向Client2确认加入成功，并返回房间信息。重复相同的过程，Client3也如此加入了房间。

- WebRTC连接建立（以Client1和Client2为例）

Client1**创建Offer**并通过SignalingServer向Client2发送Offer，SignalingServer将Offer转发给Client2。Client2创建Answer，并通过SignalingServer向Client1转发Answer。之后，Client1和Client2还会以类似的方式互相交换ICE候选信息，通过SignalingServer进行转发。

注：offer是由发起者（通常是调用方）创建的SDP（Session Description Protocol）消息，表示希望建立的媒体会话的描述。answer是由接收者（通常是被叫方）回复的SDP消息，表示其对offer的响应。SDP中通常包含媒体格式、网络信息、编解码器等详细信息，供双方协商和确认，具体可参考我之前的文章《

[使用Go和WebRTC data channel实现端到端实时通信]》。

- 客户端离开(以Client2离开为例)

Client2向SignalingServer发送**离开房间**的请求，SignalingServer通知房间内的其他客户端（Client1 和 Client3）有客户端离开。

- 房间关闭

Client1（假设是房主）向SignalingServer发送**关闭房间**的请求。SignalingServer通知剩余的客户端（Client3）房间已关闭。

我们看到：这个流程展示了Room模型在WebRTC信令过程中的典型应用：

- Room作为一个逻辑单元，管理多个参与者之间的通信。
- SignalingServer负责转发所有的信令消息，包括房间管理消息和WebRTC相关的SDP和ICE候选信息。
- 客户端可以动态地加入和离开房间，SignalingServer会及时通知房间内的其他客户端。
- 房间可以由创建者（通常是第一个加入的客户端）来关闭。

由此来看，支持Room模型的信令服务器要支持房间创建、加入房间、转发Offer和Answer、离开房间、房间关闭等关键API。同时我们也能看出这种模型非常适合于实现多人音视频通话、在线教室、游戏大厅等应用场景，它提供了一种结构化的方式来管理复杂的多方实时通信。

有了信令服务器，WebRTC通信两端就可以交换元信息了，这其中就包含用于建立端到端通信的ICE候选信息。接下来，我们就来看看WebRTC端到端建连的关键流程：交互式连接建立(ICE, Interactive Connectivity Establishment)，以及这个过程中可能发生的NAT穿透。

## 3. ICE、NAT穿透与连接最终建立

ICE是一种用于在NAT（网络地址转换）环境中建立对等连接的协议，它允许两个agent（在[RFC8445](https://www.rfc-editor.org/rfc/rfc8445)中用AgentL和AgentR指代，如下图）发现彼此的**最佳通信路径**，进而完成端到端的连接。

![](../../assets/8a6cd7f1c4c92b51.png)



在这个过程中，我们还会涉及两个概念，一个是STUN(Session Traversal Utilities for NAT)服务器，一个是ICE Candidiate。

STUN服务器是帮助上述agent(AgentL和AgentR)发现其公网IP地址和端口的服务网元，这对于NAT穿透至关重要。而ICE Candidiate则是agent采集并与对端交换的、可能用于通信的潜在端点地址（IP地址和端口的组合）。

为了更直观的理解，下面我们来看一下通过ICE选择最佳通信路径的一般流程：

![](../../assets/70359d2f6b1e773e.png)


注：上图由

[mermaid]生成，对应的脚本在webrtc-first-lesson/part2/ice-protocol-sequence.mermaid。

在信令流程发起和转发Offer/Answer之后，两个端都会开启ICE最佳通信路径选择的流程。

### 3.1 ICE Candidate Gathering

这第一步就是**ICE Candidate Gathering**，即收集ICE候选者（端点）信息。

在这个过程中，每个agent收集可能的候选者类型包括如下几种：

- 主机候选者(Host Candidate)

主机候选者，即本地接口的地址。通过直接使用本地网络接口的IP地址和端口即可获得，比如：192.168.1.2:5000。

- 反射候选者(Server Reflexive Candidate)

反射候选者是通过STUN服务器查询公网IP地址和端口获得的，比如203.0.113.1:6000。

STUN通常是位于公网的一个服务器，比如最知名的公共stun是Google的“stun:stun.l.google.com:19302”。在收集反射候选者时，Agent(客户端)会向STUN服务器发送Binding Request（绑定请求），STUN服务器会响应一个Binding Response（绑定响应），其中包含客户端的公共IP地址和端口信息。

- 中继候选者(Relay Candidate)

中继候选者是通过TURN服务器(Traversal Using Relays around NAT)获得的端点地址（在上图中未显示），是在开启中继模式的情况下，由客户端向TURN服务器发送请求以获取中继地址。只有在WebRTC通信双方(AgentL和AgentR)无法直连的情况下(通常是NAT穿透失败导致的)，才会使用中继候选者，并通过TURN服务器进行数据中继来实现两端的数据通信。

注：在本文中，我们暂不考虑中继模式。


- 对端反射候选者（Peer Reflexive Candidates）

严格来说，对端反射候选者并非是在这个环节能获取到的候选者。对端反射是在ICE连接检查过程中动态发现的候选者，只有在连接检查过程中才能发现，且不太可预测，取决于网络拓扑和NAT行为。对比反射候选者，反射后选者是通过STUN服务器发现的。当一个端点向STUN服务器发送请求时，STUN服务器会回复该端点在公网上的IP地址和端口。而对端反射候选者是在两个端点尝试直接通信时发现的。当一个端点通过其已知的候选者（如主机候选者或反射候选者）向另一个端点发送数据时，如果成功到达，接收端会发现一个新的、之前未知的远程地址。这个新发现的地址就成为了对端反射候选者。

在ICE候选者信息收集的过程中，两端的Agent还要通过定期发送的STUN Binding请求，确保收集到的ICE反射/中继候选者信息在连接建立期间保持有效。这个过程在RFC 8445中被称为“Keeping Candidates Alive”，它可以帮助检测网络环境的变化，比如IP地址或端口的变化。通过定期的STUN请求，ICE可以确保候选者在NAT设备中的映射保持活跃，避免因长时间没有通信而被关闭。

### 3.2 Candidate Priorization

两端的Agent在收集完候选者信息后，会通过信令服务器交换他们收集到的候选者信息，这个流程在前面的信令交互流程图中也是有的，是信令协议要支持的功能的一部分。

一旦ICE Candidate Gathering以及candidate交换结束，两端的agent会对自己收集到的candidate以及收到的对端的candidate信息进行”Candidate Priorization”，即对自己收集到候选者集合和交换得到的对端候选者集合分别按优先级进行排序。

RFC8445中给出推荐的候选者的优先级公式如下：

```
priority = (2^24)*(type preference) +
(2^8)*(local preference) +
(2^0)*(256 - component ID)
```


在公式中有三个名词：type preference、local preference和component ID。下面分别介绍一下这三个名词的含义：

- type preference

Type preference一个表示候选者类型优先级的值。不同类型的候选者会被赋予不同的type preference值，以反映它们在ICE过程中的相对重要性。

它的取值范围通常是0到126之间的整数，值越大，优先级越高。 RFC8445中常见候选者类型及其推荐值如下：

```
主机候选者 (Host candidates): 126
反射候选者 (Server Reflexive candidates): 100
对端反射候选者 (Peer Reflexive candidates): 110
中继候选者 (Relay candidates): 0
```


通过不同类型的候选者的推荐值，我们也能看出：主机候选者 > 对端反射候选者 > 反射候选者 > 中继候选者。

注：Peer Reflexive candidates被赋予比Server Reflexive candidates更高的优先级，前面提过，是因为它不是在ICE候选者收集阶段就能发现的，而是在后面的连接检查阶段才能发现，因此可能代表更直接的连接路径。


- local preference

local preference是一个表示本地优先级的数值，其取值范围0~65535。这个值由本地ICE agent根据自己的策略来设置。

[RFC 8421（Guidelines for Multihomed and IPv4/IPv6 Dual-Stack Interactive Connectivity Establishment (ICE)）](https://www.rfc-editor.org/rfc/rfc8421)进一步补充了关于local preference的使用建议，特别是在多宿主和双栈（IPv4/IPv6）环境下。建议为IPv6候选地址分配比IPv4更高的local preference值，比如：IPv6地址可以分配65535（最高优先级），IPv4地址可以分配65535-1=65534（次高优先级）。在多宿主(Multihomed)环境中，可以根据网络接口的特性（如带宽、延迟、成本等）来分配不同的local preference值。

注：多宿主环境(Multihomed)指的是一个设备或系统通过多个网络接口连接到网络的情况。这些接口可以连接到同一个网络，也可以连接到不同的网络。多宿主环境下，每个网络接口都可能产生多个ICE候选者，需要为不同接口的候选者分配合适的优先级，可能需要考虑不同网络接口的特性（如带宽、延迟、成本）。


- Component ID

Component ID用于区分同一媒体流中的不同组件。在ICE中，一个媒体流可能包含多个组件，例如RTP和RTCP。Component ID通常是从1开始的连续整数。在公式中使用(256 – component ID)是为了确保值较小的component ID得到较高的优先级。RTP组件通常被赋值为1，RTCP组件(如果存在)通常被赋值为2。Component ID在优先级计算中的作用相对较小，主要用于在其他因素相同的情况下，为同一流的不同组件提供细微的优先级区分。

下面我们用一个示例来演示一下候选者计算优先级的过程。示例将展示一个ICE agent如何计算自己的candidates和对端candidates的优先级。我们假设这是一个音频流的情况，涉及RTP组件。假设我们有两个agent：AgentL和AgentR，我们将关注AgentL的视角。

AgentL的收集的候选者集合如下：

```
Host candidate (IPv4): 192.168.1.10:50000
Server Reflexive candidate: 203.0.113.5:50000
Relay candidate: 198.51.100.1:50000
```


AgentL通过信令交换获得的AgentR的候选者集合如下：

```
Host candidate (IPv6): 2001:db8::1:5000
Host candidate (IPv4): 192.168.2.20:5000
Server Reflexive candidate: 203.0.113.10:5000
```


上面优先级计算公式中各个参数值选择如下：

```
Type preferences:
- Host: 126
- Server Reflexive: 100
- Relay: 0
Local preferences:
- IPv6: 65535
- IPv4: 65534
Component ID: 1 (RTP)
```


下面是AgentL的候选者优先级的计算过程：

```
- Host (IPv4): (2^24) * 126 + (2^8) * 65534 + (256 - 1) = 658871
- Server Reflexive: (2^24) * 100 + (2^8) * 65534 + (256 - 1) = 658195
- Relay: (2^24) * 0 + (2^8) * 65534 + (256 - 1) = 655595
```


AgentR的候选者优先级（从AgentL的角度计算）计算过程：

```
- Host (IPv6): (2^24) * 126 + (2^8) * 65535 + (256 - 1) = 658881
- Host (IPv4): (2^24) * 126 + (2^8) * 65534 + (256 - 1) = 658871
- Server Reflexive: (2^24) * 100 + (2^8) * 65534 + (256 - 1) = 658195
```


最终优先级排序（从高到低）：

```
AgentR: Host (IPv6) - 658881
AgentR: Host (IPv4) - 658871
AgentL: Host (IPv4) - 658871
AgentR: Server Reflexive - 658195
AgentL: Server Reflexive - 658195
AgentL: Relay - 655595
```


这个优先级排序将用于指导下一阶段的ICE连接检查(ICE Connectivity Checks)顺序，但最终的连接选择还会考虑连接检查的结果。在实际场景中，可能会有更多的候选者，包括不同网络接口的多个Host候选者等等。

### 3.3 ICE Connectivity Checks

有了两端的候选者集合以及优先级值后，两个Agent就可以进入下一阶段ICE Connectivity Checks(连接检查)了。

连接检查实际也可以划分为三个阶段，我们逐一来看一下。

#### 3.3.1 确定角色(Determining Role)

在 WebRTC 的 ICE（Interactive Connectivity Establishment）连接过程中，角色的确定对于连接检查非常重要。ICE 的角色分为两种：控制方（Controlling）和被控方（Controlled）。这些角色用于决定在多个候选路径中选择哪一条作为最终的连接路径。控制方(Controlling Agent) 负责最终选择使用哪个候选对进行通信，而受控方(Controlled Agent)则需遵循控制方的决定。

在offer/answer的信令模型中，通常发起offer的一方会被指定为控制方，而应答(answer)的一方会成为受控方。有时可能会出现两个agents都认为自己是控制方的情况。ICE提供了解决这种冲突的机制：每个agent生成一个随机数(称为tie-breaker)，当发现冲突时，比较tie-breaker，tie-breaker较大的agent成为控制方。

ICE（Interactive Connectivity Establishment）连接检查是由控制方和被控方的两个ICE agent同时进行的。两者会各自发起连接检查，以确保双方能够建立有效的连接。控制方通过在检查中包含USE-CANDIDATE属性来提名(Nomination)候选对。

在某些情况下，角色可能会在ICE过程中切换，比如如果发现角色冲突并解决冲突后，又比如在ICE重启(restart)的特定场景下。

#### 3.3.2 形成检查列表(Forming checklist)

通信的双方，无论是控制端还是被控端都会独立形成自己的检查列表。

检查列表是所有可能的候选者对（Candidate Pair）的组合。让我们结合上面的示例，详细说明这个过程。

在我们的例子中，以AgentL为例，每个本地候选与每个远程候选会形成一对，这里会形成9个候选者对：

```
(L-Host, R-Host-IPv6)
(L-Host, R-Host-IPv4)
(L-Host, R-Server-Reflexive)
(L-Server-Reflexive, R-Host-IPv6)
(L-Server-Reflexive, R-Host-IPv4)
(L-Server-Reflexive, R-Server-Reflexive)
(L-Relay, R-Host-IPv6)
(L-Relay, R-Host-IPv4)
(L-Relay, R-Server-Reflexive)
```


根据之前计算的优先级，对候选对对优先级进行计算，并按从高到底进行排序。RFC8445中给出了候选者对优先级计算的公式：

```
// Let G be the priority for the candidate provided by the controlling agent.
// Let D be the priority for the candidate provided by the controlled agent.
pair priority = 2^32*MIN(G,D) + 2*MAX(G,D) + (G>D?1:0)
```


具体的计算过程这里就不体现了，排序后的检查列表可能如下：

```
(L-Host, R-Host-IPv6)
(L-Host, R-Host-IPv4)
(L-Server-Reflexive, R-Host-IPv6)
(L-Server-Reflexive, R-Host-IPv4)
(L-Host, R-Server-Reflexive)
(L-Server-Reflexive, R-Server-Reflexive)
(L-Relay, R-Host-IPv6)
(L-Relay, R-Host-IPv4)
(L-Relay, R-Server-Reflexive)
```


AgentR（被控方） 也会形成自己的检查列表，与AgentL类似，但AgentR并不主动选择最终的路径。

有了排序后的候选者对后，我们接下来便可以执行连接检查了，AgentL和AgentR会各自执行自己的检查。

#### 3.3.3 执行连接检查(Performing Connectivity Checks)

我们以AgentL为例，看看执行连接检查的主要步骤。

AgentL开始按照检查列表的顺序(优先级由高到低)发送STUN Binding请求:

- AgentL向R-Host-IPv6发送STUN Binding请求；
- 如果第一个检查失败或超时，AgentL会继续向第二个候选者对的R-Host-IPv4发送STUN Binding请求；
- 如果失败，继续下一个候选对…，依次类推

同时，AgentR也会执行类似的过程，按照他自己的检查列表发送自己的STUN Binding请求。

当AgentL收到STUN Binding响应时，可能有以下几种可能：

- 如果是成功的响应，这个候选对被标记为有效。
- 如果响应来自一个未知地址，创建一个新的Peer Reflexive候选。

之后，AgentL便会更新候选列表，将新候选与所有远程候选配对，形成新的候选对，并根据ICE优先级算法重新排序检查和更新检查列表。AgentL还可能对新形成的候选对立即开始连接性检查。

#### 3.3.4 NAT穿透与最终候选路径的形成

如果两端都在NAT后面，那么**Peer Reflexive候选者就是NAT穿透的关键**！我们结合下图详细说说ICE过程是如何一步步的选出由新发现的Peer Reflexive组成的最终候选路径的。

![](../../assets/f743578e4037cf31.png)


注：上图由

[mermaid]生成，对应的脚本在webrtc-first-lesson/part2/ice-nat-traversal-sequence.mermaid

图中使用A、B作为两个端点，通过stun服务器获取的反射候选为A’和B’，通过连接检查阶段发现的对端反射候选(Peer Reflexive)分别为A”和B”。接下来，我们详细说明一下图中流程。

- ICE候选收集阶段

端点A和B都收集主机候选。A和B都通过各自的NAT向STUN服务器发送请求，获取服务器反射候选（A’和B’）。

- 候选交换

A和B交换各自的候选列表，包括主机候选和反射候选（A’和B’）。

- 连接检查开始

A向B的反射候选B’发送STUN绑定请求，这个请求经过A的NAT和B的NAT。

B收到请求后，发现源地址（A”）与A提供的候选(A’)不匹配，因此创建一个新的Peer Reflexive候选A”。

B通过NAT链回复STUN绑定响应。

A收到响应后，从响应中的XOR-MAPPED-ADDRESS字段获知并创建自己的Peer Reflexive候选A”。

注：STUN协议中的XOR-MAPPED-ADDRESS字段可用于帮助对等方（peer）在ICE连接检查阶段找到自己的Peer Reflexive地址。


- B也向A发送STUN绑定请求

类似的过程在反向发生。A创建B的Peer Reflexive候选B”。B从A的响应中获知并创建自己的Peer Reflexive候选B”。

- 更新候选对和继续检查

A和B都更新各自的检查列表，包括新的(A”, B”)对。

- 选择最佳路径

最终，(A”, B”)被选为最佳路径，实现双向NAT穿透。

一旦选定了最佳候选者对，ICE过程就结束了，可以开始实际的数据传输。

### 3.4 ICE重启

最后我们简单说说ICE重启(restart)。ICE restart提供了一种在不中断现有应用会话的情况下重新建立和优化网络连接的机制。这通常是因为网络条件发生了变化或者需要切换到更优的连接路径。下面序列图展示了ICE重启的基本流程：

![](../../assets/955402ce887eec30.png)


注：上图由

[mermaid]生成，对应的脚本在webrtc-first-lesson/part2/ice-restart-sequence.mermaid

ICE restart可能由多种原因触发，如网络变化、切换到更优路径、或解决连接问题。任何一方都可以发起ICE restart。

和前面的ICE流程不同之处在于重启时，发起restart的一方会生成新的ICE ufrag和password。这些新的凭证用于区分新的ICE会话和旧的会话。

之后的流程就和正常的ICE交互选出最优通信路径没有太大区别了！这里也就不重复说明了。

注：ICE restart不一定会改变控制方（controlling）和受控方（controlled）的角色。通常情况下，原有的角色分配会被保持。


## 4. 小结

在这篇文章中，我们深入探讨了WebRTC连接建立的全流程，涵盖了以下关键概念：

- 信令：我们讨论了信令的重要性，并了解了基于Room抽象的常见的信令服务器模型；
- ICE框架：我们学习了ICE候选信息的收集、交换以及连接检查；
- NAT穿透：我们在ICE连接检查过程中，详细说明了ICE是如何实现NAT穿透并选出最终最优的通信路径的。

在实际生产应用中，我们可能还需要考虑以下几点：

- 连接建立优化：可以通过使用ICE Lite、预先收集候选信息等方式来加速连接建立过程。
- 安全性考虑：在生产环境中，应该使用HTTPS和WSS来保护信令通道。
- 错误处理和重连：实际应用中需要处理各种可能的错误情况，并实现自动重连机制。

在接下来的系列文章中，我将用一个相对完整的演示示例来展示WebRTC应用端到端建连的所有细节(通过TRACE级别日志)，希望通过这些细节的分析能帮助大家更好地理解WebRTC的建连过程。

本文涉及的Mermaid源码在[这里](https://github.com/bigwhite/experiments/blob/master/webrtc-first-lesson/part2)可以下载到 – https://github.com/bigwhite/experiments/blob/master/webrtc-first-lesson/part2

## 5. 参考资料

[WebRTC 1.0: Real-time Communication Between Browsers](https://www.w3.org/TR/webrtc/)– https://www.w3.org/TR/webrtc/[Interactive Connectivity Establishment (ICE)](https://tools.ietf.org/html/rfc8445)– https://tools.ietf.org/html/rfc8445[Session Traversal Utilities for NAT (STUN)](https://tools.ietf.org/html/rfc8489)– https://tools.ietf.org/html/rfc8489[Traversal Using Relays around NAT (TURN)](https://tools.ietf.org/html/rfc8656)– https://tools.ietf.org/html/rfc8656

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