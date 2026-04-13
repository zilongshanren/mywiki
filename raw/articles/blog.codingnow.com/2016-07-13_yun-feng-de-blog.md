---
title: 云风的 BLOG
url: https://blog.codingnow.com/2016/07/
published: '2016-07-13'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 在 skynet 中如何实现多 actor 协作的事务

今天在 qq 群中，有个同学问，在 skynet 中，如果多个 actor 需要协作时，能否有事务来保证一系列操作的过程中，状态不会被破坏。

他举了个例子：

如果有一段业务逻辑是：

local a = skynet.call(A, ...) local b = skynet.call(B, ...) if a and b then dosomething() end

如何保证 a and b 这个条件有效呢？也就是说，在第一行从 A 处获取状态后，还要向 B 查询一个状态；如果希望两者查询完毕，一直到 dosomething() 结束前，A 和 B 的状态都不要改变。期间，如果有请求发到了 A 或者 B ，最后都暂时挂起。

后来，又有同学补充了一个更实际一点的案例：

如果我需要买点东西，先从银行查询余额，然后从商店获取一个物品，然后去银行扣掉钱，再把物品加到背包里。这个过程会涉及多个 actor ，整个过程又需要是一个事务，不要在执行这个事务过程中，有任何涉及的 actor 状态改变。

固然，我们肯定可以从设计上找到一个更好的方法处理上面这类交易事件，而不需要涉及复杂的多个 actor 之间的交互。但这也是一个典型的案例说明本文一开始想表达的需求。

如果一系列的操作只涉及一个 actor ，那么在这个 actor 中使用 [skynet.queue](https://github.com/cloudwu/skynet/wiki/CriticalSection) 就可以避免在处理消息过程中的外部干扰了。但若涉及多个 actor 就会麻烦一些。

我简单思考了一下，似乎还是可以用 skynet.queue 这个模块来解决这个问题。简单做了个实现，供参考。

这个事务的模拟有很多限制，其中之一是，任何时候系统中只能有一个事务在处理。（这个限制应该可以去掉，但加上这个限制，可以让这个 example 代码更简单一些）

如果你的 actor 要针对事务处理来响应消息，那么就应该使用 transaction.dispatch 来处理消息，而不是直接用 skynet.dispatch 分发。transaction.dispatch 会回传一个 transaction 对象，如果需要对外请求，应该使用 transaction:call 而不能再使用 skynet.call 。

transaction:call 会把事务的 session 号传递给对方，而每个能处理事务的 actor 每次收到请求后，都会根据 session 号把这个请求加到对应的队列中（由 skynet.queue 管理）。

而每个执行队列的最前面，都会向 transactiond 这个中心服务请求锁。如果当前没有事务在运行，那么回直接返回，从而拿到执行权；如果当前有其它事务在运行，则这个请求会被挂起，继而让整个运行队列都挂起。

这个 example 还有一些缺陷，如果要实际使用需要进一步完善。

比如 transaction 的创建和销毁都是显式的 api 调用（transaction.create 和 transaction:release），如果漏掉了 release 调用，或是中间过程有 error 没有捕获，或是还没等到 release 环节，服务自己退出了，跳过了 release ，都会导致整个事务锁不会被解开。

改进方法是用 pcall 封装事务的 create/release 过程，并在 transactiond 中增加一个监视创建者退出的方法。这个这里就不展开了。