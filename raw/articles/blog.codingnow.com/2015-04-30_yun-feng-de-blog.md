---
title: 云风的 BLOG
url: https://blog.codingnow.com/2015/04/
published: '2015-04-30'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### ltask ：用于 lua 的多任务库

2021 年 2 月 7 日：这个库已经删除，用新的实现代替了。见：[https://blog.codingnow.com/2021/02/ltask.html](https://blog.codingnow.com/2021/02/ltask.html)

写这个东西的起源是，前段时间我们的平台组面试了一个同学，他最近一个作品叫做 [luajit.io](http://luajit.io/) 。面试完了后，他专门找我聊了几个小时他的这个项目。他的核心想法是基于 luajit 做一个 web server ，和 `ngx_lua`

类似，但撇开 nginx 。当时他给我抱怨了许多 luajit 的问题，但是基于性能考虑又不想放弃 luajit 而转用 lua 。

我当时的建议是，不要把 lua/luajit 作为嵌入语言而自己写 host 程序，而是想办法做成供 lua 使用的库。这样发展的余地要大很多，也就不必局限于用户使用 lua 还是 luajit 了。没有这么做有很多原因是设计一个库比设计一个 host 程序要麻烦的多，不过麻烦归麻烦，其实还是可以做一下的，所以我就自己动手试了一下。

Lua 的多任务库有很多，有兴趣的同学 [可以参考一下 lua user wiki](http://lua-users.org/wiki/MultiTasking) 。

一般有几种做法：要么不使用操作系统的线程，只用 lua 本身的 coroutine 来模拟多任务。用 lua 写一个调度器即可。由于 lua 目前允许从 debug hook 中 yield （但暂时需要用 C 来实现 hook），所以甚至你可以实现一个抢占式的调度器；另一种流行的做法是在每个 os thread 里都开启一个独立的 lua vm ，然后用消息通讯的方式协作。

大多数库实现出来都是为了解决类似 web 服务这种需求，所以同时也都实现了一套配套的网络接口，让网络 IO 可以和多任务系统协调工作。

而我想了一段时间后觉得，如果有一个纯粹的 lua 多任务调度库更好。而且这种库不应该实现成 n:n 的调度器，也就是一个 os thread 配一个 lua vm 。这样就不适合做轻量的任务了。原本创建销毁 lua vm 都是很轻量的操作，而单个 lua vm 所占的内存资源也非常小，基本开销甚至比 os thread 本身的开销小的多。有了 vm 的隔离，实现成 m:n 的调度器应当是理所当然的事。btw, `ngx_lua`

这种让不同连接复用 lua vm 的方式，虽然可以提供响应速度，节省单连接上的内存开销，但从设计上我认为是不太干净的。

解决了任务调度器后，唯一必须的底层协作设施就只有 channel 通讯；而网络 IO ，timer 这些，都应该是更上层的设施，这样的设计可以让多任务库更简单纯粹。比如处理大量网络连接的 lua 库，我的同事就在 libev 的基础上实现过一个 [levent](https://github.com/xjdrew/levent) 。完全可以在一个 task 中运行 levent ，然后把收发的网络包通过 channel 传给别的 task 去处理。

我大概花了两天时间做接口设计和实现。目前的代码基本可以运行，放在 github 上，[https://github.com/cloudwu/ltask](https://github.com/cloudwu/ltask) 。目前仅提供了一个 M:N 调度器和一组内建的 channel 设置。

你必须在主程序中启动初始化调度器，初始化的时候可以配置使用多少条工作线程。一旦调度器启动起来，将阻塞住永不退出（目前的概念阶段的简化处理），所以在启动之前，你需要启动你的 task 。每个 task 都是一个 lua 文件，可以传递给它任意参数。同一个 lua 文件被启动多次是多个独立的 task 。在 task 运行中也可以启动新的 task ，task 的总数只受内存限制。

调度器会平均把任务分配到固定的工作线程上。task 并没有固定绑定某个特定工作线程。任何一条工作线程空闲时，都会尝试从其它工作线程的队列中抢走待命的 task 。

每个 task 由于是一个独立的 lua vm ，所以不可以共享 lua 数据。但是它们可以通过 channel 协作。channel 从调度器里创建出来，用一个数字 id 来标识，所以 id 可以很方便的在 task 间传递。调度器尽量不复用 channel id （除非 32bit 回绕），所以即使一个 channel 被关闭，读写它也是安全的，并不会错误的操作到其它 channel 上。channel 中每组数据都可以被原子的读写，单条记录可以是任意多个 lua 数据的组合。channel 可以同时有多个读者和写入者。当 channel 存在多个读取者时，调度器会尽量平均的把数据依次分配出去。channel 的写入是非阻塞的，只要内存够用，你可以无限的向 channel 写入数据。

和很多类似框架不同，channel 的读操作并非阻塞的。如果 channel 为空，读操作也会立刻返回。所以在使用时，通常你需要在 lua 层再做一点封装。在读 channel 前应该先 select 它（可以同时 select 多个 channel ）。由于 select 也并不阻塞，所以在 select 返回空时，应该立刻调用 coroutine.yield() 让出 cpu 。而最后一次 select 失败，会将当前的 task 标记为 blocked 状态，yield 后不再放回 worker 的处理调度队列中，直到相关 channel 有新的数据写入。

所以，一切的阻塞点都发生在 coroutine.yield 上。在 task 的 main thread 里调用 coroutine.yield 会让出当前 task 对 cpu 的占用。至于 worker 会不会立刻切回来，取决于你之前是否有 select 调用以及 channel 的状态。

ltask 看起来和 skynet 解决了差不多的问题：让 lua 可以充分利用多核系统处理多任务。但它们还是有一些不同的。

skynet 本质上是消息驱动的模型。每个服务（对应 ltask 中的 task ）只有一个 channel ，就是它自己。每条消息会唤醒服务一次，赋予服务一小片 CPU 时间。skynet 和 erlang 也不同，它并没有将 channel 实现成一个 mailbox ，所以服务不能自己挑拣消息，而必须按次序消化掉每条消息。

ltask 更接近 erlang 的调度方式。每个 task 可以关心任意多 channel ，task 也可以随时让出 cpu ，而不一定以消息处理来分割时间片。如果你在 task 中设置 debug hook ，也可以很容易的模拟 erlang 那种调度方式，对指令情况做一个简单的记数，超过一定范围后就强制 yield 。而不必让业务层自己来主动调用 yield 。

目前我不太好判断这两种方式的优劣，只能说 skynet 在它设定的模式下，可以实现的效率更高一点点。但从通用性角度看，却不及 ltask 这样简单纯粹。skynet 也很难实现成一个外挂的 lua 库，而使用 ltask 你可以方便的和其它库一起工作来搭建一个你需要的业务处理框架。

能够在 1 天半时间把这个东西搭建好，也是因为之前做了许多铺垫工作。

最后随便提一下：

关于线程池，我没有使用现成的第三方跨平台库。而是自己先实现了一个简单的对 pthread 及 windows threading api 的封装。毕竟我需要用到的 api 很少，所以有个 100 多行的封装库就够了。有兴趣的同学可以看看这个独立的仓库：[https://github.com/cloudwu/simplethread](https://github.com/cloudwu/simplethread)

在 ltask 中，task channel 都是暴露出数字 id 供业务层使用的。我觉得这是在多线程环境下最好的方式，比交给用户对象指针要健壮的多。这里我用到了前几天从 skynet 里提出来的另一个模块，之前[写过一篇 blog 介绍](http://blog.codingnow.com/2015/04/handlemap.html) 。