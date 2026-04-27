---
tags: [source, computer-systems, gpu, amd, gcn, architecture-history]
date: 2026-04-27
sources: 1
---

# GCN, AMD's GPU Architecture Modernization（Chips and Cheese）

[[chester-lam]] 发表于 2023 年 12 月的文章，以 Tahiti（HD 7950）与 Hawaii（R9 390）为硬件样本，系统回顾 GCN 架构的设计哲学与历史意义。

## 摘要

GCN（Graphics Core Next）是 AMD 对 Terascale 的全面颠覆：将巨型 SIMD + VLIW 替换为四个小型 16-wide SIMD 的 Compute Unit，执行模型转向标量/线程级并行，缓存体系也从面向图形的只读纹理缓存升级为支持写回的通用层次。GCN 的调度策略依靠线程级并行（多线程多发射），而非 Terascale 的编译器 VLIW 打包。文章通过 VkFFT 测试展示 GCN 在大型 FFT 负载下的带宽优势，并剖析 GCN 在小三角形、短 draw call 场景中对 Kepler 的劣势原因。

## 关键要点

- Compute Unit 结构：4 × SIMD16（64 FP32 ops/cycle），10 线程槽/SIMD，共跟踪 40 wavefronts
- 缓存层次：16 KB 向量 L1（写通，LRU，64B/cycle）+ 16 KB 标量缓存（4 CU 共享，低延迟）+ 分片 L2（写回）
- 64 KB LDS（软件管理 scratchpad），32 banks × 32 bit = 128 B/cycle
- 多发射：最多 5 指令/cycle（跨不同类别的线程），依赖 occupancy 而非编译器
- GCN 对大规模 compute 友好，但光栅填充率受限（Tahiti 仅 2 个光栅器 / 32 CU）
- GCN 的 DNA 延续至 CDNA 系列；scalar datapath 被 Turing 借鉴

## 链接到的概念

- [[gcn-architecture]]
- [[gcn-wave-occupancy]]
- [[cdna2-mi200-architecture]]
- [[gpu-latency-hiding]]
- [[gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/gcn-amds-gpu-architecture-modernization
- 本地：`raw/articles/chipsandcheese.com/2023-12-05_gcn-amds-gpu-architecture-modernization.md`
