---
tags: [gpu, amd, rdna2, cache, raytracing, infinity-cache, wgp, compute]
date: 2026-04-27
sources: 2
---

# RDNA 2 架构

RDNA 2 是 AMD 2020 年推出的第二代 RDNA GPU 架构，首发产品 RX 6000 系列（Navi 21）是 AMD 十余年来首次能在高性能市场正面挑战 Nvidia 旗舰的产品。它在 RDNA 1 的 WGP 骨架上叠加了三项关键进化：128 MB Infinity Cache、硬件光追加速和更高频率，共同构成 AMD GPU 缓存策略的转折点。

## WGP 结构

每个 WGP（Workgroup Processor）内含 4 个 SIMD，每个 SIMD 拥有 32-wide 执行单元和 **128 KB 向量寄存器文件**，可同时追踪 **16 个 wavefront**（RDNA 1 为 20 个）。缩减 wavefront 数的动机是降低调度器每周期的检查代价，以支持更高频率——RX 6900 XT 的频率远超 RX 5700 XT（同工艺）。每 2 个 SIMD 构成一个 CU，CU 级别共享内存管线和 16 KB L0 向量缓存；纹理单元也位于 CU 层级，光追加速正是挂载在此处。

RDNA 2 的 WGP 可在 **WGP 模式**（128 KB LDS 统一共享）和 **CU 模式**（2×64 KB 各归一对 SIMD）之间切换。LDS 延迟在两种模式下均约 19.5 ns，差别在于 WGP 模式允许更大的协作工作集。

## 四级缓存体系与 Infinity Cache

RDNA 2 采用四级缓存，相比同期 Nvidia Ampere 的两级更为复杂：

| 层级 | 容量 | 特点 |
|------|------|------|
| L0 向量 | 16 KB/CU | 最小，命中率偏低（光追场景仅 55%）|
| L1 | 128 KB/Shader Array | 覆盖多 WGP，光追场景拉高累积命中率 |
| L2 | 4 MB | 全 GPU 共享，低延迟约 80 ns，高带宽 |
| Infinity Cache（MALL） | 128 MB | 独立时钟域，L2 缺失后的最后防线 |

Infinity Cache 的命名来源是 MALL（Memory Attached Last Level）——所有 VRAM 访问都经过它。相比 Nvidia Ampere 直接上 384-bit GDDR6X 的策略，AMD 以大缓存换取 256-bit GDDR6，在显著降低功耗的同时提供竞争力相当的有效带宽。这一策略标志着 GPU 缓存由"辅助工具"升格为"架构核心"，[[rendering/rdna3-architecture|RDNA 3]] 和 [[rendering/ada-lovelace-architecture|Ada Lovelace]] 均继承并延伸了这一方向。

## 光追加速：最低硬件成本方案

RDNA 2 的光追加速通过两条新纹理指令实现，计算能力挂载在纹理单元上：

- 每 CU 每周期 **4 次 box 相交测试** 或 **1 次 triangle 相交测试**
- BVH 遍历完全由常规 compute shader 负责，包括计算射线方向的倒数（3 条额外指令，执行速率仅 1/4）
- 光追 kernel 中每 SIMD 占用率受向量寄存器文件限制，通常仅 10/16（RDNA 3 提升至 12/16）

这是一个"以软换硬"的权衡：相比 Nvidia 的专用 RT Core，AMD 的方案对面积更友好，但对寄存器和缓存压力更大。在《赛博朋克 2077》实测中，RX 6900 XT 每秒完成 28.7 Gb box 测试和 3.21 Gb triangle 测试（降频 1800 MHz 下）。BVH 的 TLAS 单独就达 11 MB，远超 L1 容量，因此 L2 和 Infinity Cache 成为光追场景的实际关键缓存层级。关于 AMD 与 Nvidia BVH 构建策略的详细对比，见 [[rendering/bvh-traversal-hardware]]。

## 游戏工作负载趋势

Chester Lam 的帧分析发现现代 AAA 游戏中 compute shader 占比持续上升——《赛博朋克 2077》里甚至传统光栅化退居次席，大量时间花在 compute 和光追上。RDNA 2 在高占用率 compute kernel 中表现出色（vector ALU 利用率可达 50–70%），但 L1 缓存命中率在多数工作负载中偏低是持续的短板。

## 参见

- [[rendering/rdna3-architecture]] — 后继架构，L0/L1 翻倍，VOPD 双发射
- [[rendering/ada-lovelace-architecture]] — 同期竞争对手的缓存策略对比
- [[rendering/bvh-traversal-hardware]] — AMD 与 Nvidia BVH 格式与硬件遍历对比
- [[rendering/hybrid-raytracing-pipeline]] — 混合光栅+光追管线架构
- [[computer-systems/gpu-latency-hiding]] — wavefront 占用与延迟隐藏
- [[rendering/rdna1-overclocking-navi10]] — RDNA 1 基础架构

## Sources

- [[sources/chipsandcheese-rdna2-architecture]]
- [[sources/chipsandcheese-rt-rdna-turing]]
