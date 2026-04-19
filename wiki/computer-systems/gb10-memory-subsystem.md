---
tags: [内存子系统, iGPU, arm, 缓存, 异构]
date: 2026-04-19
sources: 1
---

# GB10 CPU 侧内存子系统

GB10 是 Nvidia 与 Mediatek 合作、把 Blackwell 架构塞进 iGPU 的 SoC（DGX Spark 产品形态）。GPU 侧见 [[gb10-gpu-blackwell-igpu]]。CPU 侧共 20 核，分两簇，每簇 5 个 Cortex X925 + 5 个 Cortex A725。X925 跑 3.9–4.0 GHz，A725 跑 2.8 GHz——一个典型的大小核异构配置，但每簇内部混合编排。

## 缓存层次

| 层级 | 容量 | 延迟 | 备注 |
|---|---|---|---|
| A725 L1D | 64 KB | 3–4 cycle | 48 B/cycle |
| A725 L2 | 512 KB / 8-way | 9 cycle / 3.2 ns | 32 B/cycle |
| X925 L1D | 64 KB | 4 cycle | 64 B/cycle |
| X925 L2 | 2 MB / 8-way | 12 cycle | 64 B/cycle |
| L3（共享） | 8 MB（簇 0） / 16 MB（簇 1） | ~56 cycle / 14 ns（X925）；~60+ cycle / 21 ns（A725） | |
| SLC（System Level Cache） | 16 MB | 42 ns / 47 ns | CPU/GPU 共享，兼 CPU 的 L4 |
| DRAM（LPDDR5X @ 8533 MT/s） | — | 113 ns | 256-bit bus |

L3 延迟对 A725 来说偏差（21 ns），但 A725 只给 512 KB L2，意味着很容易踩进 L3。这是面积妥协：A725 本就不负责高单线程性能，压 L2 可以塞更多核心。相反 X925 配 2 MB L2 + 14 ns L3，延迟档位与 Intel Arrow Lake 的 L3 接近，配置更平衡。

## 非对称双簇

两簇硬件并不对称：
- **簇 0**：8 MB L3，外部带宽较窄，像 Strix Halo 的 CCX
- **簇 1**：16 MB L3，外部带宽 >100 GB/s（类似 AMD GMI-Wide），读写路径独立

DynamIQ Shared Unit 120（DSU-120）最多支持 4 条 256-bit CHI 接口，推测两簇配不同的接口数。但核心编排仍然每簇 5+5 混合——Chester 认为，如果把 10 个 A725 全塞进簇 0、10 个 X925 全塞进簇 1，OS scheduler 会更简单，空闲簇也更易整体 power-gate。

## SLC 的真实用途

16 MB SLC 在 CPU 侧 latency 曲线上不明显，因为 L3 比它大。Nvidia 自己的说法是 SLC 旨在"为各引擎之间提供高能效数据共享"——即 CPU/GPU 之间绕过 DRAM 往返。作为 CPU 的 L4 反而是副业。

## DRAM 是亮点

113 ns 的 DRAM 延迟对 LPDDR5X 来说相当好——Strix Halo、Meteor Lake 都在 140+ ns。CPU core 与 memory controller 同 die、以及 8533–9400 MT/s 的总线速度都有贡献。LPDDR5X 此前给人的印象是"比 DDR5 延迟更高"，GB10 展示了 SoC 一体化的优势。

## 带宽与压力

单核 X925 能从 DRAM 拉到 38 GB/s、从 L3 拉到近 90 GB/s；A725 分别是 26 / 55 GB/s。但 256-bit LPDDR5X 的总带宽（~273 GB/s 理论值）单靠 CPU 端打不满——和 Strix Halo 一样，大 iGPU 平台的 CPU 带宽被 iGPU "挤出去"的场景真实存在：测试里 GPU 拉 231 GB/s 时，CPU 侧测延迟能飙到 351 ns；再叠加两个 X925 打满带宽，延迟逼近 400 ns。

## Core-to-core 与一致性

[[cache-coherence-cross-cluster]] 在 GB10 上成本可见：
- X925–X925 同簇：50–60 ns（最好情况）
- A725–A725 跨簇：最高 240 ns
- Strix Halo 跨簇可控制在约 100 ns，GB10 明显更差

DSU-120 内部由 Snoop Control Unit 用 snoop filter 协调同簇一致性；跨簇由 Nvidia/Mediatek 的 High Performance Coherent Fabric 负责。

## 与 Strix Halo 的对位

Chester 的个人评价：等面积更愿意把 32 MB 都做成单级快速 cache，而非 16 MB L3 + 16 MB SLC。但 GB10 赢在 DRAM 延迟和簇 1 的外部带宽，这是 AMD 任何客户端设计都没做到的。

## 相关

- [[gb10-gpu-blackwell-igpu]]
- [[memory-hierarchy]]
- [[cache-coherence-cross-cluster]]
- [[latency-vs-throughput]]

## Sources

- [[sources/chipsandcheese-gb10-cpu-memory]]
