---
tags: [compute-shader, gcn, amd, shared-memory, 性能优化, gpu]
date: 2026-04-27
sources: 1
---

# AMD GCN Compute Shader：TGSM 访问模式与优化规则

在 AMD GCN 架构的 compute shader 中，线程组共享内存（TGSM，Thread Group Shared Memory，即 OpenCL 中的 LDS / Local Data Share）的访问模式直接决定 compute pass 的性能上限。Wolfgang Engel 在 GDC 2014 的 PostFX pipeline 优化实践中系统测量了三款 Radeon GPU（6770 / 7750 / 7850），总结出一组跨代可靠的经验规则。

## TGSM Bank Layout 与顺序访问

GCN 的 LDS 被分成若干 banks（物理上 32 banks，每个 bank 宽 32 bits）。当同一 wavefront 内的多个线程在同一个 bank 发出不同地址的读写请求时，会产生 **bank conflict**，硬件将请求串行化，吞吐量成倍下降。

最简单的规避策略是**顺序写、顺序读**：每个线程写入/读取步长为 wavefront 宽度倍数的偏移量，使请求均匀散布在不同 banks 上。随机跨步访问是最坏情况，尤其是步长为 2 的幂次时极易与 bank 数对齐，产生系统性冲突。

在 parallel reduction 这类算法里，树状规约的每一层访问步长在减半，需要针对每一层检查 bank 分布，必要时插入 padding（在 LDS 分配时多一格）来错开 bank 映射。

## 循环展开的有条件收益

展开循环（`[unroll]` / `#pragma unroll`）在理论上消除了循环计数器的算术 overhead 和条件分支，同时给编译器更大的指令调度空间。然而在 GCN 上：

- 展开后代码体积膨胀，可能超出指令缓存容量，导致 i-cache miss；小 kernel 展开有益，大 kernel 可能反效果
- 地址算术本身（乘法 + 加法生成 LDS 地址）在 GCN 的 scalar ALU 上相对廉价，但不可忽视——展开后的多份地址计算仍然消耗 SALU 带宽
- 跨两代（GCN 1 → GCN 2，即 6770 → 7850）对比显示，某些原先有益的展开在新一代 GPU 上收益缩小，原因是新一代硬件对循环的动态分支预测更好

实用原则：对内层循环有限展开（展开因子 4~8），外层循环保留循环结构。

## 利用 Wavefront 跳过内存屏障

`GroupMemoryBarrierWithGroupSync()`（HLSL）在完整线程组内同步，代价是整个 wave 停下来等待。在 GCN 架构中，同一 wavefront（64 个线程）内的 LDS 写入对彼此是**自动可见**的——因为所有 64 个线程严格同步推进（SIMT 锁步执行）。

这意味着：如果一次 LDS 写入和随后的读取**只发生在同一个 wavefront 内部**，可以省掉 barrier，只需保证编译器不乱序（`[allow_uav_condition]` 或手工结构化代码使写在读之前完成）。超过一个 wavefront 范围就必须用 barrier。

注意这个技巧依赖 64-wide wavefront，RDNA 引入了 wave32 模式，在此情况下 barrier 省略条件变得更严格。

## 数据预取与打包

**预取**：compute shader 在处理一个 tile 之前，先把公共数据（如 depth、normal、lighting coefficients）集中读入 LDS，后续线程直接从 LDS 取，避免对全局内存的重复读取。代价是 LDS 容量消耗和一次同步 barrier，收益在于：全局内存延迟通常 100–400 周期，LDS 命中仅 ~20 周期。

**打包**：将多个 8/16 bit 的值打包进一个 32 bit LDS 槽，既减少 LDS 使用量（从而提高 occupancy），又通过减少 LDS 事务数间接降低 LDS bank pressure。解包时需要 bit-shift + mask，在 SALU 上几乎免费。

## 相关

- [[computer-systems/gcn-architecture]] — GCN CU 结构：4×16-wide SIMD、40 wavefront 槽、LDS 设计
- [[computer-systems/gcn-wave-occupancy]] — occupancy 对 latency hiding 的影响
- [[rendering/async-compute]] — GCN 的 compute queue 并发能力
- [[rendering/gpgpu-compute-simt-model]] — SIMT 执行模型基础
- [[rendering/software-rasterization-compute]] — Engel 等用 compute 实现软光栅化的更激进应用

## Sources

- [[sources/humus-compute-optimizations-gdc2014]]
