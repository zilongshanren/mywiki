---
tags: [intel, gpu, xe3, xve, raytracing, stoc, battlemage, arc]
date: 2026-04-27
sources: 1
---

# Intel Xe3 GPU 架构前瞻

Xe3 是 Intel 继 [[xe2-igpu-architecture|Xe2]]（Battlemage / Lunar Lake）之后的下一代 GPU 架构。截至 2025 年初，Xe3 硬件设计已完成，软件工作正在进行，相关变化在 Mesa、Intel Graphics Compiler 等开源仓库中可见。本文梳理从代码库变化中能读出的 Xe3 架构方向。

## Render Slice 拓扑扩展

Intel GPU 通过层级拓扑（XVE → Xe Core → Render Slice → 全 GPU）实现规模伸缩。Xe3 扩展了 `sr0` 寄存器的拓扑枚举位宽：每个 Render Slice 内的 Xe Core 编号从 2-bit 扩为 4-bit，理论上允许单个 Render Slice 容纳最多 16 个 Xe Core（前代上限为 4）。这意味着 Intel 可以在不增加固定功能单元（光栅化器、ROP）数量的前提下，向 Shader Array 中填入更多计算力，与 AMD（Shader Engine 含 10 WGP）和 Nvidia（GPC 含 8 SM）的趋势一致。

## XVE 改进：更高占用率与更灵活的寄存器分配

**并发线程数从 8 增至 10。** 更多在途线程意味着更强的延迟隐藏能力，类似 CPU 的 SMT。Xe3 将 64 KB 寄存器文件的分配粒度细化为 32 个寄存器一块，只要每个线程不超过 96 个寄存器即可维持 10 线程满占用。相比前代非 0/8/4 档的硬降级机制，复杂着色器现在可以更平滑地退化到低占用档。

**Scoreboard 令牌翻倍。** 每个线程固定获得 32 个 scoreboard 令牌（Xe2 在 8 线程模式下只有 16 个），整个 XVE 共拥有 320 个令牌，大幅增加每线程可同时挂起的长延迟指令数量，有利于内存级并行度（MLP）提升。

**新增 Scalar Register（s0）。** Xe3 在架构寄存器文件（ARF）中增加 `s0` 标量寄存器，用于 gather-send 指令，允许从寄存器文件中聚合非连续数据后以单条 send 指令发出，减少内存访问的指令开销。

**指令集扩展：** 支持 `FCVT` 的饱和修饰符（便于高精度到低精度浮点转换）；新增 HF8（8-bit 半浮点）格式，与 Xe2 已有的 BF8 并列；XMX 矩阵单元新增稀疏点积指令 `xdpas`（sparse systolic dot product with accumulate），与 AMD 和 Nvidia 的稀疏矩阵加速功能对齐。

## 光追改进：Sub-Triangle Opacity Culling (STOC)

Xe3 最引人注目的光追新功能是**子三角形不透明度裁剪（STOC）**。当游戏用低多边形网格 + 透明通道纹理表现树叶、链环围栏等几何体时，每条与三角形相交的光线都必须调用 any-hit 着色器做 alpha 测试，造成大量无效着色器启动。

STOC 的做法：将 BVH 叶节点中的三角形细分为若干子三角形，并用 2-bit 标记每个子三角形的不透明度状态（完全透明 / 完全不透明 / 部分透明）。

Xe3 实现了两个层次：

- **STOC1**：保持 64 字节叶节点大小，在 Intel 现有的 QuadLeaf 格式（一对共边三角形）中挤出 18 个额外位存储 STOC 信息（每个三角形 8 bit、即 4 个子三角形），另加 2 bit 调试标志。对完全透明的子三角形，RTA 直接跳过 any-hit 调用；对完全不透明的子三角形，可提前终止光线并跳过 alpha 测试。
- **STOC3**：叶节点扩展为 128 字节，存储指向外部 STOC 位图的指针，支持递归细分以减少部分透明子三角形比例，灵活性更高但 BVH 内存占用更大。

Intel 论文报告软件实现的 STOC 已能将性能提升 5.9–42.2%（透明光追阴影场景）；硬件 STOC 还可让 RTA 直接跳过着色器启动，预期收益更大。STOC 目前不属于 DXR / Vulkan 标准，需要引擎侧额外支持。

## 与前代的对比定位

Xe2（Battlemage）通过 XVE 合并、256 KB L1、atomic 重构等改进以更小的芯片超越了前代旗舰 A770；Xe3 继续在此基础上提高每 Xe Core 的并行度、延迟容忍能力和光追效率。Nvidia Ampere 到 Blackwell 期间 SM 架构几乎未变，侧重规模扩展；Intel 则选择持续迭代核心微架构。

## Sources

- [[sources/chipsandcheese-xe3-gpu]]
