---
tags: [source, gpu, amd, rdna4, raytracing, bvh, obb, primitive-compression]
date: 2026-04-27
sources: 1
---

# RDNA 4's Raytracing Improvements（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 4 月的文章，系统分析 RDNA 4（RT IP 3.1）在固定功能光追硬件上的三大升级：双相交引擎、定向包围盒（OBB）和图元节点压缩。

## 摘要

RDNA 4 的 Ray Accelerator 从 1 个 Intersection Engine 增至 2 个，盒测试吞吐翻倍（每周期 8 个），三角形测试也加倍。为充分利用更高吞吐，BVH 宽度从 4-wide 升至 8-wide，减少延迟敏感的指针追逐步骤，以更多并行计算换取更少串行内存跳转。同时新增 IMAGE_BVH_DUAL_INTERSECT_RAY 指令支持 BVH4x2 算法（同时遍历两条路径）。OBB 通过 104 个预定义旋转矩阵（索引查表）近似几何体的最优包围方向，每个 8-wide box node 仍保持 128 字节。图元节点压缩将多对共享顶点的三角形打包进 128 字节，并对顶点坐标尾部零位做截断压缩，box 坐标从 FP32 改为 12-bit 定点。在实测中（DXR Feature Test），RDNA 4 RX 9070 达到 111.76G 盒测试/秒 vs RDNA 2 RX 6900XT 的 38.8G，Ray Accelerator 利用率提升显著。

## 关键要点

- 8-wide BVH：每步 8 个盒测试，减少遍历总步数，以吞吐换延迟
- OBB：104 个预定义矩阵索引，128B box node 格式不变，对非轴对齐几何体效果明显
- 图元压缩：共享顶点合并 + 尾零截断，128B 最多可存 16 个唯一顶点 / 8 个三角形对
- Box 坐标 12-bit 量化，8-wide box node 维持 128 字节与 cacheline 对齐
- Ray Accelerator 新增专用光线变换模块（用于 TLAS→BLAS 过渡及 OBB 光线旋转）
- RDNA 4 同时保留旧 IMAGE_BVH_INTERSECT_RAY（4-wide），向后兼容

## 链接到的概念

- [[rendering/rdna4-rt-improvements]]
- [[rendering/bvh-traversal-hardware]]
- [[computer-systems/rdna4-architecture]]
- [[computer-systems/rdna4-ooo-memory]]
- [[computer-systems/rdna4-dynamic-vgpr]]

## 原文

- 链接：https://chipsandcheese.com/p/rdna-4s-raytracing-improvements
- 本地：`raw/articles/chipsandcheese.com/2025-04-14_rdna-4s-raytracing-improvements.md`
