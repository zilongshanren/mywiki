---
tags: [source, computer-systems, cpu, amd, zen4, infinity-fabric, igpu, rdna2, memory-bandwidth]
date: 2026-04-27
sources: 1
---

# AMD's Zen 4, Part 3: System Level Stuff, and iGPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 1 月的文章，是 Zen 4 系列深度测评的第三篇，聚焦系统级特性：Boost 时钟行为、Infinity Fabric 带宽瓶颈、以及 Raphael 平台首次集成的 RDNA2 iGPU 分析。

## 摘要

文章首先分析 Ryzen 7950X 的 Boost 行为，发现两个 CCD 之间存在 100–200 MHz 的时钟差异，且最高频率核心集中在第一个 CCD——与 Zen 2/3 的同类规律一致，暗示 AMD 仅对单个 CCD 进行最高频档的 binning。随后详细测量了 Infinity Fabric 带宽瓶颈：单 CCD 32B/cycle 读链路在 DDR5-6000 高速内存下成为带宽上限，写链路（16B/cycle）的限制更明显。一个反直觉发现：使用 4 线程（每 CCD 2 核）而非全部 32 线程时，写带宽反而更高，原因是过多线程令内存控制器更难优化访问调度。最后分析 Raphael iGPU：仅 1 WGP 的极小 RDNA2 配置，L1 减半（64 KB，而非标准 128 KB）、L2 仅 256 KB，无 Infinity Cache。尽管规模极小，DRAM 访问延迟（~191 ns）优于桌面独立显卡 RDNA2（>250 ns），得益于 iGPU 与内存控制器同在 IO die 上。

## 关键要点

- Zen 4 最高 Boost 核心集中在 CCD0，两个 CCD 频率差约 100–200 MHz
- 单 CCD 32B/cycle Infinity Fabric 读链路是内存读带宽上限；写链路 16B/cycle 更紧张
- 4 线程 > 32 线程写带宽：过度并行损害内存控制器调度效率（反直觉）
- FCLK 降低 20% → 写带宽降低约对应量，但读带宽仅降 5.8%（读不受 IF 限制）
- Raphael iGPU：RDNA2，1 WGP，L1 64 KB（标准的一半），L2 256 KB，无 Infinity Cache
- iGPU DRAM 延迟 ~191 ns，优于桌面 RDNA2 >250 ns（IO die 与内存控制器同位）
- 首个高性能 AMD 桌面平台同时提供高核心数 CPU 和 iGPU（Raphael / AM5）

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[rendering/rdna3-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-zen-4-part-3-system-level-stuff-and-igpu
- 本地：`raw/articles/chipsandcheese.com/2023-01-05_amds-zen-4-part-3-system-level-stuff-and-igpu.md`
