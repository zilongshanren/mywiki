---
tags: [source, cpu, amd, zen4, gaming, profiling, performance-counter]
date: 2026-04-27
sources: 1
---

# Hot Chips 2023: Characterizing Gaming Workloads on Zen 4（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 9 月的文章，借助 Zen 4 新增的 pipeline slot 级性能计数器，以 Elder Scrolls Online 和 CoD Black Ops Cold War 为测例，解剖 [[computer-systems/zen4-microarchitecture|Zen 4]] 在实际游戏负载下的前端/后端瓶颈分布。

## 摘要

两款多人游戏的共同特征是：IPC 低、前端瓶颈占主导、后端受内存延迟拖累。Zen 4 有效 IPC 仅在其 6-wide 理论峰值的一小部分——大量 pipeline slot 被前端延迟（latency bound）和无效预测（bad speculation）消耗。前端延迟的根源是极高的分支密度（每 4-5 条指令一个分支），即使微操作缓存命中率 70-81%，L1 BTB 外溢和 indirect branch 惩罚仍造成可观损失。后端主要受 load 延迟拖累，ROB 经常填满是设计平衡良好的体现。数据侧 3D VCache 的 96MB L3 大幅吸收 L2 miss，有效降低后端停顿。MAB 占用率通常低于 4，说明瓶颈是延迟而非带宽。作者指出 AMD 在关键领域做了正确的设计取舍，但 store queue 偏小、BTB 规模与 Golden Cove 仍有差距。

## 关键要点

- 游戏负载：前端 latency bound 占比最大，每 4-5 条指令一个分支是主因
- 微操作缓存命中率 70-81%，但 L1i MPKI 17-20，分支预测惩罚积累明显
- 后端：ROB 经常填满（证明设计平衡），store queue 较 load 侧更突出
- MAB 平均占用 <4，确认是延迟而非带宽受限
- DRAM 平均延迟远低于 100ns，内存控制器不构成瓶颈
- Zen 4 的 pipeline slot 级计数器（仿 Intel TMAM）是新工具，首次实现此精度的 AMD 分析

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/dispatch-stall-breakdown]]
- [[computer-systems/littles-law-reorder-buffer]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/hot-chips-2023-characterizing-gaming-workloads-on-zen-4
- 本地：`raw/articles/chipsandcheese.com/2023-09-06_hot-chips-2023-characterizing-gaming-workloads-on-zen-4.md`
