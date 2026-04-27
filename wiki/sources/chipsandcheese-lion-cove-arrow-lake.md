---
tags: [source, computer-systems, cpu, intel, microarchitecture, lion-cove, arrow-lake]
date: 2026-04-27
sources: 1
---

# Analyzing Lion Cove's Memory Subsystem in Arrow Lake（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 1 月的文章，深入分析 Intel Lion Cove 核心在 Arrow Lake 平台下的内存子系统表现，并与 Lunar Lake、Raptor Lake 以及 AMD Zen 5 进行对比。

## 摘要

Arrow Lake 给 Lion Cove 提供了更大的资源预算：5.7 GHz 频率、每核 3 MB L2、36 MB 共享 L3，以及经过改善的 DRAM 访问延迟。相比 Lunar Lake，同一颗 Lion Cove 核心在 Arrow Lake 上的 SPEC CPU2017 整数/浮点成绩分别提升 24.8% 和 23.4%，充分说明平台对核心性能的决定性影响。然而 Arrow Lake 的 DRAM 延迟相比上一代 Raptor Lake 出现了倒退，导致 Lion Cove 在内存密集型测试（如 505.mcf、520.omnetpp）中被 Zen 5 拉开差距。文章重点剖析了 Lion Cove 特有的 192 KB L1.5 缓存如何有效承接 L1D miss 流量，在部分工作负载下几乎能取代 L2。最终结论是：Arrow Lake 是 Intel 构建可扩展 chiplet 基础设施的探索，短期性能代价是为长远铺路。

## 关键要点

- Arrow Lake Lion Cove 相比 Lunar Lake 版本性能提升超 24%，主要源于更高频率和更大缓存
- Arrow Lake DRAM 延迟相比 Raptor Lake 有所回退，内存密集型场景不敌 Zen 5
- Lion Cove 的 192 KB L1.5 缓存在高局部性工作负载（如 525.x264）中能承接超过 50% 的 L1D miss
- Zen 5 采用更大更优化的 op cache，decoder 仅处理不足 25% 的 uop；Lion Cove 则依靠 8-wide 硬件解码器
- Arrow Lake 的 chiplet 互连延迟是制约 Lion Cove 性能的主要瓶颈
- Intel 与 AMD 性能监控事件定义截然不同，直接对比需谨慎

## 链接到的概念

- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]
- [[computer-systems/golden-cove-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/analyzing-lion-coves-memory-subsystem
- 本地：`raw/articles/chipsandcheese.com/2025-01-06_analyzing-lion-cove-s-memory-subsystem-in-arrow-lake.md`
