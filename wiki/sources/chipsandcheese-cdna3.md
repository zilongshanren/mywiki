---
tags: [source, computer-systems, gpu, amd, cdna, mi300x, hpc, ai]
date: 2026-04-27
sources: 1
---

# AMD's CDNA 3 Compute Architecture（Chips and Cheese）

[[chester-lam]] 与 [[george-cozma]] 发表于 2023 年 12 月的文章，全面分析 AMD MI300X 的 CDNA 3 架构，包括 chiplet 封装、Infinity Cache 引入、跨 die 一致性机制及 CU 执行单元改进。

## 摘要

CDNA 3 以 MI300X 为旗舰，采用 8 个 XCD（Accelerator Complex Die，每片含 38 个 CU，4 MB L2）+ 4 个 IO Die（含 Infinity Cache 与 HBM 控制器）的复杂 chiplet 封装。最大创新是将 RDNA 系列的 Infinity Cache 引入计算 GPU，以提升带宽而非容量为优先目标（128 片，每片 2 MB，总带宽 17.2 TB/s@2.1 GHz）。通过 Coherent Master/Slave 机制将 Infinity Fabric 一致性扩展到多 XCD，使 MI300X 能以单一统一 GPU 呈现给软件。在执行单元上，CDNA 3 引入更灵活的 FP32 双发射机制，并将每 SIMD 可追踪线程数从 8 扩展到 24，以提升 FP32 利用率。

## 关键要点

- MI300X = 8 XCD（304 CU 总计）+ 4 IO Die，总 L2 32 MB，HBM3 容量 192 GB
- Infinity Cache 专为带宽优化：总理论带宽 17.2 TB/s，远超 DRAM 的 5.3 TB/s
- 跨 die Coherent Slave 含 snoop filter，可追踪所有 XCD L2 的缓存状态
- CDNA 3 双发射依赖线程级并行（而非编译器 VLIW），需更高 occupancy
- 每 SIMD 线程槽 8→24，改善 FP32 双发射机会，但寄存器文件带宽仍是瓶颈
- MI300X 设计的核心挑战：跨 die 带宽限制（IO die ingress 2.7 TB/s vs XCD 需求 4.2 TB/s）

## 链接到的概念

- [[cdna3-mi300x-architecture]]
- [[cdna2-mi200-architecture]]
- [[mcm-gpu-design]]
- [[cache-coherence-cross-cluster]]
- [[gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-cdna-3-compute-architecture
- 本地：`raw/articles/chipsandcheese.com/2023-12-17_amds-cdna-3-compute-architecture.md`
