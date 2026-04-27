---
tags: [渲染, GPGPU, 计算着色器, SIMT, wave, 线程组, WebGPU, HLSL, WGSL]
date: 2026-04-27
sources: 1
---

# GPGPU 计算：SIMT 模型与 Compute Shader 基础

GPGPU（通用 GPU 计算）将图形硬件用于任意并行工作负载。现代 GPU 并非真正意义上的"图形处理器"，而是**高度并行的通用处理器**，核心单元被称为 Stream Processors（AMD）、CUDA cores（NVIDIA）或 GPU cores（Apple M 系列）。它们针对吞吐量优化，不擅长延迟密集型或高度分支的任务。

## SIMT 执行模型

GPU 采用 **SIMT（Single Instruction Multiple Thread）** 架构，一组线程以锁步（lock-step）方式执行相同指令，仅在当前 thread ID 和可访问的共享数据上有所不同。这组硬件级别的线程称为：

- **Wave**（DirectX/通用）
- **Warp**（NVIDIA CUDA）
- **Wavefront**（AMD）
- **SIMD Group**（Apple Metal）
- **Subgroup**（Vulkan）

在 RDNA3 和近年 NVIDIA 硬件上，wave 宽度为 32 线程；老款 AMD 硬件为 64 线程。

## 线程层级与调度

一次 `Dispatch` 调用以 **workgroup（线程组）** 为单元分发任务。单个 workgroup 通常包含 32–256 个线程（推荐与 wave 大小对齐，即 32 或 64）。Metal 是唯一允许在 dispatch 时指定 threads-per-group 的 API，其余 API 均需在着色器内声明。

每个线程可访问的内置 ID（以 WGSL 为例）：

```wgsl
@builtin(local_invocation_id)    localInvocationID   // 组内线程 ID
@builtin(workgroup_id)           workgroupID          // 当前组 ID
@builtin(global_invocation_id)   globalInvocationID   // 全局线程 ID（"像素"）
@builtin(local_invocation_index) localInvocationIndex // 组内线性 index
@builtin(num_workgroups)         numWorkgroups         // Dispatch 参数
```

## 组共享内存（LDS）

同一 workgroup 内的线程可通过**组共享内存**（Group Shared Memory，在 AMD RDNA 上即 LDS）交换数据。这是实现前缀和（prefix sum）、Kogge-Stone / Brent-Kung 扫描算法、Radix binning 以及 BVH 构建等高阶算法的基础。数据越靠近线程（本地变量 → 寄存器 → LDS → L2 → 显存），访问越快，缓存层级规则同样适用于 GPU。

## 原子操作

`atomicAdd`、`atomicMin`/`atomicMax`、`atomicXor` 等原子操作允许多线程安全写入同一内存位置，但串行化代价显著——比普通读写慢约 10 倍。适合用于全局 histogram、scatter/compaction 等算法的最终写阶段，不适合在热路径频繁调用。

## Wave Intrinsics

Shader Model 6.0（HLSL）和 GLSL（subgroup extensions）提供了 Wave Intrinsics，允许在 wave 内部高效交换数据或做 reduction，无需经由 LDS。WGSL 正在推进类似提案。

## 典型应用

- **后处理**：计算着色器可替代传统 fragment pass，在 async compute 下与光栅化并行运行（见 [[async-compute]]）
- **几何处理**：光线追踪 BVH 构建（[[bvh-traversal-hardware]]）、物理仿真顶点更新
- **编码 / 压缩**：视频编码（[[gpu-hardware-video-encoder]]）、BC 块压缩（[[dxt-codebooks-sliding-window]]）
- **材质 / 光照**：如 Nanite 的软光栅路径使用 compute shader 进行 meshlet 绘制

## 与已有概念的关系

[[compute-shader-dispatch-ids]] 深入讲解了 `DispatchThreadID` 的计算方式；[[gpu-register-file-occupancy]] 描述了波占用率（wave occupancy）与吞吐量的权衡；[[gpu-latency-hiding]] 解释了 GPU 如何通过多 wave 在制来隐藏内存延迟。[[directx12-api-overview]] 和 Vulkan 均在 compute pipeline 路径上直接暴露这一模型。

## Sources

- [[sources/alain-gpgpu-compute]]
