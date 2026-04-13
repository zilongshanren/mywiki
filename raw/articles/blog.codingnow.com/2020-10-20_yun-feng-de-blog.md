---
title: 云风的 BLOG
url: https://blog.codingnow.com/2020/10/
published: '2020-10-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

这周，我们的 cache server 服务面临了很多的挑战。项目资源超过了 30G ，有几十个用户在同时使用。每天都有版本切换工作（导致重新上传下载 30G 的数据）。在这个过程中，我对 cache server 程序修修补补，终于没有太大的问题了。

总结一下，我认为 cache server 的协议设计，以及 Unity 客户端实现，均存在很大的问题。这些问题是无法通过改进服务器的实现彻底解决的，只能做一些缓解工作。真正的完善必须等 Unity 的客户端意识到这些问题并作出改进。

cache server 的协议设计非常简陋。就是顺序的提交请求，然后每个请求会有序的得到一个回应。这些请求要么是获取 GET 文件，要么是上传 PUT 文件。其中 PUT 文件在协议上不必回应。

由于 PUT 文件没有回应，所以客户端无法直接确定文件是否全部上传完毕；如果必须确认，只能在 PUT 文件结束后，再提交一个 GET 请求。如果收到了后续 GET 的回应，可以理解为前一个 PUT 已经结束。实际上，Unity 客户端没想去确认 PUT 是否结束，从 log 分析，它只是简单的在最后一个 PUT 结束后等待了一段时间再断开连接。

PUT 实际上是个小问题，真正的问题是：这种依赖严格次序的协议，在面对两边数据量不对等、网络速度不对等的近况时，很难有一个健壮的实现。

先来看一个最直接的服务器实现的伪代码：

while true do
local req = get_request(fd)
local resp = handle_request(req)
put_response(fd, resp)
end

即用一个死循环，依次获取网络请求，针对请求生成回应数据，然后将回应数据经网络发回。

看似符合协议，但若你这么实现，则很有可能不能正常工作。

假设 `get_request`

是阻塞读网络，`put_response`

是阻塞写网络，那么就要求客户端也是严格的配合：客户端也必须提起一个请求后，等待回应，然后再提下一个请求。否则，若客户端连续提两个请求，服务器在处理第一个请求后，推送的回应客户端不去接收（因为客户端还在提第二个请求），就可能会死锁。

死锁发生时，客户端在推送第二个请求（写操作），而服务器在推送第一个回应（写操作）；两边都没在收取对方的数据，两侧的 api 都等待在写网络上（因为对端不读）。

但现代服务器框架一般会将网络读写分离到独立线程中，死锁不会发生。服务器收到新请求就能处理，产生出回应数据。而回应数据将缓存在网络线程中，等待客户端接收，而不会阻塞住上面的业务循环。那里的 `put_response`

是非阻塞的。

但这却非常容易产生 OOM （内存溢出）的问题。因为请求和回应是不对等的，客户端可以轻易的发起大量的 GET 请求，一条几十字节的 GET 请求，很可能需要几十上白兆的回应包。巨量的回应包积压在网络线程的发送队列中，很快就会吃光所有的内存。

所以，`put_response`

这个函数必须在内存耗光前阻塞住，前面的问题就会回来。所以，合理的服务器设计必须分离 `get_request`

和 `put_response`

到两个执行序列里。

我看过早期的 unity 官方 cacheserver 的实现，只有一个简单的 js 文件，跑在 nodejs 服务中。nodejs 是基于回调机制的，请求处理放在了 socket 的 data 事件回调中，每个请求都会生成一个新的对象，这个对象会进入一个队列，由 socket 的可写事件触发出队列操作，将文件 pipe 到 socket 上。

因为回应操作是由文件的 pipe 到 socket 依次完成的，这个过程可能很慢（取决于对端的接收进度），那么新请求非常可能积压在队列中。假设客户端一直推送请求，而疏于处理回应的话，这个队列将一直增长，直到 OOM 发生。

现在的 cacheserver 版本已经变得非常复杂，不太容易看清楚。我简单浏览了一下，觉得依旧存在这个隐患：在 [server/command_processor.js](https://github.com/Unity-Technologies/unity-cache-server/blob/master/lib/server/command_processor.js#L371) 文件中，`_onGet`

函数会把要回应的 item 压入队列（`this[kSendFileQueue].push(item);`

) 这个队列可能无限增长。

我们现在的实现也是类似的机制，伪代码如下：

-- request thread
while true do
local req = get_request(fd)
push_queue(q, req)
end
-- response thread
while true do
local req = pop_queue(q)
local resp = handle_request(req)
put_response(fd, resp)
end

这里的 `push_queue`

在达到队列预设的容量后，是会阻塞等待另一个线程的 `pop_queue`

取走再继续工作的。

我们在做此修改后，把 queue 的容量设置为 8192 ，实际运行时，客户反馈以前正常的打包过程（其实会让服务器濒临 OOM 崩溃），现在有时会卡在和 cache server 的通讯上。经过线上观察（使用 skynet 预留的 debug console 的 debug 功能进入服务查看内部状态），发现这个 queue 很容易就满了，等待 `pop_queue`

；而能执行 `pop_queue`

的线程却阻塞在 `put_response`

上，也就是 unity 客户端拒绝接收前面那 8000 个请求产生的回应。

针对这种情况的合理推测是， unity 在某些极端情况下，一口气发了上万（甚至十万个）请求，它在这些请求全部从网络发出之前，没有跑网络接收的业务，导致数据全部堵在网络层；而服务器为了避免自己内存耗尽，只能暂停接收新的请求，结果就卡了。

换句话说，针对客户端不合理的使用：不断地发送请求，拒绝处理回应，那么服务器若想一直服务下去，只能在内存耗尽和卡住间二选一。当然还有拒绝服务的第三条路，即在异常情况（卡住）后，踢掉客户端。客户端发现断线，就会重连服务器再来一次。


我们最终的对策是，优化队列，让队列中保存的数据足够的少（这里可以只讲客户端请求 id 保留在队列中，每个请求所需内存在 100 字节以下）然后增加队列的容量上限到百万级；当队列满时踢掉客户端。

最近两天似乎工作平稳了。