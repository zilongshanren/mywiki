---
tags: [source, cpu, amd, magny-cours, hypertransport, opteron, numa, 互联]
date: 2026-04-27
sources: 1
---

# AMD's Magny Cours and HyperTransport Interconnect（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 7 月的文章，通过对 Opteron 6180 SE 双路系统的实测，回溯 AMD 2010 年前后的高核心数扩展策略及 HyperTransport 互联表现。

## 摘要

Magny Cours（Opteron 6000 系列）是将两颗 Phenom II X6 die 封装在同一 G34 socket 中的多 die 处理器。两颗 die 通过 HyperTransport（Gen 3，16-bit）连接，带宽约 12.8 GB/s，形成四 NUMA 节点拓扑（双路配置下）。文章测量了跨 HT 节点的延迟（~120–130 ns）、核心间 cache 传输延迟（同 die 约 180 ns、跨 socket 最差超 300 ns）、以及内存带宽瓶颈（实测单 die 约 10 GB/s，仅为 DDR3-1333 理论值的一半）。Northbridge 内部为两级 crossbar（SRI + XBAR），虽然提供低基础延迟（72 ns），但在高带宽争用时延迟骤升。文章最后将 Magny Cours 的设计策略连接到 AMD 后续的 Zen + Infinity Fabric 路线。

## 关键要点

- Magny Cours = 两颗 Phenom II X6 die，通过 HyperTransport 封装在同一 package
- HT Gen 3，16-bit，最高 6.4 GT/s，跨 die 带宽约 12.8 GB/s（另有 8-bit 子链路未使用）
- 双路系统形成四 NUMA 节点，"对角"链路仅 8-bit，带宽约 4.4 GB/s
- 跨节点内存访问延迟约 120–130 ns，本地约 70–80 ns，与同时期 Intel Westmere 双路相当
- 核心间 cache 传输需经 MCT 协调，跨三 die 最差超 300 ns（Intel 通过 L3 probe filter 可避免）
- Northbridge 两级 crossbar（SRI → XBAR），基础内存延迟约 72 ns（极低），带宽争用下急剧恶化
- 单 die 实测 DRAM 带宽仅约 10 GB/s，远低于 DDR3-1333 理论 21.3 GB/s，Northbridge 时钟仅 1.8 GHz 是主因
- HT assist（L3 探测过滤器占用 1 MB/die）可减少广播探测流量
- 策略延续：Zen 1 达到 4 die/socket，最终以 Infinity Fabric 取代 HyperTransport + Northbridge 组合

## 链接到的概念

- [[computer-systems/hypertransport-magny-cours]]
- [[computer-systems/amd-trinity-northbridge-interconnect]]
- [[computer-systems/amd-k8-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-magny-cours-and-hypertransport
- 本地：`raw/articles/chipsandcheese.com/2025-07-11_amds-magny-cours-and-hypertransport-interconnect-a-high-core.md`
