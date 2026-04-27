---
tags: [source, computer-systems, cpu, arm, server, neoverse, graviton]
date: 2026-04-27
sources: 1
---

# Arm's Neoverse V2, in AWS's Graviton 4（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 7 月的文章，在 AWS Graviton 4（96 核 Neoverse V2）实例上通过微基准测试拆解核心结构，并与 Zen 4（Bergamo/Genoa）对比。

## 摘要

Graviton 4 是 AWS 第四代 Arm 服务器芯片，96 颗 Neoverse V2 核通过 CMN-700 mesh 互联，仅配 36 MB L3。文章从系统架构（双路延迟与带宽、DDR5-5600 12 通道）到单核微架构（分支预测、FP 执行、内存子系统）逐层实测。关键发现：Graviton 4 运行在 2.8 GHz 的低频下，与 Zen 4 在 IPC 上大致持平，但频率差距导致整体性能弱于 Zen 4；store forwarding 仅支持对齐子集，弱于 Intel/AMD；L2 11 周期延迟优秀，但 L3 68 周期（25 ns）较慢；benchmark 中 7-Zip 竞争力不错，libx264 则因向量宽度劣势而落后。

## 关键要点

- 96 核 CMN-700 mesh，核间延迟 30–60 ns（无簇边界）
- 双路跨 socket 延迟媲美 Sapphire Rapids，跨 socket 带宽弱于 Zen 4
- TAGE 8 分量分支预测，triple-BTB（nano+8K+14K），分支覆盖能力出色
- Graviton 4 禁用了 2 条规格书中的 ALU，实际为 4 ALU
- L1D 64 KB（RRIP 替换），L2 2 MB（11 周期），L3 25 ns
- Store forwarding 仅限 64 位 store 的半宽转发
- libx264 中 Bergamo（Zen 4c）单 CCX 领先，7-Zip 中 V2 反超

## 链接到的概念

- [[neoverse-v2-microarchitecture]]
- [[neoverse-n2-microarchitecture]]
- [[branch-predictor-design]]
- [[zen4-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-neoverse-v2-in-awss-graviton-4
- 本地：`raw/articles/chipsandcheese.com/2024-07-22_arms-neoverse-v2-in-awss-graviton-4.md`
