---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/
published: '2023-09-22'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 一个任务调度算法引起的性能问题

这两天遇到一个任务调度算法引起的性能问题，花了颇多精力排查和解决。问题出在我写的 [ltask](https://github.com/cloudwu/ltask) 这个 lua 多任务库上。[ltask 最初是对 skynet 的一些反思中开始的](https://blog.codingnow.com/2021/02/ltask.html)，最初只是想换一种思路实现 skynet ：做一个库而不是框架、更少的锁竞争、避免服务因为消息队列堆积而过载……

后来、我们游戏引擎开始尝试基于 ltask 利用手机设备上的多核，渐渐的便完善起来，也发展出和 skynet 不同的部分。它最近两年一直是围绕移动设备客户端程序优化，所以网络部分并非重点，也就不需要像 skynet 那样把网络模块做在框架底层，而是以一个独立服务存在。而网络 IO 、文件 IO 、客户端窗口这些部分又不适合于其它渲染相关的服务混在一起，因为它们需要和操作系统直接打交道，所以我在 ltask 中又分出了独占线程和共享工作线程两种不同的线程，可以把不同的服务绑在不同的线程上。甚至对于 iOS ，[还必须让窗口线程运行在主线程上](https://blog.codingnow.com/2019/08/lua_switch_os_thread.html)，而不得不在 ltask 里做特殊的支持。

最近发现的这个问题也是游戏客户端特有的，它很能说明用于游戏服务器的 skynet 和用于客户端的 ltask 在实现侧重点上的不同。