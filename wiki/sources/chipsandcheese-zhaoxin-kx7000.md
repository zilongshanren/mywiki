---
tags: [source, cpu, 兆芯, x86, 国产芯片, 微架构, avx2]
date: 2026-04-27
sources: 1
---

# Zhaoxin's KX-7000（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 4 月 30 日的文章，对兆芯 KX-7000 处理器（世纪大道架构）进行全面微基准测试与架构分析。

## 摘要

文章系统性地测量了 KX-7000 的前端（取指带宽、BTB 延迟、方向预测）、重命名/乱序执行（ROB、调度器、执行单元）、内存子系统（L1/L2/L3 延迟带宽、DRAM 读带宽限制）以及 SPEC CPU2017 性能，最后与 AMD Bulldozer FX-8150 和 Intel Core i5-6600K（Skylake）进行了全面横向对比。核心结论：世纪大道在宏观架构层面取得重要进步（4-wide、>3 GHz、Bulldozer 级性能），但在前端设计、AVX2 内部实现方式、缓存带宽和内存子系统公平性上存在明显的不均衡，整体感觉更像"兼容优先的最低成本 AVX2 实现"而非性能最优设计。

## 关键要点

- 世纪大道：4-wide OoO，192 项 ROB，3.2 GHz，8 核 chiplet 结构，32 MB L3
- AVX2 吞吐与 Haswell 持平，但 256-bit 指令内部拆为 2× micro-op
- BTB 3 周期 taken branch 延迟，无 branch fusion，前端较落后
- L3 延迟 80+ 核心周期，DRAM 读带宽 2 核后不再提升（共享队列饱和）
- SPEC INT 单线程约等于 Bulldozer，FP 单线程领先约 10%
- 多线程性能有时不及 Bulldozer（2011 年设计）

## 链接到的概念

- [[zhaoxin-century-avenue-microarchitecture]]
- [[via-x86-isaiah-lujiazui]]

## 原文

- 链接：https://chipsandcheese.com/p/zhaoxins-kx-7000
- 本地：`raw/articles/chipsandcheese.com/2025-04-30_zhaoxins-kx-7000.md`
