---
tags: [source, rendering, intel, gpu, xe3, raytracing, stoc, xve]
date: 2026-04-27
sources: 1
---

# Looking Ahead at Intel's Xe3 GPU Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 3 月的文章，从开源软件仓库（Mesa、Intel Graphics Compiler）的变化中前瞻 Intel Xe3 GPU 架构的主要改动方向。

## 摘要

文章在 Xe3 硬件尚未上市之时，通过分析编译器和驱动代码提炼出三个核心变化方向：XVE 并发线程从 8 增至 10 并采用更细粒度的寄存器分配（32 寄存器一块），scoreboard 令牌从每线程 16 增至 32（使整个 XVE 拥有 320 个），以及光追专项优化 Sub-Triangle Opacity Culling（STOC）。STOC 针对树叶、链环等使用透明 alpha 通道的几何体，将 BVH 叶节点三角形细分并标记透明度，让硬件直接跳过对完全透明/不透明子三角形的无谓 any-hit 着色器调用。拓扑方面，Xe3 将 Render Slice 内 Xe Core 枚举位数从 2-bit 扩至 4-bit，支持更大的 Shader Array，但最终产品配置取决于市场定位。

## 关键要点

- XVE 线程槽从 8 增至 10，寄存器分配粒度细化（32 寄存器一块），避免 Xe2 的硬降级
- Scoreboard 令牌：每线程 16 → 32，全 XVE 共 320 个，大幅提升内存级并行度
- 新增 Scalar Register（s0）用于 gather-send 指令
- XMX 新增稀疏点积指令 xdpas（对齐 AMD/Nvidia 稀疏矩阵加速）
- STOC1：64 字节叶节点 + 嵌入 18 bit STOC 位，4 个子三角形/三角形
- STOC3：128 字节叶节点 + 外部 STOC 位指针，支持递归细分
- 软件 STOC 在透明阴影场景性能提升 5.9–42.2%；硬件 STOC 可让 RTA 直接跳过着色器调用

## 链接到的概念

- [[rendering/xe3-gpu-architecture]]
- [[computer-systems/battlemage-architecture]]
- [[rendering/xe2-igpu-architecture]]
- [[rendering/bvh-traversal-hardware]]

## 原文

- 链接：https://chipsandcheese.com/p/looking-ahead-at-intels-xe3-gpu-architecture
- 本地：`raw/articles/chipsandcheese.com/2025-03-19_looking-ahead-at-intels-xe3-gpu-architecture.md`
