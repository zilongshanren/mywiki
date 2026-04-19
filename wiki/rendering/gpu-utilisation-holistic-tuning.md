---
tags: [gpu-优化, 瓶颈分析, 渲染工程, 性能]
date: 2026-04-19
sources: 1
---

# GPU 利用率整体调优

现代 GPU 的核心是大量 SIMD 单元（Nvidia SM、AMD WGP），性能目标是让 VALU / SALU 持续忙。实践中 VALU 经常被各种 fixed-function 单元 starve——TEX 读数据、ROP 写 RT、Register File 存 VGPR、各层 cache 喂数据、IA / Raster 的几何输入等。单 drawcall 瓶颈优化到头后就要换视角：**整帧层面跨 pass 看哪些 pass 用了什么资源、哪些空着**，把互补瓶颈的 pass 配对起来。[[kostas-anagnostou|Kostas Anagnostou]] 在 2025 年做过一次完整梳理。

## 单 drawcall 层面的旋钮

- **memory latency bound** → 降 VGPR 提高 [[gcn-wave-occupancy|occupancy]]、或展开循环让 memory read 与 use 之间塞更多 instruction
- **cache thrashing（高 occupancy 的反效果）** → 反而要**主动降 occupancy**：加永不走的 dummy 大分支、或在 compute shader 里分配 dummy LDS
- **LDS dummy 优于 VGPR dummy**：留下 VGPR 让 parallel task 用
- **增 VGPR 分配** 反而能让编译器把 texture load 批量前置减少延迟
- **packing / 压缩 shader input 和 output**（包括 VS export，后者本身也能成瓶颈）
- **Structured Buffer vs Constant Buffer**：N 卡随机访问 Structured Buffer 更快，顺序 / uniform 访问 CB 更快

## Shader 类型选择

pixel / compute / vertex 各有固定功能单元依赖，不是"compute 一定更快"：

- **screen-space 大头、export bound 或有 early-out 发散的 PS** → 改 compute 更快（没 rasterizer / ROP 依赖、有 LDS）
- **写 RT 的任务 PS 可能更快**：GCN Color cache 直写 DRAM 绕开 L2、输出走 DCC 压缩后续读省带宽、享受 hardware VRS、享受 stencil / depth 的 wave 不 spawn 加速
- **compute threadgroup 挂同一 SM / WGP**：利于 cache locality、能配合大 threadgroup LDS
- **PS wave 按屏幕 tile 分多 SM**：launch 模式更规律、可能更快
- **VS wave 在 GCN 每 CU 一个**：locality 差、culled 三角形工作白做，移动 VALU 到 VS 性价比不高

RDNA 还有 **wave size 选择**：PC 驱动默认 compute wave32、pixel wave64；wave intrinsics 重的用 wave64（64 项一次过），发散 shader（stochastic SSR）用 wave32（更早 retire）。SM6.6 的 `WaveSize` 属性让 compute 显式选。主机平台驱动控制更宽松。

## 跨 pass 最大杠杆：Async Compute

[[async-compute|Async compute]] 是把互补瓶颈配对的主工具：

- **VALU bound compute**（GTAO cache + SM bound）配 **fixed-function bound**（Shadowmask RT core bound、z-prepass / shadow pass 几何 bound、gbuffer fill PS export bound）
- DX12 没优先级 / throttling API（Vulkan 有 VK_AMD_wave_limits）——靠 dummy LDS / VGPR、小 threadgroup 手工调
- 图形管线内部 compute 也可能和 pixel/vertex 并行，只要**没 barrier**

## 一条贯穿的免责声明

效果严重依赖 **GPU 架构、shader 编译器、渲染器结构、场景内容**。没有通吃所有平台的规则。关键在**用 profiler 看 bottleneck 图**（Nsight GPU Trace、AMD Radeon Profiler、PIX）把各单元 throughput 画出来，针对当前限制因素对症下药。

## 相关

- [[async-compute]]
- [[vertex-shader-export-bottleneck]]
- [[gcn-wave-occupancy]]
- [[gpu-latency-hiding]]
- [[bottleneck-analysis]]
- [[shader-instruction-cost]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-gpu-utilisation-holistic]]
