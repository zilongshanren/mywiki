---
tags: [source, cpu, amd, epyc, turin, zen5, server, memory-subsystem]
date: 2026-04-27
sources: 1
---

# AMD's Turin: 5th Gen EPYC Launched（George Cozma / Chips and Cheese）

[[people/george-cozma]] 发表于 2024 年 10 月的服务器 CPU 评测，重点聚焦于 Turin（AMD EPYC 9005 系列）内存子系统的实测数据，基于 AMD EPYC 9575F（64 核）。

## 摘要

Turin 是 AMD 第五代 EPYC，基于 [[computer-systems/zen5-microarchitecture|Zen 5]] 核心。相比于 Genoa（Zen 4），Turin 最重要的内存子系统变化是 GMI3-W 链路：每个 CCD 有两条 GMI 链接至 IO Die（Genoa/桌面 Zen 5 仅一条），且 GMI 写链路从 16B/link 扩宽至 32B/link。这使得单 CCD 的内存带宽显著高于桌面 Zen 5。全插槽 9575F 在读带宽上接近理论峰值 576 GB/s（实测约 99%），写和读改写分别为 435/453 GB/s。时钟表现亮眼：所有 64 核均可在单线程测试中达到 5 GHz，全核并行也能保持 4.3 GHz（轻载如 TLS 业务约 4.9 GHz 全核）。文章将 Turin 定位为稳步迭代（类似 Milan→Genoa），而非代际飞跃，核心 + 内存带宽 + 核数同步升级，高频低核 F SKU 面向传统企业，高核数 SKU 面向超大规模数据中心。

## 关键要点

- GMI3-W：每 CCD 双 GMI 链路 + 写链路 32B（vs 桌面单链路 16B），CCD 内存带宽翻倍
- 12 通道 DDR5（最高 DDR5-6400 1DPC），常规配置 DDR5-6000；双插 DIMMs 降至 4400 MT/s
- 全插槽峰值读带宽约 576 GB/s（实测 ~570 GB/s），接近理论值
- Intra-CCD 延迟 ~45 ns，Inter-CCD ~150 ns，Socket-to-Socket ~260 ns；较 Genoa 略有延迟劣化
- 单线程 5 GHz，全核并发约 4.3 GHz（向量密集）
- Turin 不是飞跃式革命，但高核 + 高频 F SKU 组合覆盖了企业市场的两端需求

## 链接到的概念

- [[computer-systems/zen5-epyc-server]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/numa-multi-socket-design]]
- [[computer-systems/memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-turin-5th-gen-epyc-launched
- 本地：`raw/articles/chipsandcheese.com/2024-10-11_amd-s-turin-5th-gen-epyc-launched.md`
