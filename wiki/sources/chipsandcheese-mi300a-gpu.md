---
tags: [source, computer-systems, gpu, amd, mi300a, cdna3, hpc, benchmark, compute]
date: 2026-04-27
sources: 1
---

# Sizing up MI300A's GPU（Chester Lam、George Cozma、Neggles / Chips and Cheese）

[[people/chester-lam]] 等人发表于 2025 年 1 月的文章，通过 OpenCL 微基准与真实 HPC 工作负载，全面评估 MI300A 的 GPU 算力，横向对比 MI300X 和 Nvidia H100。

## 摘要

MI300A 以 6 枚 XCD（228 CU）取代 MI300X 的 8 枚（304 CU），换入 24 颗 Zen 4 核心。文章通过 FP32/FP64/INT32 吞吐、L1/LDS 缓存带宽、全局/局部原子操作、FluidX3D 流体模拟以及 GROMACS 分子动力学等多维评估，结论是 MI300A 的 GPU 侧算力依然远超 H100 PCIe，部分实测甚至超过 MI300X。主要原因在于两者共享同一内存子系统（256 MB Infinity Cache + 5.3 TB/s HBM3），真实工作负载多为内存带宽瓶颈；此外 MI300A 在散热约束相同时可能运行在更高频率。全局原子操作低于预期，推测是跨 XCD 一致性维护带来的额外开销所致。功率目标从 550 W 提升至 760 W 对 FP32/FP16S 的性能提升有限（约 5%），但对 FP16C 和 FP64 计算密集负载可提升 12~15%。

## 关键要点

- FP32 吞吐约 113.2 TFLOPS，H100 PCIe 为 49.3 TFLOPS，MI300A 超出约 2.3×
- L1 缓存带宽和 LDS 带宽与 MI300X 基本持平，均远超 H100
- FluidX3D FP32 模式下 MI300A 与 MI300X 差距仅约 1%（550W），760W 时甚至小幅领先
- 全局原子操作吞吐低于 RX 6900 XT，推测因跨 XCD 需要额外 L2 一致性探测
- GROMACS（STMV benchmark）MI300A 760W 模式比 H100 SXM5 快约 15%
- 24 核 Zen 4 的 AVX-512 吞吐约 2.8 TFLOPS，相较 GPU 侧仅属零头
- MI300A 定位是"带 CPU 的巨型 GPU"，而非传统"带 GPU 的 CPU"

## 链接到的概念

- [[computer-systems/mi300a-apu-memory-subsystem]]
- [[computer-systems/cdna3-mi300x-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/sizing-up-mi300as-gpu
- 本地：`raw/articles/chipsandcheese.com/2025-01-20_sizing-up-mi300as-gpu.md`
