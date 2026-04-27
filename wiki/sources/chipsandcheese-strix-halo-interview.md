---
tags: [source, computer-systems, amd, soc, strix-halo, igpu, apу, interview]
date: 2026-04-27
sources: 1
---

# AMD's Strix Halo - Under the Hood（George Cozma / Chips and Cheese）

[[people/george-cozma]] 发表于 2025 年 1 月的访谈文章，在 CES 2025 现场与 AMD Senior Fellow Mahesh Subramony 深度对话，揭示 Strix Halo SoC（Ryzen AI Max）的关键架构决策。

## 摘要

Strix Halo 是 AMD 历经四代迭代、将旗舰 CPU 与高性能 iGPU 整合在单一封装上的里程碑产品。其核心架构革新体现在两方面：一是将 CCD 与 SoC tile 之间的互连从串行 GMI SERDES 换为扇出封装层上的"海量导线"直连——时钟频率从 20 GHz 降至 1-2 GHz，但功耗更低、延迟更小、无状态可即时开关；二是 CPU 核心配备完整 512-bit 数据路径的 Zen 5，以换取更低功耗而进行 binning（牺牲峰值频率）。32 MB MALL（Last Level Cache）目前仅供 GPU 写入以放大图形带宽，但架构上支持灵活配置，未来可通过固件调整分配给 NPU/VCN 等其他计算引擎。

## 关键要点

- 互连从 GMI SERDES 改为扇出封装直连：32 byte/cycle 双向带宽不变，但功耗、延迟大幅降低
- Zen 5 核心保留完整 512-bit FPU，通过 binning 换取移动端效率
- 32 MB MALL 当前仅 GPU 写入安装，但整个 fabric 保持一致性，CPU 读取会查询 MALL
- 一致性点位于 Data Fabric 与内存控制器之间，非 MALL
- 仅需 1-2 个 CPU 线程即可打满 DRAM 带宽（streaming 场景）
- Fabric 时钟与 LPDDR 速率匹配，避免异步接口开销

## 链接到的概念

- [[computer-systems/strix-halo-soc]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/cdna3-mi300x-architecture]]
- [[computer-systems/mcm-gpu-design]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-strix-halo-under-the-hood
- 本地：`raw/articles/chipsandcheese.com/2025-01-13_amd-s-strix-halo-under-the-hood.md`
