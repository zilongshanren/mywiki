---
tags: [source, chipsandcheese, cpu, cache, power, avx512, mobile, zen3, willow-cove]
date: 2026-04-27
sources: 1
---

# Caching Energy Efficiency Data – Mobile and AVX-512（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 7 月的文章，是其桌面端缓存功耗测试的移动端续篇，新增 Zen 3 移动（Cezanne）、Willow Cove 移动（Tiger Lake-U）以及 Cascade Lake-X HEDT 平台，并首次量化 AVX-512 对缓存能效的影响。

## 摘要

移动端 CPU 受电池和散热约束，必须在更低的功耗预算下工作，即使使用与桌面相同的核心。AMD 的 Cezanne 采用单片封装，避免了 Vermeer chiplet 方案的跨 die 数据搬运开销，实测 L1D 层级的封装功耗仅约 25W（Vermeer 超过 90W），能效远优。Willow Cove 的 AVX-512 在核私有缓存（L1/L2）层级领先，但 AMD 在 L3 和 DRAM 层级重新取得优势。Cascade Lake-X 因高功耗预算牺牲能效，但带宽领先 80%；Rocket Lake vs Kaby Lake 的对比是 AVX-512 能效效益最清晰的案例。

## 关键要点

- 移动端热节流导致频率不稳定，结果难以与桌面端对标，但总体趋势仍清晰
- Cezanne 的单片封装在数据搬运能效上与低功耗 Tremont 相当
- Willow Cove 在指令侧（instruction fetch）能效不如 Cezanne，但向量数据侧占优
- AVX-512 在 L3 及以上层级不再有效，因为 L3 带宽已由 AVX（256-bit）饱和
- Intel 的 HEDT/高功耗平台并非能效优化设计，不应用于能效评估

## 链接到的概念

- [[avx512-cache-efficiency]]
- [[cache-power-efficiency]]
- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/caching-energy-efficiency-data-mobile-and-avx-512
- 本地：`raw/articles/chipsandcheese.com/2022-07-15_caching-energy-efficiency-data-mobile-and-avx-512.md`
