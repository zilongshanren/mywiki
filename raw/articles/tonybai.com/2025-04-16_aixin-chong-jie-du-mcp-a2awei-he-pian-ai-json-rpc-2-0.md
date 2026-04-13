---
title: AI新宠？解读MCP、A2A为何偏爱JSON-RPC 2.0
url: https://tonybai.com/2025/04/16/ai-protocol-prefer-jsonrpc/
published: '2025-04-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# AI新宠？解读MCP、A2A为何偏爱JSON-RPC 2.0

![](../../assets/fb618aef92e25324.png)


[本文永久链接](https://tonybai.com/2025/04/16/ai-protocol-prefer-jsonrpc) – https://tonybai.com/2025/04/16/ai-protocol-prefer-jsonrpc

大家好，我是Tony Bai。

在AI技术飞速演进的今天，底层通信协议的选择对系统效率和互操作性至关重要。细心的开发者可能已经发现，新兴的AI协议如[模型上下文协议（MCP）](https://modelcontextprotocol.io/)和[Agent2Agent（A2A）](https://github.com/google/A2A)协议，都不约而同地将目光投向了** JSON-RPC 2.0**。这并非巧合，而是一个深思熟虑的技术选型。在这篇文章中，我将和大家一起看看JSON-RPC 2.0的

**起源、核心规范以及历史应用**，并解读这个10多年前定义的“老协议”为何能在AI时代能再次获得青睐。

## 1. JSON-RPC 2.0：起源与核心规范

JSON-RPC协议的诞生，源于对早期RPC协议（如[XML-RPC](http://xmlrpc.com/)、[SOAP](https://tonybai.com/2019/01/08/go-and-soap)）复杂性的反思，旨在提供一种**更轻量、更简洁**的远程过程调用机制。其2.0版本规范（基于2009年草案，正式发布于2010年左右）更是将这一理念发扬光大。其核心设计哲学正如规范开篇所言：**“It is designed to be simple!”**

很多开发者日常都是用过JSON-RPC 2.0，但可能没有对其规范做过深入的了解，借此篇文章机会，让我们依据其官方规范，深入了解其关键特性。。

### 1.1 核心原则

我们先来看一下JSON-RPC协议设计的几个核心原则。

**Stateless (无状态):**每次请求都是独立的，服务器不保存客户端状态。**Light-weight (轻量级):**协议开销小，消息体紧凑。**JSON Data Format (JSON数据格式):**使用广泛流行、易于解析和人类可读的JSON([RFC 4627](http://www.ietf.org/rfc/rfc4627.txt)) 作为数据交换格式。**Transport Agnostic (传输无关):**协议本身不限定网络传输方式，可在HTTP、[WebSocket](https://tonybai.com/2019/09/28/how-to-build-websockets-in-go/)、TCP、甚至进程内等多种环境使用。

接下来，我们再来看一下工作原理。JSON-RPC 2.0是一个相对简单的协议，其规范也就几页，因此其工作原理也非常好理解。

### 1.2 工作原理

JSON-RPC 的工作原理是向实现此协议的服务器发送请求。在这种情况下，客户端通常是打算调用远程系统的单个方法的软件。多个输入参数可以作为数组或对象传递给远程方法，而方法本身也可以返回多个输出数据（这取决于实现的版本。）

![](../../assets/72061d058162d378.jpg)


下面是对协议中的一些核心对象的解读。

#### 1.2.1 **Request Object (请求对象)**

Request Object是发起RPC调用的核心，由客户端发送请求到服务端。我们结合一个示例来理解请求对象的各个字段的含义：

```
--> {"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}
<-- {"jsonrpc": "2.0", "result": 19, "id": 4}
```


- jsonrpc: 必须是”2.0″，这是区分版本的关键标识。
- method: 是一个字符串类型的必选字段，表示要调用的方法名。以rpc.开头的为保留方法。
- params: 是一个可选参数，它是一个结构化值Array或Object，包含调用方法所需的参数。

JSON-RPC支持两种传递params的方式，一种是**By-name(按名称)**，即params是一个对象，其成员名与服务器期望参数名匹配，比如上面示例中params使用的就是一个by-name的参数传递方式。另外一种是**By-position (按位置)**，即params是一个数组，值按服务器期望顺序排列。比如上面示例中params等价为下面按位置传递方式的params：

```
{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}
```


- id: 是一个字符串或数字类型的值，用于关联请求和响应。比如上面示例中，请求的id=4，其对应的响应(Response)的id也应该为4才能匹配成功。

#### 1.2.2 **Response Object (响应对象)**

上面的示例中的第二行其实是一个Repsonse Object，即服务器针对有效请求（非通知类）的回复：

```
<-- {"jsonrpc": "2.0", "result": 19, "id": 4}
```


- jsonrpc: 必须是”2.0″，这是区分版本的关键标识。
- result: 包含方法调用的成功结果。如果rpc调用失败，那么响应中不有result字段，可以说与下面的error是二取一的。
- error: 包含一个Error Object。如果rpc调用没有错误发生，响应体中不应该存在error字段。
- id: 与对应请求对象中的id一致。如果检测请求id出错(比如解析出错或非法请求)，则应为Null，比如下面这个示例：

下面是返回错误码的示例：

```
--> {"jsonrpc": "2.0", "method": 1, "params": "bar"} // method值不是字符串，不是一个合法的请求对象
<-- {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}
```


再强调一下：**result 和 error 成员互斥，必须存在其一。**

#### 1.2.3 **Error Object (错误对象)**

错误对象用于描述发生的错误，对象有三个字段：

- code: 错误码，类型为整数，指示错误类型。
**-32768到-32000**为预定义错误码范围。下面是一些典型错误code：- -32700: Parse error
- -32600: Invalid Request
- -32601: Method not found
- -32602: Invalid params
- -32603: Internal error
- -32000 to -32099: Server error

- message: 错误信息，字符串类型，用于简短描述错误。
- data: 可选，代表原始值或结构化值，包含额外错误信息。

下面是一个错误对象示例：

```
--> {"jsonrpc": "2.0", "method": "foobar", "id": "1"}
<-- {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "1"}
```


#### 1.2.4 Notification通知

Notification通知一种特殊的Request，它**没有id成员**。表示客户端不关心响应，服务器也不用回复，适用于无需确认的操作。比如下面这个示例：

```
--> {"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}
```


也就是说当一个合法的Request中没有id，则可以认为是Notification通知。

#### 1.2.5 Batch批量调用

Batch批量调用是指客户端可能发送一个包含多个Request对象的数组，以实现批量处理。服务器应该返回一个包含对应Response对象的数组（通知除外）。请求处理和响应返回**可以是无序的**，客户端通过id匹配。下面是一个批量调用的示例：

```
--> [
{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},
{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
{"jsonrpc": "2.0", "method": "subtract", "params": [42,23], "id": "2"},
{"foo": "boo"},
{"jsonrpc": "2.0", "method": "foo.get", "params": {"name": "myself"}, "id": "5"},
{"jsonrpc": "2.0", "method": "get_data", "id": "9"}
]
<-- [
{"jsonrpc": "2.0", "result": 7, "id": "1"},
{"jsonrpc": "2.0", "result": 19, "id": "2"},
{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null},
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "5"},
{"jsonrpc": "2.0", "result": ["hello", 5], "id": "9"}
]
```


## 2. JSON-RPC的“前世今生”：应用场景

自诞生以来，JSON-RPC凭借其**简洁、轻量、易于实现和跨语言**的特性，在多个领域得到了广泛应用，满足了开发者对“高效”通信的需求：

**Web APIs:**作为RESTful API的一种替代或补充，尤其是在需要明确“过程调用”语义的场景。**微服务架构:**服务间的内部通信，特别是在追求低延迟、简单交互的场景下，比HTTP REST更轻量。**消息队列(Message Queues):**作为消息体格式，在基于消息队列的异步任务处理系统中定义任务和传递结果。**桌面应用与Web端交互:**例如，本地应用通过WebSocket与网页前端进行双向通信。**物联网(IoT):**资源受限设备间的通信，其轻量特性非常适合。**区块链节点通信:**一些区块链项目使用JSON-RPC作为节点间或客户端与节点间交互的标准接口。

这些应用场景充分证明了JSON-RPC作为一种基础通信协议的**普适性和生命力**。

## 3. 为何AI时代再次垂青？MCP/A2A 的选择逻辑

**MCP和A2A**是AI领域新兴的协议，旨在为日益复杂的AI系统（如多模型协作、Agent智能体交互）提供**标准化的通信框架**，解决互操作性问题。 那么，JSON-RPC 2.0究竟凭借哪些优势，在众多协议中脱颖而出，被MCP、A2A等选中呢？下面我们就来看看JSON-RPC的优势。

**极致简洁，降低开发与理解成本**

JSON-RPC 2.0 使用人类可读的 JSON 格式。其规范非常简单，定义清晰，无论是开发者学习、实现客户端/服务端，还是调试网络通信，成本都相对较低。这在需要快速迭代和广泛协作的AI领域尤为重要。

**跨语言跨平台，适应AI生态多样性**

AI的开发涉及Python、Java、Go、Rust等多种语言和框架。JSON-RPC的简洁性和文本基础使其极易在不同语言和平台间实现互操作，为构建异构AI系统提供了基础通信能力，某种程度上提供了通信层面的“一站式解决方案”的可能性。

**传输协议无关，提供高度灵活性**

JSON-RPC 2.0本身不绑定具体的网络传输协议。它可以承载于HTTP(S)、WebSocket、TCP、消息队列等多种传输层之上。这种灵活性使得它可以适应不同的部署环境和通信需求，无论是需要低延迟长连接的Agent交互，还是简单的模型服务调用。

**成熟稳定，生态工具丰富**

作为一个存在已久的协议，JSON-RPC 2.0拥有大量成熟的库和工具支持，覆盖了几乎所有主流编程语言。这意味着开发者可以快速集成，将更多精力投入到核心的AI逻辑开发上，而不是在基础通信协议上“重复造轮子”，符合用户“要更高效”的心理。比如：golang.org/x/exp/jsonrpc2就是Go team维护的一个高质量JSON-RPC 2.0的实现。

**清晰的请求-响应模式，契合常见AI服务调用**

JSON-RPC明确的请求（方法名、参数）和响应（结果、错误）结构，非常适合表示AI服务中的函数调用、查询等交互模式，使得接口定义和理解更加直观，有助于提升开发和沟通效率。

**易于扩展**

JSON-RPC协议本身简洁，但params和data字段提供了足够的**扩展空间**来承载复杂的AI特定数据结构。

以上JSON-RPC协议的核心特点与AI时代需求的**高度契合**。

## 4. 小结：大道至简，务实之选

**综上所述**，JSON-RPC 2.0并非昙花一现的“新宠”，而是凭借其**诞生之初的简洁设计、久经考验的稳定性、广泛的跨平台能力以及与当前AI通信需求的天然契合**，在AI时代焕发了新的生机。MCP、A2A等协议选择它，正是看中了其作为通信基石的**扎实、高效和务实**。

对于JSON-RPC在AI领域的应用，以及未来可能出现的更优协议，**你有何看法？欢迎在评论区分享你的真知灼见！**

**关注**我，持续获取有深度的AI与技术解析。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Gopher的AI原生应用开发第一课”、“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

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

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论