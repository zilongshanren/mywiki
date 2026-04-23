---
tags: [source, 并发, 多线程, 消息队列, X-Plane]
date: 2026-04-19
sources: 1
---

# A Healthy Fear of Threading（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 8 月的随笔，核心观点：**加线程必须有明确收益，因为它把程序正确性验证从 dynamic testing 升级成了 static reasoning**。文章给出 X-Plane 实践中常用的对策——**消息队列作为线程所有权原语**。

## 摘要

单线程代码的 bug 可以通过反复运行来逐步暴露；多线程不行——interleaving 每次都不同，且没有保证说「跑 N 次穷举了所有可能顺序」。要验证正确性必须用逻辑证明锁 / 同步约束让执行组合收敛到「有限且每个都正确」。这不是快速工作，所以**引入线程的标准应该是「收益值得这份开发成本」**。X-Plane 需要吃满多核，Supnik 的折中是只用执行限界已知的设计模式，其中最常用的是消息队列：数据的读写权随消息沿队列流动，**有消息才有指针，没消息就 deref 不了任何东西**，C++ 的 RAII + 指针语义天然封死误操作。这比粗锁收紧了 interleaving 粒度，是实际可工程化的方案。

## 关键要点

- 多线程正确性从 testing 升级到 reasoning，人类和工具都不擅长
- 加线程的决策点是「节省的 ms 是否值得开发成本」，默认答案是否
- 消息队列 = 数据所有权随消息流动 = 每时刻只有一个线程握着指针
- C++ 的指针 + RAII 让这套约束局部可检查
- 同思路的其它模式：主线程任务注入、task 化、actor/channel

## 链接到的概念

- [[message-queue-thread-ownership]]
- [[main-thread-task-injection]]
- [[vfx-multithreading-patterns]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/08/healthy-fear-of-threading.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-08-06_a-healthy-fear-of-threading.md`
