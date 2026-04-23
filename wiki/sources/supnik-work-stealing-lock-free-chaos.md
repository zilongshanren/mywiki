---
tags: [source, 并发, 无锁, work-stealing, 设计哲学, x-plane]
date: 2026-04-19
sources: 1
---

# Work Stealing and Lock Free Chaos（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2016 年 1 月短评 CppCon 2015 上 Pablo Halpern 的 work-stealing 讲座与 Fedor Pikus 的 lock-free 讲座，顺手交代了 X-Plane 自己的并发选择。

## 摘要

X-Plane 的任务调度器是**中央 work-pool**（类似 libdispatch），不玩 continuation 之类的花样——假设背景任务数量足够大、任务是冷的、通常要调度到非渲染核心上。Supnik 借 Pikus 的讲座提炼出一条黄金法则：**通用 lock-free 是陷阱**。Pikus 的核心观点有两层：其一，并发 FIFO 这种数据结构「真的是 FIFO 吗」根本没法测——要 assert 顺序就必须引入同步，而同步又破坏无锁；其二，不要写通用 lock-free，而要**在应用层找机会简化问题**。X-Plane 的艺术资源 API 本身**不**是 lock-free 的（加载 / 卸载要拿全局表锁），但「拿到引用计数和指针后使用资源」的路径**是** lock-free 的。这对渲染主线程足够——它永远不被 loading 线程阻塞。这种分层是「unfair but unfair in the right direction」，在需要 fast path 的地方零同步，在冷路径上老老实实用锁。文末预告「这其实有个微妙的 race」——就是两天后的 [[supnik-worst-lock-ever]]。

## 关键要点

- X-Plane 用中央 work pool，不用 work-stealing 的 continuation 链
- 并发容器的正确性不可测（测试本身破坏观测）
- 不要写通用 lock-free，要在应用层简化
- 分层：loading API 不 lock-free，using API lock-free
- refcount + immutable pointer 是这种分层的粘合剂

## 链接到的概念

- [[app-space-lock-free-simplification]]
- [[cas-refcount-lowbit-lock]]
- [[message-queue-thread-ownership]]
- [[performance-by-design]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/01/work-stealing-and-lock-free-chaos.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-01-08_work-stealing-and-lock-free-chaos.md`
