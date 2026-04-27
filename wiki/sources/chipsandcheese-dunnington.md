---
tags: [source, computer-systems, cpu, intel, dunnington, penryn, merom, core2, server, p6, uncore]
date: 2026-04-27
sources: 1
---

# Intel's Dunnington: Core 2 Goes Dun Dun Dun（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 2 月的文章，深度解析 Intel Dunnington 服务器芯片及 Merom/Penryn 微架构，并分析 Intel 早期多核 uncore 设计的得失。

## 摘要

Dunnington 是 Intel 2008 年为应对 AMD 服务器市场优势而推出的六核服务器处理器，将三个双核 Penryn 模块集成在一块 503 mm² 的 45nm 芯片上，并配备 16 MB 共享 L3 缓存。文章首先详细分析 Merom/Penryn 微架构：尽管保留 P6 时代的 ROB+RRF 设计，但前端和执行单元全面提升（4-wide 解码、原生 128-bit 向量操作），L2 大容量低延迟是其核心竞争力。Dunnington 的问题在于 uncore：L3 延迟高达 ~37 ns（远高于 AMD），且仍基于老旧的 FSB + Cache Bridge Controller（CBC）架构，与 AMD HyperTransport 的点对点互联差距显著。多线程扩展性非常差，加载两个模块仅带来 53% 性能提升。但文章肯定了 Dunnington 作为从 FSB 到现代 ring bus 过渡节点的历史意义——Nehalem 和 Sandy Bridge 均继承并改进了 Dunnington/Tulsa 中首次实验的 uncore 概念。

## 关键要点

- Penryn 核：4-wide 解码，ROB+RRF OoO，3 周期 L1D，~15 周期 L2，L2 容量 3–6 MB，远优于同期 AMD L3
- Penryn L/S：一 load AGU + 一 store AGU（vs AMD 三 AGU 均可做 load），AGU 利用率不均衡
- Penryn 4K page 惩罚极重：load 越 4K 边界 163 周期，store 218 周期（K10 无此罚则）
- Dunnington uncore：CBC 中心化 hub + 16 MB L3，L3 延迟 ~37 ns，读带宽 ~38 GB/s（6 核分享）
- L3 含 core-valid bits 作为全芯片 snoop filter，L3 miss 即表示数据不在片上任何位置
- 7300 芯片组 MCH：四路 FSB + DDR2 四通道，内置 1M 条目 128-way snoop filter 覆盖四路 socket
- 多核扩展性差：6 核仅比 2 核快约 10–20%，L3/FSB 带宽是瓶颈；需 12 核才能打败 4 核 AMD
- 历史意义：Dunnington 的 inclusive L3 + SDI + CBC 等概念后来演化为 Nehalem 的 global queue 和 Sandy Bridge 的 ring bus

## 链接到的概念

- [[computer-systems/dunnington-penryn-server]]
- [[computer-systems/netburst-microarchitecture]]
- [[computer-systems/numa-multi-socket-design]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-dunnington-core-2-goes-dun-dun-dun
- 本地：`raw/articles/chipsandcheese.com/2023-02-05_intels-dunnington-core-2-goes-dun-dun-dun.md`
