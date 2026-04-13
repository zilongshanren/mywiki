---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/cat52/
published: '2023-05-01'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

今天发现 Skynet 消息处理的一个 bug ，是由多线程并发引起的。又一次觉得完全把多线程程序写对是件很不容易的事。我这方面经验还是不太够，特记录一下，备日后回顾。


Skynet 的消息分发是这样做的：

所有的服务对象叫做 ctx ，是一个 C 结构。每个 ctx 拥有一个唯一的 handle 是一个整数。

每个 ctx 有一个私有的消息队列 mq ，当一个本地消息产生时，消息内记录的是接收者的 handle ，skynet 利用 handle 查到 ctx ，并把消息压入 ctx 的 mq 。

ctx 可以被 skynet 清除。为了可以安全的清除，这里对 ctx 做了线程安全的引用计数。每次从 handle 获取对应的 ctx 时，都会对其计数加一，保证不会在操作 ctx 时，没有人释放 ctx 对象。

skynet 维护了一个全局队列，globalmq ，里面保存了若干 ctx 的 mq 。

这里为了效率起见（因为有大量的 ctx 大多数时间是没有消息要处理的），mq 为空时，尽量不放在 globalmq 里，防止 cpu 空转。

Skynet 开启了若干工作线程，不断的从 globalmq 里取出二级 mq 。我们需要保证，一个 ctx 的消息处理不被并发。所以，当一个工作线程从 globalmq 取出一个 mq ，在处理完成前，不会将它压回 globalmq 。

处理过程就是从 mq 中弹出一个消息，调用 ctx 的回调函数，然后再将 mq 压回 globalmq 。这里不把 mq 中所有消息处理完，是为了公平，不让一个 ctx 占用所有的 cpu 时间。当发现 mq 为空时，则放弃压回操作，节约 cpu 时间。

所以，产生消息的时刻，就需要执行一个逻辑：如果对应的 mq 不在 globalmq 中，把它置入 globalmq 。

需要考虑的另一个问题是 ctx 的初始化过程：

ctx 的初始化流程是可以发送消息出去的（同时也可以接收到消息），但在初始化流程完成前，接收到的消息都必须缓存在 mq 中，不能处理。我用了个小技巧解决这个问题。就是在初始化流程开始前，假装 mq 在 globalmq 中（这是由 mq 中一个标记位决定的）。这样，向它发送消息，并不会把它的 mq 压入 globalmq ，自然也不会被工作线程取到。等初始化流程结束，在强制把 mq 压入 globalmq （无论是否为空）。即使初始化失败也要进行这个操作。