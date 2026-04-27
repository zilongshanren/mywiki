---
tags: [cpu, amd, zen4, hybrid-cores, microarchitecture]
date: 2026-04-27
sources: 2
---

# Zen 4c 微架构

Zen 4c 是 AMD 对 Zen 4 的物理重新设计版本，目标是在保持完整架构不变的前提下大幅缩减核心面积。"c" 代表 compact（紧凑），而非对架构的任何削减。

## 核心策略

AMD 的做法与 Intel 为 Alder Lake 设计 Gracemont 效率核心的策略截然不同。Zen 4c 不引入新的微架构——所有执行管道、FPU 结构、乱序深度、ISA 支持（包括 AVX-512）与标准 Zen 4 完全一致。面积缩减来自物理实现层面：

- 利用低目标频率（~3.5 GHz），使用密度更高的 6T SRAM 替代标准 SRAM，用于 L1 缓存、分支预测存储、TLB 等结构
- 更小的时钟网格
- 其他针对低频目标的物理优化

最终结果是整个核心面积缩减约 35%，而 [[van-gogh-steam-deck-apu]] 时代砍掉 PS5 Zen 2 FPU 管道只换来核心面积缩减 5.8%。

## 频率与缓存的代价

面积节省的代价主要体现在两处：

1. **最高频率**：Zen 4 桌面版可达 5.7 GHz，Zen 4c 上限约 3.55 GHz（移动平台）。更低的频率意味着更高的绝对延迟，即使周期数相同。
2. **L3 缓存容量减半**：服务器版 Zen 4c（Bergamo）每核 L3 容量从桌面 Zen 4 的 4 MB 缩减至 2 MB，以进一步压缩核心面积，使单 CCD 可以容纳 16 核而非标准的 8 核。

## 混合部署：Ryzen Z1

[[sources/chipsandcheese-ryzen-z1-rog-ally]] 详细测试了 Ryzen Z1 中 2 颗 Zen 4（最高 5 GHz）与 4 颗 Zen 4c（最高 3.55 GHz）混合运行的行为。值得注意的是：

- 两类核心共享同一 L3 簇，L3 以最快核心的频率运行
- 当 Zen 4 核心活跃时，Zen 4c 核心会被限频至 3.3 GHz（L3/core 频率比约束所致）
- 由于 ISA 完全相同，AVX-512 优化无需区分核心类型，调度器不必担心 ISA 碎片问题

这与 Intel Alder Lake 禁用 E-Core 上 AVX-512 的做法形成对比。参见 [[intel-hybrid-alder-lake]]。

## 与 PS5 Zen 2 FPU 削减的对比

[[sources/chipsandcheese-ps5-zen2-fpu]] 揭示了 AMD 早期另一种面积优化策略——删减 FPU 执行管道。Zen 4c 的设计思路更系统：针对全核物理设计而非手术式裁减特定执行单元，面积节省效果是前者的 6 倍，且不造成任何功能降级。

## Sources

- [[sources/chipsandcheese-ryzen-z1-rog-ally]]
- [[sources/chipsandcheese-ps5-zen2-fpu]]
- [[sources/chipsandcheese-bergamo-zen4c]] — Bergamo 双路系统实测
