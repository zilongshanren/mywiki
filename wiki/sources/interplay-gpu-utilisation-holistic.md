---
tags: [source, gpu-优化, 瓶颈分析, async-compute, 渲染]
date: 2026-04-19
sources: 1
---

# GPU Utilisation and Performance Improvements（Kostas / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2025 年 8 月 29 日的方法论总结，系统梳理"当单个 drawcall / dispatch 优化到头后，如何跨 pass 看问题、把闲下来的定点单元喂饱"。

## 摘要

GPU 的核心是大量 SIMD 单元（Nvidia SM、AMD WGP），目标是让 VALU 单元忙起来。但 VALU 经常被 fixed-function 单元拖后腿：TEX 读数据、ROP 写 RT、Register File 存 VGPR、各层 cache 喂数据、IA / Raster 几何输入等，任一瓶颈都能 starve VALU。Shadowmap pass 天生 VALU 轻、被 IA（World Pipe）和 VRAM 带宽绑死；深度 mipchain / RT copy 的 compute shader 也没够工作量。**单独优化一个瓶颈 drawcall 做完，就要换视角看整帧**——这是博客核心观点。

单 drawcall 层面能做的事：如果 memory latency bound，降低 VGPR 以提高 occupancy；如果过高 occupancy 引起 cache thrashing 反而要**故意降 occupancy**（加假分支或 dummy LDS 分配）。LDS 分配优于 VGPR 分配——留出 VGPR 可能被并行任务用；增高 VGPR 分配还可能让编译器把 texture load 批量前置减少延迟。packing / 压缩 shader 的 input / output（包括 VS export 本身）、按访问模式挑选 Structured Buffer vs Constant Buffer（随机访问时前者在 N 卡更快），都值得做。

选择 shader 类型也有讲究：screen-space、export bound 或有 early-out 发散的 pixel shader 做成 compute 往往更快（compute 没 rasterizer / ROP 依赖还有 LDS）；但 pixel shader 有 GCN 专用 Color cache 直写 DRAM 绕开 L2、能走 DCC 压缩后续读取节省带宽、能享受 hardware VRS、能走 stencil / depth 的 wave 不 spawn 优化，所以写 RT 的任务 pixel 可能比 compute 更快。工作分发模式也不同：compute 的 threadgroup 全挂在同一 SM 上利于 cache locality（大 threadgroup 可以很好利用 LDS），pixel shader 的 wave 按屏幕 tile 分配到多 SM 可能执行更快；vertex shader 的 wave 在 GCN 上每 CU 一个、locality 不佳且 culled 三角形的工作白做。RDNA 的 wave size 也影响：PC 驱动当前给 compute 选 wave32、pixel 选 wave64，shader 用 wave intrinsics 的话 wave64 能处理 64 项而不是 32；发散执行（如 stochastic SSR）wave32 compute 能更早退役。SM6.6 的 `WaveSize` 属性给 compute 提供了显式控制。

跨 pass 层面最大的杠杆是 [[async-compute]]：把 VALU 饱和 pass（如 GTAO，cache + SM bound）和 fixed-function bound pass（如 Shadowmask RT core bound、z-prepass / shadow pass 几何 bound、gbuffer fill 的 pixel export bound）配对并行，两者抢的是不同资源。DX12 上 async compute 没有优先级 / throttling API（Vulkan 有 VK_AMD_wave_limits），dummy LDS / VGPR 分配和小 threadgroup 可以手工调整。在某些架构上图形管线内部的 compute 也能和 pixel / vertex 并行——只要没 barrier。

一个诚实 disclaimer 贯穿全文：**效果严重依赖 GPU 架构、编译器、渲染器和内容**，作者自己也只能给方向，不能给固定答案。

## 关键要点

- 单 drawcall 优化做完还要跨 pass 看问题——不同 pass 的瓶颈常常互补
- VALU 被 fixed-function 单元 starve 是常见模式——IA、ROP、TEX、cache、RF 都会成为瓶颈
- 降 occupancy 反而能提升性能的场景：cache thrashing、编译器 batch 加载
- LDS 假分配比 VGPR 假分配更友好——留下 VGPR 给并行任务
- shader 类型选择考虑 fixed-function 依赖：screen-space compute 通常优于 pixel，但写 RT 场景 pixel 有 Color cache / DCC / VRS 优势
- 工作分发模式差异：compute threadgroup 挂同一 SM、pixel wave 按 tile、vertex wave 每 CU
- RDNA wave size：compute wave32、pixel wave64；发散 shader 用 wave32、wave intrinsics 密的用 wave64
- Async compute 是跨 pass 优化的主工具：VALU bound 配 fixed-function bound 配对，DX12 缺控制 API，靠 dummy 分配调整

## 链接到的概念

- [[gpu-utilisation-holistic-tuning]]
- [[async-compute]]
- [[gpu-latency-hiding]]
- [[gcn-wave-occupancy]]
- [[vertex-shader-export-bottleneck]]
- [[bottleneck-analysis]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/08/29/gpu-utilisation-and-performance-improvements/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-08-29_gpu-utilisation-and-performance-improvements.md`
