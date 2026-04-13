---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/11/
published: '2017-11-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Windows 下重定向当前进程的 stdout 到网络连接

前段时间碰到一个需求，想把当前进程的标准输出重定向到一个 tcp 连接上。

如果依照 posix 标准，调用一下 dup2 这个 api 就能搞定，但是 windows 并不是基于 posix 标准的操作系统，所以做起来要麻烦的多。

我在 stackoverflow 和 msdn 上找了一番，没有看到什么靠谱的做法，所以自己折腾了一天。这里的难点在于：windows 上虽然有 `_dup2`

来模拟 posix 的 api dup2 ，但 fd 在 windows 上并不是内核对象， HANDLE 才是。fd 是在 runtime 层模拟出来的东西。msdn 上引用最多的一篇是：[Creating a Child Process with Redirected Input and Output](https://msdn.microsoft.com/zh-cn/library/windows/desktop/ms682499(v=vs.85).aspx) ，做的事情是创建一个子进程，然后重定向标准输入输出。

重定向子进程和重定向当前进程有什么区别？我是这样理解的：

Windows 虽然也有标准输入输出的概念，但是是基于 HANDLE 的。GetStdHandle 和 SetStdHandle 两个 API 虽然可以读写 Windows 的标准输入输出句柄，但这个句柄似乎（我猜想）是在 runtime 初始化阶段绑定到 fd 0 1 2 上的，之后，基于 fd 的一套 runtime 机制都不再经过这个转换过程。在进程运行过程中，调用 SetStdHandle 并不能重定向 C 的标准输入输出库。

在 stackoverflow 上的一个帖子也谈及了这个问题，[SetStdHandle has no effect on cout/printf](https://stackoverflow.com/questions/21374548/setstdhandle-has-no-effect-on-cout-printf) 。模仿 posix 的做法，使用 GetStdHandle 获得 windows 标准输出，然后利用 DuplicateHandle 复制 handle 的做法是无效的。

帖子里给出的方案是在 runtime 层用 `_dup`

复制 fd 再重定向到文件。不过想重定向到网络连接却没这么简单。因为 windows 下 socket 并不是 first class 的 handle ，不能直接当普通的文件 handle 使用，也就无法用 dup/dup2 传过去。

所以，我们需要先将 stdout 用 dup2 重定向到匿名管道，再创建一个线程去读这个管道，转发到 socket 。

光启动这么一个转发线程也有潜在的问题：在进程结束的时候，runtime 在处理最后的标准输出时，无法直接让转发线程感知到，这样有可能丢失结束前最后的输出。我们需要额外的机制在进程要结束时通知转发线程停止转发。主动通知可以让转发线程处理完所有已经转发的数据，而不会有遗漏，主线程则可以等待转发线程工作作完再自行退出。

因为读转发管道 Handle 使用的是 ReadFile ，windows 下的文件 Handle 无法和 Windows 的 Event 一起通过 WaitForMultipleObjects 工作（这或许是 windows 要额外引入 IOCP 的原因之一？）。我们不能利用额外的 Event 来做这件通知工作，只能通过关闭管道，让 ReadFile 感知。

这里要小心，dup 内部会增加内核 handle 的引用计数，所以不要漏掉了 close ，否则会让管道没有正确关闭，ReadFile 无法在关闭后返回。

我 [写了一个示例供参考](https://github.com/cloudwu/netout) 。它把转发开启和转发结束的过程封装在一个 lua 模块中。