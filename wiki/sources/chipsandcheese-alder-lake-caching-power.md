---
tags: [source, cpu, cache, power, efficiency, alder-lake, golden-cove, gracemont]
date: 2026-04-27
sources: 1
---

# Alder Lake's Caching and Power Efficiency（Chips and Cheese）

[[chester-lam]] 发表于 2022 年 7 月的文章，通过 Intel RAPL 功耗计数器（MSR 0x611）对 Alder Lake（Golden Cove P 核 + Gracemont E 核）各级缓存的数据传输能量进行量化测量，并与 Haswell、Skylake、Zen 2/3、Tremont、Goldmont Plus 进行对比。

## 摘要

文章建立了一套方法论：在内存带宽基准测试的每个数据点前后读取功耗计数器，换算为每比特传输能耗，从而量化"数据从哪里来对功耗的影响"。核心发现：L2 命中能耗约为 L1 的 2 倍，L3 约为 L2 的 2+ 倍，DRAM 约为 L3 的 4-5 倍。这一规律在所有测试架构上普遍成立。Golden Cove 在 L1/L2 上能耗效率优于 Skylake，且带宽更高；Gracemont 则因共享 L2 的复杂性和拆分 AVX，在 L1/L2 上反而比 Golden Cove 更低效，本质是面积效率设计而非功耗效率设计。

## 关键要点

- DRAM 能耗约是 L3 的 5 倍；保持数据局部性对功耗的收益远大于缩小核心结构
- uop cache 与 L1i 命中能耗相差 < 6.5%，说明 uop cache 的功耗价值主要体现在性能而非节能
- Golden Cove 的大型 L2（1280 KB）是 Intel 应对长环形总线 L3 高能耗的核心策略
- Gracemont 在 DRAM 效率上胜出（小 OoO 引擎等待时更省电），但在缓存命中路径上劣于 Golden Cove
- Tremont（10nm 低频）在所有缓存层级上均比 Gracemont 省电，印证了低频对效率的重要性
- AMD Zen 2/3 RAPL 数据为建模值，非实测，需留意误差

## 链接到的概念

- [[cache-power-efficiency]]
- [[intel-hybrid-alder-lake]]
- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[tremont-microarchitecture]]
- [[cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/alder-lakes-caching-and-power-efficiency
- 本地：`raw/articles/chipsandcheese.com/2022-07-07_alder-lakes-caching-and-power-efficiency.md`
