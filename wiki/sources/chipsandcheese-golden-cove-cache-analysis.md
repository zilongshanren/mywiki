---
tags: [source, cpu, 缓存, intel, golden-cove, champsim]
date: 2026-04-27
sources: 1
---

# Going Armchair Quarterback on Golden Cove's Caches（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 2 月的文章，用 ChampSim 仿真器系统评估"如果 Golden Cove 换用不同缓存配置会怎样"，是对已有 [[golden-cove-microarchitecture]] 测量结论的假设性延伸。

## 摘要

文章对 214 条指令追踪（SPEC2006、SPEC2017、Qualcomm 混淆追踪）分别模拟 L1D、L2、L3 的参数变体，得出以下核心判断：Golden Cove 的 L1D 延迟偏高（5 周期），如果换成 Skylake 的 32 KB 4 周期 L1D，204/214 追踪性能提升；L2 容量从 1.2 MB 缩减到 Zen 风格的 512 KB 则效果相反，hitrate 损失大于延迟收益；L3 如果锁回 Sandy Bridge 的核心时钟域（~30 周期），可普遍提升性能。VCache 方案（90 MB L3）效果两极分化：少数追踪（libquantum、lbm）获得 50–90% IPC 提升，但 111/214 追踪反而因延迟增加而退步。

## 关键要点

- 小而快的 L1D 赢过大而慢的（32 KB 4 周期 vs 48 KB 5 周期），因大多数工作集已驻留 32 KB
- Phenom 风格 64 KB 2-way L1D 在多数追踪中更好，但 2-way 组相联导致热 set 冲突，有少数极端负例
- L2 容量是金科玉律：1.2 MB 大 L2 是 Golden Cove 的设计亮点，弥补了高延迟 L3
- L3 延迟降低到 Zen 3 水平（Zen 3 L3 @ 核心时钟）可带来整体 IPC 提升
- Apple M1 的缓存配置（128 KB L1D + 3 周期延迟 + 超大 L2）在仿真下可提供等效一代性能跃升，但 M1 整体无法复制（高时钟 vs 低功耗的设计空间对立）
- 文章作者建议 Intel 最可行的改进：将 L3 重新锁定到核心时钟域，代价是 iGPU 共享场景下功耗略增

## 链接到的概念

- [[golden-cove-microarchitecture]]
- [[cache-size-vs-latency-tradeoff]]
- [[gracemont-microarchitecture]]
- [[zen2-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/going-armchair-quarterback-on-golden-coves-caches
- 本地：`raw/articles/chipsandcheese.com/2022-02-11_going-armchair-quarterback-on-golden-coves-caches.md`
