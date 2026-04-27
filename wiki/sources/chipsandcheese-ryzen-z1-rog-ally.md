---
tags: [source, computer-systems, cpu, amd, hybrid-cores]
date: 2026-04-27
sources: 1
---

# AMD's Mild Hybrid Strategy: Ryzen Z1 in ASUS's ROG Ally（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 2 月的文章，分析 AMD Ryzen Z1 SoC 中 Zen 4 与 Zen 4c 混合核心方案在 ROG Ally 掌机上的具体表现。

## 摘要

Ryzen Z1 将 2 颗高性能 Zen 4 核心与 4 颗密度优化的 Zen 4c 核心集成于同一 L3 簇中。Zen 4c 在架构上与 Zen 4 完全一致，仅通过更紧凑的物理设计将最高频率从 5 GHz 降至 3.55 GHz，以换取更小的核心面积。文章通过大量微基准测试揭示：两类核心共享同一 L3（14.16 ns vs 10.46 ns，因时钟差异导致绝对延迟有别）；当 Zen 4 核心活跃时，Zen 4c 核心还会被降频至 3.3 GHz；LPDDR5 内存延迟约 124 ns，远高于桌面 DDR5；L1 峰值带宽超过 1.329 TB/s。AMD 的"温和混合"策略规避了 Intel 的 ISA 分裂问题（AVX-512 全核支持），但牺牲了 Intel 那种针对低频核心可以优化微架构（如 Gracemont 的 3 周期 L1d）的机会。

## 关键要点

- Zen 4c 与 Zen 4 架构完全相同，仅物理设计不同，AVX-512 全核一致
- 两类核心同在一个 L3 簇；L3 以最快核心频率运行
- Zen 4 核心活跃时，Zen 4c 从 3.55 GHz 降至 3.3 GHz
- LPDDR5-6400 延迟约 124 ns，仅优于 Van Gogh（155 ns）
- 六核 FP32 算力超过 1 TFLOPS，远超 Nintendo Switch 的 Maxwell iGPU
- AMD 混合策略比 Intel/ARM 更保守，工程资源投入更少

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/amd-phoenix-soc]]
- [[computer-systems/van-gogh-steam-deck-apu]]
- [[computer-systems/intel-hybrid-alder-lake]]
- [[computer-systems/vcache-3d-die-stacking]]
- [[computer-systems/zen4c-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-mild-hybrid-strategy-ryzen-z1-in-asuss-rog-ally
- 本地：`raw/articles/chipsandcheese.com/2024-02-12_amds-mild-hybrid-strategy-ryzen-z1-in-asuss-rog-ally.md`
