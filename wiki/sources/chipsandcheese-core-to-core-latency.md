---
tags: [source, chipsandcheese, cpu, cache-coherence, lock, atomic]
date: 2026-04-19
sources: 1
---

# Exploring CPU Core to Core Latency and the Role that Locks Play（George Cozma / Chips and Cheese）

[[george-cozma]] 2021 年 6 月的文章，跟进早前 Rocket Lake 评测里引出的核到核延迟话题。测试工具由 Clamchowder 实现。

## 摘要

文章明确指出业界常用的"核到核延迟"测试其实测的是 **contested lock latency**——两线程在同一 cache line 上循环做 atomic CAS，被迫让 cache line 在两核间反复迁移。这种 workload 能代表的只是锁争用最坏情况，而非 CPU 日常。作者用 PMU 事件 XSNP（L3 hit 后需跨核 snoop）和 HITM（line 在另一核 modified 状态，必须跨核搬运）在 War Thunder、Time Spy、Overwatch、以及 Cinebench 等 workload 上测频率：contested lock ≤ 0.01% of instructions；L3 miss 则是 20–30 per 10000 instructions。游戏 L3 miss 比 HITM 频繁 20–30 倍，Cinebench 差 80 倍。结论：核到核延迟测试对现实 workload 性能几乎无预测力，CPU 评测应把重心放在 cache/内存层次。

## 关键要点

- Core-to-core latency test = contested lock 上 atomic CAS 的 cache line 往返延迟
- 游戏里 contested lock 占指令 ≤ 0.01%
- 游戏 L3 miss 频率是核间 HITM 的 20–30×
- Cinebench L3 miss 频率是 HITM 的 80×
- 跨 CCX/CCD 延迟高对多数真实 workload 影响很小
- PMU 事件 HITM / XSNP 是检测跨核一致性流量的正确手段

## 链接到的概念

- [[core-to-core-latency-lock-test]]
- [[cache-coherence-cross-cluster]]
- [[cas-refcount-lowbit-lock]]

## 原文

- 链接：https://chipsandcheese.com/p/exploring-cpu-core-to-core-latency-and-the-role-that-locks-play
- 本地：`raw/articles/chipsandcheese.com/2021-06-09_exploring-cpu-core-to-core-latency-and-the-role-that-locks-p.md`
