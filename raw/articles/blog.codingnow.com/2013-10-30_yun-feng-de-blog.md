---
title: 云风的 BLOG
url: https://blog.codingnow.com/2013/10/
published: '2013-10-30'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### skynet 中 Lua 服务的消息处理

最近为 skynet 修复了一个 bug ，[Issue #51](https://github.com/cloudwu/skynet/issues/51) 。经查，是由于 redis driver 中的 batch 模式加锁不当造成的。

有同学建议把 batch 模式取消，由于历史原因暂时还保留。在很多其它 redis driver 的实现中也不提供类似机制。也就是依次提交多个数据库操作请求，不用等回应，最后再集中处理数据库返回的信息。

我的个人建议是在目前的 redis driver 基础上再实现一个独立服务，里面做一个连接池，让系统不同服务对数据库的读写工作在不同连接上，这样可能更好些。如果简单的实现一个数据库代理服务而不采用连接池的话，可能会面对一些意想不到的情况。

这是由 skynet 的 lua 模块工作方式决定的，下面解释一下。

skynet 中的不同服务是利用系统的多线程完全并行的。当你从服务 A 向 B 和 C 分别各发送一条消息时，并不能保证先发的消息先被处理。

而当你从服务 A 向 B 依次发送两条消息，那么先发的消息一定会被 B 先处理。

用 lua 实现的服务只是一个内嵌了 Lua 虚拟机的服务，也遵守上面的规则。但目前的实现中，由于使用了 lua 的 coroutine 机制，问题变得更复杂一些了。

如果 B 是一个 lua 服务，当 A 向 B 发送了两条消息 x 和 y 。skynet 一定保证 x 先被 B 中的 lua 虚拟机收到，并为 x 消息生成了一个 coroutine X ，并运行这个 coroutine 。然后才会收到消息 y ，重新生成一个新的 coroutine Y ，接下来运行。

大多数情况下系统是会保证运行次序的。可一旦 coroutine X 中调用了skynet 提供的 socket IO 处理，或是调用了 skynet.call skynet.sleep （注：skynet.send 不会导致挂起）等会导致 coroutine 挂起的指令，那么消息处理的执行流就被暂时挂起了。

和 erlang 的 process 不同，此时 skynet 挂起的是 lua vm 中的 coroutine ，服务 B 本身是可以继续处理消息的。这个时候，一旦 y 消息抵达，一个新的 coroutine Y 就会被创建并运行。看起来，B 中就有两条执行流程并行了。

从这个意义上来说 skynet 中 lua 虚拟机里的 coroutine 才能看成是 erlang 中 process 的（不完全）等价物。lua 虚拟机，也就是 skynet 中的一个服务，提供了一个共享环境，让不同的 coroutine 之间可以共享状态。这也是很多 bug 的滋生之处。

如果这个行为让你困扰的话，那么我建议另外实现一个 lua 库，去掉 coroutine 的部分，转而实现一个类似 erlang 的 mailbox 机制来接收 skynet 的 C 层转发过来的消息会更好一些。

或者，我今天给 skynet 增加了一个叫 mqueue.lua 的库，可以给每个服务定义一个消息队列，消息队列里的消息会被依次处理。

见 testqueue.lua 以及 pingqueue.lua 可以看到基本用法。