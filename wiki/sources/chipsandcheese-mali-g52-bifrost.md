---
tags: [source, gpu, arm, mali, bifrost, 移动GPU, compute, tile-rendering]
date: 2026-04-27
sources: 1
---

# Arm's Bifrost Architecture and the Mali-G52（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 5 月 10 日的文章，以 Amlogic S922X 上的 Mali-G52 为测试对象，对 ARM Bifrost GPU 架构进行深度分析，并与 Snapdragon 670 的 Adreno 615 进行对比。

## 摘要

文章从 ARM 的授权业务模型出发，解释了 Bifrost 必须在宽泛工作负载下保持性能一致性的设计动机。然后逐层分析 Bifrost 的执行引擎（标量化 SIMT + FMA/FADD 双发射）、Clause-based ISA 与软件管理操作数转发、内存子系统（分离纹理/load-store 缓存，无片上专用本地内存），以及层级式 tile 渲染与 Transaction Elimination 带宽优化。通过 FluidX3D GPGPU 基准测试揭示：Bifrost 在 FMA 密集型 compute 工作负载上明显优于 Adreno 615（后者缺少硬件 FMA 快速路径），但在纹理吞吐和本地内存性能上逊色。文章最后将 Bifrost 定位为"介于 Terascale 与 GCN 之间的中间道路"，适合低功耗宽泛场景。

## 关键要点

- Bifrost：2016 年，标量 SIMT + FMA+FADD 双发射，取代 VLIW4 Midgard
- Mali-G52：2× triple-EE（8-wide）SC，800 MHz，约 96 GFLOPS
- Clause-based ISA + temporary registers 节省寄存器文件带宽（类 Terascale 2 PV/PS）
- 无专用片上本地内存（Local Memory 走 DRAM 回退，compute 短板）
- Tile 渲染 + Transaction Elimination 有效降低 ROP 侧 DRAM 流量
- FP16/INT8 均有硬件快速路径，vs Adreno 615 两者均无
- Bifrost 零拷贝仅 coarse-grained（Amlogic 系统限制），Adreno 支持零拷贝

## 链接到的概念

- [[arm-bifrost-mali-architecture]]
- [[adreno-640-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-bifrost-architecture-and-the
- 本地：`raw/articles/chipsandcheese.com/2025-05-10_arms-bifrost-architecture-and-the-mali-g52.md`
