---
tags: [source, 并发, 同步原语, pthread, linux, nptl]
date: 2026-04-19
sources: 1
---

# Semaphore Follow-Up: NTPL（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 12 月的短文，是前一篇 [[sources/supnik-semaphore-vs-condvar|semaphore vs condition variable]] 的跨平台补记——把视角从 OS X 的 pthread 实现切到 Linux 的 NPTL 上。

## 摘要

Supnik 承认上一篇里那些 OS X 上让 `pthread_cond_wait` 变得昂贵的实现细节，在 Linux 的 NPTL（Native POSIX Thread Library）里**大多不存在**。NPTL 的 pthread mutex 是 spin-sleep 混合锁，适合短临界区而且 moderately contested 时反而占优；`sem_t` 有原子计数器，未争用时不进内核；底层一切同步都围绕 **futex**（fast userspace mutex）展开，确保未争用路径只用原子操作。OS X 的 pthread 虽然也用 spin lock 做用户空间簿记，但 Supnik 判断 futex 路径整体更快。换言之：**他之前为 X-Plane 自研 semaphore+critical section 队列的必要性，主要是被 OS X 的 pthread 实现放大的**；同一套代码在 Linux 上原生 pthread condition variable 也能跑得差不多快。

## 关键要点

- **NPTL mutex** = spin-sleep 组合，短临界区 fast-path 不进内核。
- **`sem_t` 原子计数器** 避免未争用情形的系统调用。
- **futex** 是 NPTL 一切同步原语的底座：未争用路径全部走原子操作。
- OS X 的 pthread 未争用路径也是 spin lock，但 Supnik 认为 futex 更快。
- 平台差异的直接后果：**同步原语的「正确选择」可能是平台依赖的**，不存在一种跨平台方案在所有 libc 上都最优。

## 链接到的概念

- [[semaphore-vs-condvar-latency]] —— 前作，描述为什么 OS X 上要换原语
- [[message-queue-thread-ownership]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/semaphore-follow-up-ntpl.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-04_semaphore-follow-up-ntpl.md`
