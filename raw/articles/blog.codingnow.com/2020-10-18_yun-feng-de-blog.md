---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/cat11/
published: '2020-10-18'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### cache server 问题总结

这周，我们的 cache server 服务面临了很多的挑战。项目资源超过了 30G ，有几十个用户在同时使用。每天都有版本切换工作（导致重新上传下载 30G 的数据）。在这个过程中，我对 cache server 程序修修补补，终于没有太大的问题了。

总结一下，我认为 cache server 的协议设计，以及 Unity 客户端实现，均存在很大的问题。这些问题是无法通过改进服务器的实现彻底解决的，只能做一些缓解工作。真正的完善必须等 Unity 的客户端意识到这些问题并作出改进。

cache server 的协议设计非常简陋。就是顺序的提交请求，然后每个请求会有序的得到一个回应。这些请求要么是获取 GET 文件，要么是上传 PUT 文件。其中 PUT 文件在协议上不必回应。

由于 PUT 文件没有回应，所以客户端无法直接确定文件是否全部上传完毕；如果必须确认，只能在 PUT 文件结束后，再提交一个 GET 请求。如果收到了后续 GET 的回应，可以理解为前一个 PUT 已经结束。实际上，Unity 客户端没想去确认 PUT 是否结束，从 log 分析，它只是简单的在最后一个 PUT 结束后等待了一段时间再断开连接。

PUT 实际上是个小问题，真正的问题是：这种依赖严格次序的协议，在面对两边数据量不对等、网络速度不对等的近况时，很难有一个健壮的实现。