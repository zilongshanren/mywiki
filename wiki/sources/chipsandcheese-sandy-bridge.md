---
tags: [source, cpu, intel, sandy-bridge, microarchitecture, cache, ring-bus]
date: 2026-04-27
sources: 1
---

# Sandy Bridge: Setting Intel's Modern Foundation（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 8 月的文章，通过微基准测试系统分析 Intel Sandy Bridge 微架构，追溯其对后续十年 Intel 架构乃至 AMD、ARM 设计的深远影响。

## 摘要

Sandy Bridge（2011 年）是 Intel 从 P6/Netburst 两条线索提炼出的全新架构，引入了 micro-op cache（1536 entry，4 source 供给路径）、PRF 乱序执行引擎（支持 256-bit AVX）、环形总线分布式 L3，以及大幅改进的分支预测器（BPB capacity 翻倍至 4096、更快 BTB L0）。环形总线取代了 Nehalem 的中央 Global Queue，L3 延迟从 Nehalem 的约 17.5 ns 降至 10.3 ns，带宽近乎翻倍。文章将 Sandy Bridge 的关键设计（micro-op cache、分布式 L3）与后来 AMD Zen 系列和 ARM 高性能核的雷同设计相互印证，指出 Sandy Bridge 是现代高性能 CPU 设计的奠基性范本。

## 关键要点

- Micro-op cache（1536 entry，虚地址索引）：绕过传统 fetch/decode 路径，降低功耗并提升带宽；Intel、ARM、AMD 后来均采用类似策略
- 分布式环形总线 L3：每个 L3 切片处理本地请求，L3 延迟从 Nehalem ~17.5 ns 降至 ~10.3 ns
- PRF 乱序执行引擎：取代 P6 的 ROB 存储值方案，支持 256-bit AVX 的完整宽度寄存器
- 分支预测器大幅改进：BTB 从 2048 扩至 4096 entry，L0 BTB 可处理 8 个 1 周期分支
- 双 AGU 是当时瓶颈；Haswell（2013）扩至三 AGU，AMD Zen 2（2019）才跟上
- Zeroing idiom 识别但缺乏 move elimination（Ivy Bridge 才加入）
- Sandy Bridge 架构血脉延续至今（Alder Lake、Raptor Lake 可追溯的迭代演进起点）

## 链接到的概念

- [[computer-systems/sandy-bridge-microarchitecture]]
- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/skylake-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/sandy-bridge-setting-intels-modern-foundation
- 本地：`raw/articles/chipsandcheese.com/2023-08-05_sandy-bridge-setting-intels-modern-foundation.md`
