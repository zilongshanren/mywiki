---
tags: [source, 渲染, GPGPU, 计算着色器, SIMT, WebGPU, DirectX12, alain.xyz]
date: 2026-04-27
sources: 1
---

# GPGPU Compute Concepts（Alain Galvan / alain.xyz）

[[alain-galvan]] 发表于 2023 年 1 月的文章，系统介绍 GPGPU 计算的核心概念，以 WebGPU（WGSL）和 DirectX 12 为主要示例 API。

## 摘要

文章首先阐明 GPU 的 SIMT 本质：大量简单核心、高吞吐低延迟的设计哲学，以及 Wave/Warp/Wavefront/Subgroup 等跨 API 术语的统一。随后从 Dispatch 调用的 workgroup 分发模型展开，说明 threadgroup 到 wave 的层级结构，以及 GlobalInvocationID / LocalInvocationID 等内置变量的语义。重点章节包括：组共享内存（LDS）作为算法加速的 scratchpad；原子操作的语义与 10x 性能代价；Barrier 的同步保证；以及 HLSL Wave Intrinsics。文末概述了 Convolution、Histogram、Radix Sort 等典型 compute workload 的分解思路。

## 关键要点

- SIMT 要求算法以"大量线程并行处理数据"的方式重新建模
- Workgroup 大小推荐对齐 wave 宽度（32 或 64），除非数据局部性要求更大的组
- LDS 是 prefetch / privatization / scan 算法的关键基础设施
- 原子操作适合最终写阶段，不适合热路径；考虑用局部变量累积后单次原子写出
- Wave Intrinsics 可替代部分 LDS 通信，减少同步开销（仅 HLSL/GLSL，WGSL 待定）

## 链接到的概念

- [[rendering/gpgpu-compute-simt-model]]
- [[rendering/compute-shader-dispatch-ids]]
- [[rendering/async-compute]]
- [[rendering/gpu-latency-hiding]]
- [[rendering/gpu-register-file-occupancy]]
- [[computer-systems/gpu-latency-microbench-methodology]]

## 原文

- 链接：https://alain.xyz/blog/gpgpu-compute-concepts
- 本地：`raw/articles/alain.xyz/2023-01-19_gpgpu-compute-concepts.md`
