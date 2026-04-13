---
title: 云风的 BLOG
url: https://blog.codingnow.com/2018/05/
published: '2018-05-26'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 跟踪 skynet 服务间的消息请求及性能分析

skynet 中每个服务都是独立 lua 虚拟机，虽然服务间相互发起请求很容易，但业务复杂后，追踪业务逻辑却很麻烦。

我最近给 skynet 加了一个 skynet.trace() 命令，可以开启对当前执行序的跟踪统计。比如，在 example 的 agent 服务中，我们在每条 client 发起的请求处理时调用一次 skynet.trace() 就会得到下面这样的 log ：

[:01000012] <TRACE :01000012-5> 9563528587255135 trace [:01000012] <TRACE :01000012-5> 9563528587272881 call : @./examples/agent.lua:17 @./examples/agent.lua:36 @./examples/agent.lua:58 [:0100000d] <TRACE :01000012-5> 9563528587326048 request [:0100000d] <TRACE :01000012-5> 9563528587344784 response [:0100000d] <TRACE :01000012-5> 9563528587352027 end [:01000012] <TRACE :01000012-5> 9563528587367443 resume [:01000012] <TRACE :01000012-5> 9563528587423140 end

第一项是一个 tag ，用来标识这条 log 属于哪个 session 。tag 由服务地址和一个递增的编号组成，生成为一个唯一的字符串，方便程序过滤 log 。

第二项是时间戳，精度为 ns （即 1000000000 分之一秒）。可以用它来分析执行序每个环节的耗时。

第三项表明发生的事件。trace 表示开始跟踪；call 表示向另一个服务发起了请求； request 表示该服务收到了这个请求。通常 call 和 request 是紧挨着的，request 的 log 来源提示了调用到哪个服务中去了，而 call 后面还会显示发起调用的调用栈。这两条时间戳的差值为 skynet 框架内部消息延迟。如果被调用服务过载，那么这个延迟就会偏大。

response 表示服务回应了请求的消息，end 表示这个 tag 关联的请求在当前服务已经执行完毕。resume 表示当前服务被唤醒。sleep 表示被挂起（可能是因为调用 skynet.sleep 或 skynet.wait）。

实现这个 trace 功能并没有修改 skynet 的 C 内核，只是在 lua 部分做了手脚。这里用到了一点小技巧：我在需要跟踪的 coroutine 中，每次调用 skynet.call 之前，都向目的地址先发送了一个 `PTYPE_TRACE`

(新定义的消息类型) 消息，把 trace tag 同时发送过去。由于同一个服务内发送消息都是串行的，所以这条 TRACE 消息一定和 call 消息接连投递到。接收方服务在收到一条 TRACE 消息后，记录下是从哪里发过来的，那么接下来的一条同一来源的消息就是需要跟踪写 log 的。

trace 功能会略微降低 skynet 处理消息的性能，因为每条消息处理时都需要做一次判断。但是这个性能损失可以忽略不计，它给开发带来的好处却是很明显的。

5 月 28 日补充：

当使用 cluster 模式时，调用时跨进程的，所以需要对 clusterd 做一点改造，增加 trace 协议，可以把 trace tag 传播到别的节点。

由于现在集群并没有统一输出 log （当然你可以自定义 log 服务，汇总到一起），所以我们还需要额外生成一个集群唯一的 tag 方便程序处理。我的方法是再原有进程内的 tag 再加上 hostname pid nodename ，在每个需要追踪的执行流上 log 下这个全局唯一 tag 。我们在汇总的 log 中，就可以根据这个来过滤出相关信息出来。

我截取了内部一个服务器，一条消息的 trace log 信息，写了个脚本整理为树结构的文本，并统计出执行流的时间开销：包括总时间、内部计算开销、调度开销、集群间网络通讯开销等等。统计结构及转换脚本放在 [gist](https://gist.github.com/cloudwu/7c59d768d1e68f2797c4772b3ea96437) 上，等需要完善时参考。