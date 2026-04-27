---
tags: [source, cpu, arm, aws, graviton, server, microarchitecture]
date: 2026-04-27
sources: 1
---

# Graviton 3: First Impressions（Chips and Cheese）

[[george-cozma]] 与 [[chester-lam]] 发表于 2022 年 5 月的文章，对 AWS Graviton 3 进行首次微架构深度分析，与 Neoverse N1、Zen 3、Ice Lake SP 进行全面对比。

## 摘要

文章通过微基准测试逆向工程了 Graviton 3 的主要微架构参数：分支预测器（BTB 层次、零气泡跳转能力）、前端（4-wide 解码 + 3K uop cache）、重命名宽度（6-wide）、乱序结构（ROB 约 512 条目）、执行单元（4 整数 ALU、3 内存流水线、4 个 128-bit 向量/FP 流水线）以及缓存层次（64 KB L1D、L2/L3 延迟对比前代大幅改善，DDR5 带宽领先但延迟略差）。核心结论：Graviton 3 与 Zen 3 和 Ice Lake 在微架构规模上同一量级，远超 Neoverse N1，但低主频（2.6 GHz）导致实际时间性能仍落后于 x86 竞品。AWS 的策略是用 5nm 低功耗换取计算密度，而非追求单核峰值性能。

## 关键要点

- Graviton 3 分支预测器与 Intel/AMD 旗舰水平相当，micro-BTB 容量超过 Golden Cove
- ROB 约 512 条目，超过 Zen 3（192）和 Ice Lake（352）
- SVE 支持首次进入通用云场景，但 2022 年软件生态几乎为零
- 移位消除能力有限，无法完全消除链式依赖 MOV（Zen 3 和 Ice Lake 均可）
- DDR5 提供约 2× 内存带宽优势，但延迟比 DDR4 竞品差约 10-20 ns

## 链接到的概念

- [[aws-graviton3-microarchitecture]]
- [[sunny-cove-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[neoverse-n1-microarchitecture]]
- [[branch-predictor-design]]
- [[cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/graviton-3-first-impressions
- 本地：`raw/articles/chipsandcheese.com/2022-05-29_graviton-3-first-impressions.md`
