---
tags: [gpu, intel, xe-hpg, arc, a770, rendering, compute]
date: 2026-04-27
sources: 1
---

# Xe-HPG 架构（Intel Arc）

Intel Arc A770 所基于的 Xe-HPG 架构是 Intel 第三次冲击独立显卡市场的产品（此前有 i740 和夭折的 Larrabee）。Xe-HPG 源自 Intel 集成显卡的 Xe-LP 架构血统，增加了硬件光追、矩阵单元，并设计为可扩展到更大配置。A770 配置 512 EU（4096 FP32 lanes），定位中端独显市场。

## 基本构建单元

Xe Core（旧称子切片）是 Xe-HPG 的基本计算单元，内含 16 个 Vector Engine（VE）和共享的 L1 缓存与指令缓存，类比于 Nvidia 的 SM 或 AMD 的 WGP。每个 VE 是 8-wide FP32 通道，两个 VE 共享一个"Send"端口（内存访问）——这意味着一个 Xe Core 有 8 个 Send 端口同时竞争 L1 缓存访问权，内存子系统复杂度高于 Nvidia SM（4 个 SMSP）或 AMD CU（2 个 SIMD）。

VE 的设计血统可追溯至 Ivy Bridge 时代 8-wide 的 EU，当时 Intel 需要以极小增量扩展 iGPU 配置（最少 6 EU = 48 FP32 lanes）。这种高度细分的架构在 Xe-HPG 扩展到大型独显时带来了低占用度下的带宽调度困难。

## 内存层次

A770 采用较为激进的大容量缓存策略：

- **L1 缓存**：至少 192 KB（Intel 和 Nvidia 都允许 L1 与本地内存共享同一 SRAM 池，驱动动态分配）
- **L2 缓存**：16 MB，远大于 Nvidia（RTX 3060 Ti 的 2 MB）和 AMD（RDNA 2 变体），延迟接近 Nvidia 同级水平
- **VRAM**：256-bit GDDR6，VRAM 延迟明显高于 AMD RDNA 2 和 Nvidia Ampere，接近十年前老产品水平

大容量 L2 是 Intel 应对自身 VRAM 高延迟的主要手段：通过提高 L2 命中率，减少对高延迟 VRAM 的访问频率。在高占用度下，A770 在 L2 带宽方面表现出色，能与竞争对手媲美甚至领先。

## 占用度依赖问题

A770 最根本的性能特征是**对高占用度的强烈依赖**。在低占用度（单 workgroup 或极少 Xe Core 工作）下：

- 单 Xe Core 的 VRAM 带宽仅约 8 GB/s，远低于 AMD RDNA 2 WGP（63 GB/s）和 Nvidia Ampere SM（34.4 GB/s）
- L2 带宽扩展性极差，在相同并行度下落后于 AMD Infinity Cache 和 Nvidia
- 无法通过增加 workgroup 数量线性达到峰值带宽；A770 在全部 32 个 Xe Core 满载时仍无法饱和其 VRAM 带宽

这一特性的根源可能在于 Xe Core 内的循环调度方案：Intel 的 OneAPI 优化指南指出 VE 按轮询（round-robin）方式获得内存访问机会，若占用度低、活跃 VE 少，则总线利用率严重不足。

在 512 workgroups（每 Xe Core 16 个 workgroup）的高占用度测试中，A770 才能展示出具有竞争力的缓存带宽和 VRAM 带宽。这解释了 A770 为何在高分辨率游戏（大量像素着色器并行）中表现较好，而在需要处理大量小型 Dispatch 调用的场景（如 GHPC 中的帧）中性能欠佳。

## 执行性能

FP32 加法吞吐表现合理，但 FMA 吞吐未达到理论值（实测约为理论值的某分数），与 Terascale 2 相比也处于劣势。执行延迟方面，FP32 加法延迟可接受，但 FMA 延迟高于 AMD 和 Nvidia 现代 GPU，需要更高的占用度才能充分隐藏。整数加法吞吐合理，但与 Nvidia Ampere 相比 INT32 吞吐比（FP32 lane 比）偏低，INT32 乘法尤其薄弱。

## PCIe 带宽

测试平台为 PCIe 3.0（非 4.0），但启用了 Resizable BAR。在此配置下，A770 的 CPU↔GPU 传输带宽接近 GTX 980 Ti 水平，正常但并不出色。

## Xe-HPG vs GCN/Vega

A770 与 AMD Vega（Radeon VII）有相似的高占用度依赖特征：两者都需要大量并行工作才能充分发挥，且都以高计算吞吐为卖点。区别在于 A770 用 16 MB GDDR6 L2 替代了 Vega 的 HBM，以缓存换带宽。在高占用度下，A770 的 L2 带宽优势明显；在低占用度下，Radeon VII 由于 HBM 带宽足够宽，扩展性更好。

## 相关

- [[ada-lovelace-architecture]]
- [[cdna2-mi200-architecture]]
- [[gcn-wave-occupancy]]
- [[gpu-latency-hiding]]
- [[gpu-memory-hierarchy-latency]]
- [[gpu-latency-microbench-methodology]]
- [[async-compute]]
- [[gpu-queues-vs-dispatch-execution]]
- [[gpu-latency-hiding]]

## Sources

- [[sources/chipsandcheese-arc-a770]]
