---
title: 云风的 BLOG
url: https://blog.codingnow.com/2016/05/
published: '2016-05-13'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 代理服务和过载保护

在 skynet 中，有时候为一个服务实现一个前置的代理服务是很有必要的。

比如，你希望对这个服务发起的请求是支持超时的，就不必在功能实现的服务中实现，那样会增加无谓的复杂性。你可以在功能实现的服务前加一个代理服务，当超时发生时，通知请求方。关于这个实现，我在 blog 中[给过一个示例](http://blog.codingnow.com/2015/10/timeout_skynetcall.html)。

同理，当你需要做一些负载均衡的处理的时候，也可以做一个代理服务，让请求分摊到多个可以完成类似功能的服务中去，实现比较简单，本文就不展开了。

今天想谈一下怎么利用代理服务更好的为一些热点服务提供过载保护。

[过载保护在两年前我就写过](http://blog.codingnow.com/2014/10/skynet_overload.html)，这两年的运营产品经验表明，对于缺乏经验的 skynet 使用者，它是最容易碰到的问题。这可能也是并发环境的最需要解决的问题。

[我想过在未来的版本中，做一些更底层的保护措施](http://blog.codingnow.com/2016/01/skynet2.html)。不过目前的 skynet 1.0 版，我们依旧可以在上层做一些工作。

假设我们已经知道了某个服务容易成为热点，那么前置一个代理服务就可以做很多事情。

所谓代理服务，就是向真正的功能服务发起请求时，请求消息发到另一个代理服务中，由这个代理服务转发这个请求给真正的功能服务；同样，回应消息也会被代理服务转发回去。

代理服务在过滤这些消息时，可以做一些工作，例如：

如果某个服务的请求过于频繁，则可以暂时搁置这些请求，而优先转发其它服务的请求。这样便增加了公平性。而如果请求来源的服务已经退出，在代理服务中若还存在他所未发出的请求，则可以直接将这些消息丢弃，减轻功能服务的负担。

我们还可以从代理服务勘察对应的功能服务的负载情况，如果功能服务过忙，也可以暂时缓存新的请求。这样可以让我们从调试控制台对功能服务发起调试控制指令时，可以更快的回应。（从调试控制台直接对功能服务发起命令，不经过代理）在线上解决问题时，往往服务过载后，调试指令响应迟缓会极大降低线上处理故障的效率。

skynet 对编写代理服务已经提供了不错的支持，你可以参考 [clusterproxy 服务](https://github.com/cloudwu/skynet/blob/master/service/clusterproxy.lua) 来编写自己的服务代理。

通常一个代理服务是这样的：

local skynet = require "skynet" require "skynet.manager" -- inject skynet.forward_type skynet.register_protocol { name = "system", id = skynet.PTYPE_SYSTEM, unpack = function (...) return ... end, } local forward_map = { [skynet.PTYPE_LUA] = skynet.PTYPE_SYSTEM, [skynet.PTYPE_RESPONSE] = skynet.PTYPE_RESPONSE, -- don't free response message } local realsvr = tonumber((...)) skynet.forward_type( forward_map ,function() skynet.dispatch("system", function (session, source, msg, sz) skynet.ret(skynet.rawcall(realsvr, "lua", msg, sz)) end) end)

上面的代码并不完整，你需要根据你的真正业务逻辑补全它。

使用 `skynet.forward_type`

需要提供一张映射表，表示你需要处理哪些类型的协议。除此之外，和 skynet.start 的用法一致。

在映射表中的协议消息，框架不会释放消息所占的内存，这是为了避免做不必要的消息拷贝；同时，你也必须小心的处理它们，避免内存泄漏。

在上面的例子中，所有的 lua 协议类别的消息被重定向为 system 类别（这样你可以重新定义 unpack 函数，不做任何解包处理）。然后在随后的 dispatch 函数中，使用 skynet.rawcall 直接发送消息指针，从而绕过打包流程和对回应包的解包流程。

这里还映射了 response 类消息，仅仅是为了让框架不要释放它。在后续 dispatch 内，skynet.rawcall 返回的回应包是 C 指针和长度，直接交给 skynet.ret 就可以回应给原始请求方了。

这里的示例只处理了请求回应模式的消息。如果你还向正确转发单向的 skynet.send 行为，可以在里面多判断一下 session 是否为 0 。（请求消息的 session 约定为不等于 0 的整数）

**如何判断功能服务是否过载？**

如果是线上监控，你可以查看 log 。目前在消息队列过长来不及处理时，会输出 "May overload, message queue length = xxx" 。

服务自己也可以通过 skynet.mqlen 查一下当前待处理的消息队列长度。

如果你想取查询对方是否可能及时处理消息，比较简单的方法是实现一条协议，立刻返回。你作为请求方，使用 skynet.now 测试一下这个请求的回应速度。在最新的 skynet 版本中，我增加了默认的 debug 协议 ping 来做这件事情。

local ti = skynet.now() skynet.call(address, "debug", "PING") ti = skynet.now() - ti

使用 debug console 的话，可以使用 ping address 命令。

btw. 在上面的代理服务中使用 debug ping 是安全的。虽然 response 类消息的行为被 `skynet.forward_type`

修改为不会释放，但 debug ping 协议比较特殊，它的回应消息的内容为空。

如果你需要在代理服务中发起其它请求，记得使用 rawcall 并销毁掉回应包指针。

skynet.trash(skynet.rawcall(address, "lua", skynet.pack(...)))

需要手工销毁 ping 的 response 消息。

**如何即时获知一个服务已经退出？**

skynet 早期推荐的做法是使用 skynet.monitor 定义一个自己的监控服务。所有服务的退出都会通知它。但这种用法现在已经不推荐了。

如果被监控的服务是一个 lua 服务的话，目前最简单的方法是向这个服务发送一个永不返回的请求。而当该服务正常退出的话，这个没有返回的请求将会由框架向请求方抛出一个 error 。所以，只要你使用 pcall 向需要监控的服务发起一个 skynet.call ，就能感知到服务退出了。

skynet 最新版本增加了一个 debug 指令 link 可以帮助你做这件事：

pcall(skynet.call, address, "debug", "LINK")