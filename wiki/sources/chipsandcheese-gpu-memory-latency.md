---
tags: [source, chipsandcheese, gpu, 内存延迟, rdna2, ampere, 微基准]
date: 2026-04-19
sources: 1
---

# Measuring GPU Memory Latency（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 4 月发表于 [[chips-and-cheese]] 的 GPU 内存延迟实测文章，使用 OpenCL pointer chasing 基准测量多代 AMD 和 Nvidia GPU 的各级缓存延迟，并与 CPU（Intel Haswell）对比。

## 摘要

文章以"GPU 也有缓存层次，为何不像 CPU 一样系统实测"为出发点，使用 pointer chasing 微基准穿越不同大小的数组，使访问落在不同缓存层上，从而测出各级缓存的延迟。核心发现是 RDNA 2（RX 6800 XT）的缓存层次极具竞争力：L0→Infinity Cache 的延迟（~86 ns）低于 Ampere L1→L2 的延迟（>100 ns），而 RDNA 2 穿越三级缓存到 VRAM 的总延迟与 Ampere 两级缓存到 VRAM 相当，暗示 Infinity Cache 是一个增量延迟仅约 20 ns 的"廉价 L3"。CPU（Haswell DDR3-1600）访问 DRAM 的往返延迟仅 63 ns，GPU 的 226 ns 高出近 4 倍，揭示了 GPU 依赖线程级并行隐藏延迟的根本原因。

## 关键要点

- RDNA 2 Infinity Cache 延迟：~20 ns over L1 hit，低于 Ampere 的 L2 延迟（>100 ns）
- RDNA 2 vs Ampere 最终 VRAM 延迟相近，RDNA 2 多走两级缓存却无额外代价
- Haswell DRAM 往返 63 ns；RDNA 2 GDDR6 往返 226 ns；差距约 3.6 倍
- Maxwell/Pascal 延迟相近；Turing 引入 L1 后结构开始向 Ampere 靠近
- AMD 历代 L0/L1/VRAM 延迟持续降低：Terascale → GCN → RDNA 2
- OpenCL pointer chasing 方法可直接复用于 CPU 延迟测量，跨平台对比公平

## 链接到的概念

- [[gpu-memory-hierarchy-latency]]
- [[memory-hierarchy]]
- [[gpu-latency-hiding]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/measuring-gpu-memory-latency
- 本地：`raw/articles/chipsandcheese.com/2021-04-16_measuring-gpu-memory-latency.md`
