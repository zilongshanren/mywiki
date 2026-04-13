---
title: 云风的 BLOG
url: https://blog.codingnow.com/2016/06/
published: '2016-06-30'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### skynet 的一个简单范例

之前已经介绍过，[skynet 只是一个轻量框架，不是一个开箱即用的引擎](https://github.com/cloudwu/skynet/wiki/GettingStarted)。能不能用好它，取决于使用者是否清楚知道自己要干什么，如果是用 skynet 做网络游戏服务器，那么就必须先知道网络游戏服务器应该如何设计。

在 skynet 发布版中带的 example 中，有类似 gate watchdog agent 之类的服务，它们并不是唯一的用 skynet 构建游戏服务器的模式。我想另外写一个范例，示范依旧基于 skynet 但用不同的模式构建游戏服务器的方法。

在这个范例中，我主要想展示这样一些东西：

[GateServer](https://github.com/cloudwu/skynet/wiki/GateServer) 并不是唯一的管理连接的模式。在 skynet 中，也可以自定义其它的方式来管理大量外部连接。这个例子中使用了前段时间我实现的[另一个模块](http://blog.codingnow.com/2016/03/skynet_tcp_package.html) ，这个模块并没有放在 skynet 发布版中。

在这个范例中，实现了一个 hub 服务，类似 gate 的作用。但是它仅仅监听端口，并把新建连接交给合适的服务处理。按范例中的流程，每个新连接都直接转交 auth 服务；只有 auth 服务认可了连接，再转给 manager 服务。

这里 auth 和 manager 都是单一服务。如果实际使用的时候有性能问题，auth 服务可以扩展为多个，做负载均衡。如果有必要，还可以加一个排队服务的环节。

manager 拿到连接的身份后，会根据身份分派 agent 服务代理这个连接上的请求。注意：这里的代码并没有简单的为已认证身份的连接启动一个新的 agent 。这也是很多对 skynet 缺乏了解的同学普遍的误解——skynet 一定会为每个链接创建一个独立的 lua vm 。

manager 管理若干 agent 的原则是，如果系统中没有为特定用户服务的 agent 存在，则启动一个新的。但即使这个用户连接断开，也不一定及时退出 agent 服务。agent 是否退出，是由 agent 自己决定的。manager 只负责将用户关联到活着的 agent 服务上。这个关联关系面向用户而不是面向连接的，多个连接可以同时通过 auth 认证，一起关联到同一个 agent 服务上（比如多客户端同时以不同连接接入）。

manager 服务目前实现的还很简陋，但是稍加改造，就可以支持把多个用户关联到同一个 agent 。比如，做棋牌服务器时，你可能让同一个牌桌的用户在一起会更好。

agent 服务可以用来处理业务逻辑。目前的范例中仅能处理 login 和 ping 请求。我们区分了 signin 和 login 。signin 表示用户已经通过了认证进入系统，但未必可以进行业务请求；而 login 表示被 agent 接受。这个范例里，如果一个用户 login 成功，在他的连接断开前，这个用户无法再次 login ；当然你可以稍微改造，变成后login 的用户顶掉前一个；或是让他们可以同存。

这个范例还提供了一个不同于 [snax](https://github.com/cloudwu/skynet/wiki/Snax) 另一个简单封装。展示如何不用 skynet 早期提供的具名服务方式，而使用 skynet.uniqueservice 来取代它们。

在这个范例封装中，只需要声明服务依赖的其它服务的名称就可以以正确的次序启动它们了。

封装层把 `skynet.dispatch`

`skynet.info_func`

等在编写 skynet 服务时的繁琐步骤简化了，它的工作原理理解起来可能比 snax 要简单一些，用起来也很容易。

这次的客户端使用了一个开源的 lsocket 库，而不是 skynet 发布版中那个简陋的 clientsocket 模块。这能更好的展示怎么编写 skynet 的客户端。

同时，客户端中使用 sproto 协议的代码也更清晰一点，稍微做了一些封装，让代码比 skynet 自带的 example 更易读。

服务器部分和客户端交互的部分也有对应的封装模块。

关于客户端部分，我比较推崇只使用请求/回应模式，而不支持服务器推送数据。如果需要推送，可以用 long polling 解决。

在客户端，和服务器不同，它要同时面对用户 UI 的交互、图像渲染、以及网络请求回应。所以我觉得不适合把服务器的那套 rpc 机制直接搬到客户端。所以在范例中，我也并没有使用 coroutine 来做 rpc 调用。

callback 模式可能更适合客户端的工作。但 callback 并不是 `rpc_call(request, cb)`

这种。而是把 request （只可以从客户端发起，服务器永远只响应客户端的请求，而没有反向请求）的回应处理方法注册在一张表中。

比如，有一个叫做 ping 的请求，客户端先定义好：

function ping(req, resp, session)

然后在需要 ping 服务器（对于客户端来说通常是由用户 UI 操作引起的）时，local session = request("ping", req) 就可以了。当收到服务器的 ping 回应时，上面的 ping 函数被回调，可以接收到当初 request 时发起的 req 数据，以及服务器传回的 resp ，和 session 。

如果 ping 操作是无状态的，那么 session 多半可以忽略掉。在回调函数中，我们可以拿到提起请求时的内容 req ，也就不必再依赖其它状态了。

有部分流程，可能依赖多次和服务器交互。这种带上下文的交互，或许我们应该用 coroutine 封装一下这类 RPC 调用？但目前最常见的多次交互只出现在登录认证流程中，似乎不必为它单独做太复杂的东西。