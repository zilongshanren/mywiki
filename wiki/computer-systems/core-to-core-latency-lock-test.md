---
tags: [cpu, cache-coherence, atomic, lock, benchmark, HITM]
date: 2026-04-19
sources: 1
---

# 核间延迟测试：测的是锁，不是 CPU 的日常

很多 CPU 评测会给一张"核到核延迟"矩阵——一般数百到上千 ns 的数值。George Cozma / Chips and Cheese 2021 年 6 月的文章明确指出：这个测试测的是**被争用锁**（contested lock）在两个核之间搬运的延迟，与真实 workload 的平均表现关系很弱。

## 测试怎么做

两个线程在共享 cache line 上不停执行 **原子 compare-and-set**（CAS）。每次 CAS 需要独占该 line，强制 cache coherence 协议把 line 从上一个 owner 核拉到当前核，记录一次 core-to-core transfer。两个线程交替压榨，测出的就是 line 在两核之间往返的平均延迟。

这类锁原语正是上层 mutex / spinlock 构建的基础（参见 [[cas-refcount-lowbit-lock]]）。测试结果在理论上能代表"两个线程竞争同一数据"的最坏情况。

## 真实 workload 里锁有多频繁

作者用 Intel 的 PMU 事件（XSNP = L3 hit 后需要跨核 snoop；HITM = 在另一核的 L1/L2 里找到 modified 状态的副本，必须跨核搬运）对 War Thunder、Time Spy、Overwatch、以及自家 core-to-core 测试本身做实测：

- 所有被测游戏：**contested lock 占指令数 ≤ 0.01%**
- 游戏 L3 miss ≈ 20–30 / 10000 instructions；core-to-core transfer 比 L3 miss 稀有 20–30 倍
- Cinebench 这类高度并行生产力 workload：L3 miss 比 HITM 事件频繁 80 倍

## 结论

核到核延迟测试只是 CPU 总体性能的一个小侧面，重要性远不及 cache/内存层次的整体延迟与带宽表现。游戏与多数生产力 workload 绝大多数时候被 memory latency（[[memory-hierarchy]]、[[gpu-memory-hierarchy-latency]]）主导而非 lock latency。

这一观察对 Ryzen 3000/5000 系列"跨 CCX/CCD 核间延迟高"的惯常批评提供了反驳证据——跨 CCD 的高核间延迟在真实 workload 里极少被触发到足以影响整机表现。相关延伸见 [[cache-coherence-cross-cluster]]。

## 对锁密集代码的含义

如果你的 workload 真的属于 contested lock 密集（某些数据库、强同步的 job system），核到核延迟数字才值得作为架构选择依据。大多数游戏、渲染、编码 workload 不在此列。降低 lock 争用本身（per-thread 累积、lock-free 队列、sharding）远比选 CPU 更重要。

## Sources

- [[sources/chipsandcheese-core-to-core-latency]]
