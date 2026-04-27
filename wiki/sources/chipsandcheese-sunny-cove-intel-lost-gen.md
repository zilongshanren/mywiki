---
tags: [source, cpu, intel, microarchitecture, sunny-cove, ice-lake]
date: 2026-04-27
sources: 1
---

# Sunny Cove: Intel's Lost Generation（Chips and Cheese）

[[chester-lam]] 发表于 2022 年 6 月的文章，是 Chips and Cheese CPU 微架构深度系列的第一篇，对 Intel Sunny Cove（Ice Lake / Rocket Lake）进行全面技术解析，并深入剖析 10nm 工艺失败对该架构命运的影响。

## 摘要

文章系统覆盖 Sunny Cove 的各个流水线阶段：分支预测器（BTB 零气泡能力翻倍至 256 条目，单级快速预测）、前端（uop cache 从 1.5K 扩至 2.3K）、重命名（从 Skylake 4-wide 首次提升至 5-wide，移位消除能力与 AMD 对齐）、乱序结构（ROB 等核心结构普遍扩大 50%+）、调度器（进一步分散化，独立 AGU 对消除峰值带宽瓶颈）、缓存（48 KB L1D、双 L2 配置、Tiger Lake 非包含 L3）。核心论点：Sunny Cove 是 Intel 自 Sandy Bridge 以来最大幅度的微架构升级，技术上完全有能力与 Zen 2 竞争乃至压制；但 10nm 工艺的持续失败使它从未得到公平竞争的机会，最终在 Golden Cove 接棒前就被遗忘。

## 关键要点

- 5-wide 是 Intel 自 2006 年 Merom 以来首次提升核心宽度
- Sunny Cove 的 14nm 回炉版（Cypress Cove/Rocket Lake）核心面积庞大、功耗惊人，8 核上限直接输掉多线程竞争
- 如果 10nm 按时成熟，Sunny Cove + AVX-512 + 5+ GHz 将形成 2019-2021 年的压倒性优势
- Tiger Lake 的非包含 L3 解决了因包含 L2 导致缓存容量浪费的问题
- Sandy Bridge 微操作缓存与 NetBurst Trace Cache 在内部结构上有明显继承关系

## 链接到的概念

- [[sunny-cove-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[netburst-microarchitecture]]
- [[branch-predictor-design]]
- [[op-cache-decoded-uop-cache]]
- [[move-elimination-zeroing-idioms]]

## 原文

- 链接：https://chipsandcheese.com/p/sunny-cove-intels-lost-generation
- 本地：`raw/articles/chipsandcheese.com/2022-06-07_sunny-cove-intels-lost-generation.md`
