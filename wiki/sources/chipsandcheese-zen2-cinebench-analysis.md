---
tags: [source, chipsandcheese, cpu, 微架构, zen2, 分支预测, 调度器]
date: 2026-04-19
sources: 1
---

# Analyzing Zen 2's Cinebench R15 Lead（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 2 月发表于 [[chips-and-cheese]] 的 Zen 2 微架构实测分析，以 Cinebench R15 单线程为载体，用性能计数器逐项比较 Zen 2 与 Skylake 的前端/后端/缓存特性。

## 摘要

文章从 CBR15 的指令构成出发（41.7% SSE、大量 FP64），逐步剖析 Zen 2 领先的三大原因。一是 [[branch-predictor-design|分支预测器]]：Zen 2 的 MPKI 为 5.15，Skylake 为 6.45，后者多出 25% 的误预测，直接浪费约 17% 的前端带宽。二是 [[cpu-scheduler-design|非调度 FP 溢出队列]]：Zen 2 通过在 36 条目 FP 调度器之外附加一个 64 条目非调度缓冲，使 FPU 侧可容纳 100 个待执行微操作而无需阻断派发，将后端受限周期从 Skylake 的 20.1% 压低到 15.1%。三是 L2 容量：512 KB vs 256 KB，在相同 12 周期延迟下提供更高的数据和指令命中率，减少 L3 访问频率。文章也诚实指出 Skylake 的优势面：更大的 store buffer、更高的 op cache 命中率以及一体式设计带来的更低内存延迟。

## 关键要点

- Zen 2 MPKI 5.15 vs Skylake 6.45：每千指令多 1.3 次误预测 × ~16 周期惩罚
- Zen 2 前端带宽浪费率 1.39 ops/retired，Skylake 为 1.63（差 17%）
- 非调度 FP 队列：64 条目 × 低成本，使 FPU 可见深度达 192 微操作
- Skylake 后端受限 20.1% vs Zen 2 15.1%；Skylake RS 满是主要瓶颈
- Zen 2 L2 hitrate 明显高于 Skylake，IPC 与 L2 hitrate 正相关可从图中直接观察
- op cache 命中率与 IPC 相关性弱，CBR15 场景下前端带宽不是瓶颈

## 链接到的概念

- [[zen2-microarchitecture]]
- [[branch-predictor-design]]
- [[cpu-scheduler-design]]
- [[cache-friendliness]]
- [[cpu-performance-formula]]
- [[benchmark-methodology-end-to-end]]

## 原文

- 链接：https://chipsandcheese.com/p/analyzing-zen-2s-cinebench-r15-lead
- 本地：`raw/articles/chipsandcheese.com/2021-02-22_analyzing-zen-2s-cinebench-r15-lead.md`
