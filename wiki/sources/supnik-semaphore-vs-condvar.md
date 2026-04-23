---
tags: [source, 并发, pthread, 同步原语, X-Plane]
date: 2026-04-19
sources: 1
---

# Performance of Semaphore Vs. Condition Variable（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 12 月，讲 X-Plane 10 的线程化飞行模型如何在 OS X 上把 worker 唤醒延迟从 200 µsec 降到 80 µsec。

## 摘要

X-Plane 10 把多架飞机的飞行模型并行化后，主循环需要把「工作」快速派发给 worker 池再等结果，对唤醒延迟非常敏感。原来的 message queue 基于 pthread condition variable + mutex，Shark profile 看到一堆 worker 线程挤在同一把 mutex 前互相踩脚——问题出在 `pthread_cond_wait` 的语义：被唤醒后必须重新获取原 mutex，N 个 worker 同时醒来会被迫串行化成 N 次锁争抢。换成 Windows 版本原本就在用的**critical section（spin lock）+ mach semaphore** 组合后，唤醒降到 80 µsec，其中 45 µsec 是 mach semaphore 信号开销的硬下限。根因：新设计的锁只保护队列链表本身，不再跨越 pthread 内部状态，加上 spin lock 面对极短临界区时比 pthread mutex 更轻。文末展望了 lock-free ring buffer FIFO：两把 semaphore 管 filled / free 计数，原子读写指针，关键不变量是「两个计数之和可以小于 buffer 容量」，代价是放弃消息严格顺序和部分现有 API 的锁定编辑能力。

## 关键要点

- pthread cond var 贵在 `cond_wait` 被唤醒后必须重锁——多 waiter 场景下演变成 lock convoy。
- 用 semaphore + spin-lock 拆开唤醒和队列保护，锁粒度更细。
- 临界区极短时 spin lock > pthread mutex（后者只要有 2 个线程争就 sleep，代价是一个系统调用）。
- 两级队列 + 预填充可以让 semaphore 的 wait 走快速原子路径，不进内核。
- Lock-free ring FIFO 设计：filled + free 两把 semaphore，原子 read/write ptr，和小于容量保证安全。

## 链接到的概念

- [[semaphore-vs-condvar-latency]]
- [[message-queue-thread-ownership]]
- [[main-thread-task-injection]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/performance-of-semaphore-vs-condition.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-03_performance-of-semaphore-vs-condition-variable.md`
