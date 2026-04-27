---
tags: [source, computer-systems, cpu, intel, meteor-lake, hybrid-arch, cache, latency]
date: 2026-04-27
sources: 1
---

# Previewing Meteor Lake at CES（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 1 月的文章，基于 CES 现场测试数据，对 Meteor Lake 三种核心类型的缓存与内存访问特性进行微基准分析。

## 摘要

文章通过缓存延迟与带宽微基准测试，逐一评测 Meteor Lake 的 P-Core（Redwood Cove）、E-Core（Crestmont）以及低功耗 E-Core。总体结论是：Meteor Lake 缓存层次相比 Raptor Lake 并无显著进步，L3 延迟从 60 → 71 周期略有退步（P-Core），单核内存带宽也从 30 → 25.3 GB/s 下降；E-Core 的 L2 容量减半（4 MB → 2 MB）。低功耗 E-Core 不接入 L3，核间通信延迟极高（近 100 ns 内部，跨 die 更长）。文章认为 Intel 在 Meteor Lake 上以保守策略应对 chiplet 化转变，真正的收益在于低功耗场景下彻底关闭 Compute Tile，而非提升峰值性能。

## 关键要点

- Redwood Cove：48 KB L1D（5 cy）、2 MB L2（16 cy）、L3 71 cy — L3 延迟退步，带宽 81 GB/s（低于 Raptor Lake 的 100 GB/s）
- Crestmont E-Core：32 KB L1（3 cy）、2 MB L2（20 cy，共享 4 核）— L2 容量较 Raptor Lake 减半
- LP E-Core：与 E-Core 逻辑相同，但在 TSMC N6 上实现，不接入 L3，内存延迟 >200 ns
- P-Core L1/L2 带宽仍领先 AMD（3× 256-bit AVX loads/cycle，64 B/cycle L2 接口）
- LP E-Core 核间延迟接近 100 ns（内部）到更高（跨 Compute Tile）
- 芯片变化的真正目的：省电场景关闭整个 Compute Tile，而非优化重负载性能

## 链接到的概念

- [[meteor-lake-chiplet-architecture]]
- [[intel-hybrid-alder-lake]]
- [[cache-size-vs-latency-tradeoff]]
- [[core-to-core-latency-lock-test]]

## 原文

- 链接：https://chipsandcheese.com/p/previewing-meteor-lake-at-ces
- 本地：`raw/articles/chipsandcheese.com/2024-01-11_previewing-meteor-lake-at-ces.md`
