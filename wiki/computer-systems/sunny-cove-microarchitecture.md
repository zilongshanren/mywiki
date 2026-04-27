---
tags: [cpu, intel, microarchitecture, out-of-order, ice-lake]
date: 2026-04-27
sources: 2
---

# Sunny Cove 微架构

Sunny Cove 是 Intel 于 2018 年架构日发布、搭载于第十代 Ice Lake 处理器的高性能微架构，是 Skylake 的正式继任者。由于 Intel 10nm 工艺的长期延宕，Sunny Cove 直到 2019 年底才以超低功耗形态亮相，完整桌面版（经 14nm 回炉的 Cypress Cove）迟至 2021 年 Rocket Lake 才出现，此时已面对 Zen 3 的直接竞争。

## 关键设计特征

**流水线宽度提升**：Sunny Cove 将重命名阶段从 Skylake 的 4-wide 提升至 5-wide，这是 Intel 自 2006 年 Merom（3→4-wide）后十余年来首次增加核心宽度。

**乱序结构大幅扩容**：ROB、整数寄存器堆、调度器、分支顺序缓冲等关键结构普遍扩大 50% 以上，在历代 Intel 架构演进中幅度最为突出。

**分支预测器增强**：主 BTB 从 Skylake 约 4K 项略微扩大，取出零气泡跳转的能力从 128 个翻倍至 256 个。前端实现微操作队列内的循环展开（类 trace cache），可以每周期完成两次跳转。

**调度器分散化**：延续 Skylake 的趋势，进一步将加载/存储 AGU 独立出来（各两个专用 AGU），解决了 Haswell/Skylake 中 AGU 争用导致峰值带宽无法持续的问题。

**缓存层次重构**：L1D 从 32 KB 扩至 48 KB（+1 周期延迟），L2 提供 512 KB（Rocket Lake）或 1280 KB（Tiger Lake）两种配置，Tiger Lake 的 L3 改为非包含策略并扩至 3 MB/片，大幅降低了因包含 L2 而浪费容量的问题。

**移位消除与清零识别**：5-wide 的移位消除能力与 AMD 对齐，可处理依赖链上的连续 MOV；XOR r,r 等清零惯用语可在重命名阶段被消除。

**AVX-512 下放客户端**：服务器级别的 AVX-512 首次进入消费级（以裁剪版形式），理论上可将 AVX-512 生态推向更广泛的开发平台。

## 10nm 工艺的致命拖累

Sunny Cove 的设计本是针对 10nm 密度和功耗优化的——更复杂的前端不增加流水线级数，分支预测延迟反而降低。但 Intel 10nm 工艺迟迟无法量产，导致：

1. **产品缺位**：2019-2021 年桌面主力仍是 Skylake 翻新（Comet Lake），直到 Rocket Lake 才由 Sunny Cove 接棒。
2. **14nm 回炉失真**：Cypress Cove（14nm Sunny Cove）核心面积庞大、功耗惊人，仅能上 8 核，与 Zen 3 相比毫无竞争力。
3. **时机错误**：等到 Sunny Cove 真正站稳 Intel 旗舰位置，Golden Cove（Alder Lake P-Core）已紧随其后将其取代。

在 10nm 如期交付的假设场景下，Sunny Cove 的大结构加 AVX-512 配合 5+ GHz 高频，将在 2019-2021 年对 Zen 2 形成压倒性优势。

## 与 Zen 2 的对比

Sunny Cove 几乎在所有维度上结构更大，但"聪明程度"相当。Zen 2 的优势在于：更快的 L3（核心频率运行）、更高的内存带宽效率、以及 TSMC 7nm 工艺带来的功耗优势。如果 Intel 的 10nm 工艺按时成熟，这场竞争将非常接近。

## Sources

- [[sources/chipsandcheese-sunny-cove-intel-lost-gen]]
- [[sources/chipsandcheese-graviton3-first-impressions]]
- [[sources/chipsandcheese-skylake-architecture]]
- [[sources/chipsandcheese-cannon-lake]]
