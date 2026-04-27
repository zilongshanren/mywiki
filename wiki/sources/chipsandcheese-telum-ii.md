---
tags: [source, computer-systems, ibm, mainframe, cpu, cache, virtual-l3, hot-chips]
date: 2026-04-27
sources: 1
---

# Telum II at Hot Chips 2024: Mainframe with a Unique Caching Strategy（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 9 月的文章，聚焦 IBM Telum II 大型机处理器在 Hot Chips 2024 上发布的虚拟多级缓存架构。

## 摘要

Telum II 是 IBM 为 z 系列大型机开发的最新处理器，运行于 Samsung 5nm，8 核 5.5 GHz，配备 10 个每片 36 MB 的超大 L2（八核各一片、DPU 一片、空闲一片），总计 360 MB 片上缓存，但无传统 L3。IBM 的应对策略是"虚拟化"缓存层级：利用饱和度指标（Saturation Metric）将被驱逐出 L2 的缓存行优先迁移至负载较低的其他 L2 片，从而在全芯片范围内构建一个虚拟 L3；L2 命中率极高，使对所有 L2 片进行广播查找的开销可接受。进一步地，最多 32 个 Telum II 芯片互联时，L3 逐出行可跨芯片保留，形成 2.8 GB 的虚拟 L4（延迟约 48.5 ns）。Telum II 还配备硬件 AI 加速器（在片内）和 DPU（IO 加速）。从测试对比看，单线程可访问的有效 L2 延迟（3.6 ns）和容量远超同时代客户端产品（Qualcomm Oryon 12 MB/5.29 ns），典型应用场景是低线程数、对延迟要求极高的金融交易类工作负载。

## 关键要点

- 8 核 5.5 GHz，Samsung 5nm；10×36 MB L2，共 360 MB 片上缓存，无传统 L3
- 虚拟 L3：饱和度指标驱动 L2 间缓存行迁移，使用中间 LRU 插入策略控制虚拟 L3 占比
- 虚拟 L4：跨最多 32 芯片，可提供约 2.8 GB 总量，延迟约 48.5 ns
- L2 延迟 3.6 ns，优于 Qualcomm Oryon 的 5.29 ns，且容量大 3 倍
- 内置 AI 加速器（片内）与 DPU（IO 卸载）
- 设计哲学与服务器背道而驰：8 核而非堆核，优先单线程缓存容量与延迟

## 链接到的概念

- [[computer-systems/telum-ii-microarchitecture]]
- [[computer-systems/ibm-virtual-cache-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/telum-ii-at-hot-chips-2024-mainframe-with-a-unique-caching-s
- 本地：`raw/articles/chipsandcheese.com/2024-09-08_telum-ii-at-hot-chips-2024-mainframe-with-a-unique-caching-s.md`
