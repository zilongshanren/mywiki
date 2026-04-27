---
tags: [source, cpu, intel, microarchitecture, netburst, pentium4, history]
date: 2026-04-27
sources: 1
---

# Intel's Netburst: Failure is a Foundation for Success（Chips and Cheese）

[[chester-lam]] 发表于 2022 年 6 月的文章，对 Intel Pentium 4 的 NetBurst 微架构（主要聚焦 Prescott/Cedar Mill，90nm/65nm 工艺）进行深度技术剖析，分析其失败的根本原因以及对后续 Sandy Bridge 成功的贡献。

## 摘要

文章通过实际测试（使用 Pentium Extreme Edition 965）系统分析了 NetBurst 各模块：分支预测器（当时领先，但 BTB 未命中惩罚极为惨烈，达 36 周期）、Trace Cache（12K uop 条目，取代传统 L1i，现代 uop cache 的先驱）、PRF 物理寄存器堆方案、分散式调度器、双速 ALU、存储转发（最差情形 165 周期惩罚）、写穿透 L1D（写带宽仅读带宽 1/4）。核心论点：NetBurst 一次引入了太多全新技术，各模块缺陷互相放大，导致整体性能差强人意；但这些技术实践为 Sandy Bridge 铺了路——PRF 方案、uop cache DNA、HyperThreading 调优都源自 NetBurst 时期的积累。

## 关键要点

- NetBurst 的乱序结构直到 Nehalem（2008 年）才被追平，但这是因为它必须追踪大量"僵尸"指令
- Trace Cache 优先路径快，但 L1i miss 退化为 1-wide 解码，与 AMD Athlon 的 64 KB L1i 差距悬殊
- 存储转发惩罚：最差情形（双侧不对齐）165 周期，同期竞品通常 < 30 周期
- 写穿透 L1D 是隐性带宽杀手：写操作立即穿透到 L2，每次写都要占用 L2 带宽
- Sandy Bridge uop cache 在 6-uop line、8-way 组相联等实现细节上与 Trace Cache 有明显传承

## 链接到的概念

- [[netburst-microarchitecture]]
- [[op-cache-decoded-uop-cache]]
- [[branch-predictor-design]]
- [[non-scheduling-queue]]
- [[move-elimination-zeroing-idioms]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-netburst-failure-is-a-foundation-for-success
- 本地：`raw/articles/chipsandcheese.com/2022-06-17_intels-netburst-failure-is-a-foundation-for-success.md`
