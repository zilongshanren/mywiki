---
tags: [gpu, intel, xe2, igpu, lunar-lake, battlemage, rendering, xe-core]
date: 2026-04-27
sources: 1
---

# Xe2 iGPU 架构

Xe2 是 Intel 2024 年随 Lunar Lake 推出的新一代 GPU 架构，同时也将用于即将发布的 Battlemage 独立显卡系列。它是 [[xe-hpg-architecture|Xe-HPG]] 和 Xe-LPG 的演进版，核心目标是在不增加 Xe Core 数量的情况下提升效率，并重新引入矩阵加速单元。

## Vector Engine 架构重组

Xe-LPG 的 Xe Core 内含 16 个 8-wide Vector Engine（VE），两两共享一套线程/指令控制逻辑——这种配对在引入分支发散时会强制两个 VE 同步等待，产生"隐性惩罚"。Xe2 将每对 VE 合并为单个 16-wide VE，每个 Xe Core 因此只剩 8 个 VE，但每个 VE 重新拥有独立的线程控制逻辑。每时钟 FP32 吞吐总量不变，但：

- 分支发散行为更直观：同一 Wave 内 32 线程同向时无惩罚，低于此则线性劣化
- 指令控制开销降低（每单位算力对应的控制逻辑更少）
- 相比 AMD RDNA 的 64-wide SIMD，Intel VE 仍更细粒度，但 wave32 友好性有所提升

## XMX 矩阵加速单元

Lunar Lake iGPU 重新引入 XMX 单元（Meteor Lake iGPU 缺席），每个 VE 配备 2048-bit XMX，提供 4× 于 512-bit 向量单元的矩阵计算吞吐，支持低至 INT2 的精度。对比 AMD RDNA 3.5 的 WMMA 指令（基于点积单元、最低 INT4 精度），Intel 的 XMX 为专用矩阵硬件，在小矩阵和低精度上更灵活。XMX 主要受益于 AI 推理和 DLSS/XeSS 类上采样算法，对于帧率受限的 laptop iGPU 而言意义显著。

## 缓存与内存层次

Xe2 在 Xe Core 内缓存结构大体不变（192 KB L1/SLM），但 Lunar Lake 整体 iGPU L2 从 4 MB 翻倍至 **8 MB**——目前已知 laptop iGPU 中最大的 L2。大 L2 是 Intel 抑制 DRAM 带宽需求、提升功耗效率的核心手段：相比 AMD Strix Point RDNA 3.5（2 MB L2），Intel 在测试中 DRAM 带宽需求更低，但 L2 本身延迟也更高。AMD 走另一路线：更小更快的 L2，但 DRAM 带宽需求和功耗更高。此外，Xe2 将层级 Z 缓存（HiZ）扩容 50%（4→6 KB），颜色缓存扩容 33%，以减少 fixed-function 光栅化阶段的冗余 DRAM 访问。

## 光线追踪单元

每个 Xe Core 的 RTU 升级为 **3 条遍历管线**，每条 6 box test/cycle，合计 18 box test/cycle；triangle test 维持 2/cycle。相比 Xe-LPG（推测 2 管线，12 box test）提升约 50%。Meteor Lake iGPU 已有良好的光追性能，Xe2 进一步巩固，但 AMD Strix Point（更高频率 + 更多 CU 数量）在 3DMark Solar Bay 等基准中仍领先。

## 性能定位

Lunar Lake Xe2（8 Xe Cores）在 Cyberpunk 2077 1080p 低画质下相比 Meteor Lake 提升约 50%，接近 AMD 上代 Phoenix APU 水准，但低于 AMD Strix Point（后者 GPU 更大且频率更高，功耗也更高）。Intel 的策略是：用更好的缓存覆盖率和更高效的 CPU 核心给 GPU 腾出更多热功耗空间，而不是用更大的 GPU 硬堆性能。

## Sources

- [[sources/chipsandcheese-xe2-architecture]]
