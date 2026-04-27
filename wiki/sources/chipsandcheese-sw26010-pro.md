---
tags: [source, computer-systems, hpc, cpu, supercomputer, china]
date: 2026-04-27
sources: 1
---

# China's New(ish) SW26010-Pro Supercomputer at SC23（Chips and Cheese）

[[chester-lam]] 与 [[george-cozma]] 发表于 2023 年 11 月的文章，深度解析中国神威超算体系中的 SW26010-Pro 处理器，在 SC23 超算大会上的架构亮相。

## 摘要

SW26010-Pro 是神威 TaihuLight 的继任芯片，采用六个核组（Core Group，CG）结构，每组含 64 个计算处理单元（CPE）呈 4×4 网格排布，管理核（MPE）负责线程调度与通信。相较上代 SW26010，新芯片提升了向量宽度（512 位）、时钟频率（1.45 GHz → 2.25 GHz）、CPE 暂存区容量（64 KB → 256 KB，其中一半可配置为缓存）以及内存规格（DDR3 → DDR4）。然而其根本性弱点依旧：缺乏多级缓存层次，且 DDR4-3200 双通道的内存带宽与庞大的计算吞吐量严重不匹配，导致 FP32 带宽利用率约为 0.11 字节/FLOP，远低于同期 GPU 竞争对手。文章认为该芯片过度追求 TOP500 排名而牺牲了实用性。

## 关键要点

- 每芯片 6 个 CG，共 6 × 64 = 384 CPE，全芯片含 41,140,224 CPE（107,136 片）
- 内存带宽总计 307.2 GB/s（6 个 DDR4-3200 双通道控制器），与每片 0.11 B/FLOP 的糟糕比例
- 256 KB 暂存区（LDS 风格，无硬件缓存层次）是一大设计妥协
- 网络拓扑为三级树形，每节点对外带宽 10.54 GB/s，弱于富岳（Fugaku）的 34 GB/s/节点
- HPL-MxP 优化需要手动分块跨 NUMA 节点的矩阵数据，而 Frontier/Fugaku 几乎不需要此类繁琐调优
- 文章对比了 Fujitsu A64FX 与 AMD CDNA 2（MI250X），后者具备更均衡的带宽/算力比

## 链接到的概念

- [[sw26010-pro-architecture]]
- [[cdna2-mi200-architecture]]
- [[good-parallel-computer]]
- [[memory-hierarchy]]
- [[numa-multi-socket-design]]

## 原文

- 链接：https://chipsandcheese.com/p/chinas-newish-sw26010-pro-supercomputer-at-sc23
- 本地：`raw/articles/chipsandcheese.com/2023-11-20_chinas-new-ish-sw26010-pro-supercomputer-at-sc23.md`
