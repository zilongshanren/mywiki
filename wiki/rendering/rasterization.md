---
tags: [渲染, 光栅化]
date: 2026-04-05
sources: 3
---

# 光栅化（Rasterization）

**从连续几何（三角形）到离散像素（fragment）的转换过程**。不可避免的信息丢失。

## 两个子阶段

- **Triangle Setup**：计算边方程和差分量（硬件加速）。
- **Triangle Traversal**：遍历每个像素，测试 coverage，生成 fragment。

## 为什么三角形

- **总是平面**（三点确定唯一平面）
- **总是凸**（无内部分叉）
- **重心坐标唯一**（插值数学干净）
- **硬件实现最易**

## 边方程（Edge Equations）

三角形每条边用线性方程 `f(x,y) = ax + by + c` 表示。点在三角形内当且仅当三个方程都同号。GPU 用硬件并行测试 2×2 块（quad）的 4 个像素。

## Fragment vs Pixel

**Fragment ≠ Pixel**：MSAA 下一个 pixel 可能对应多个 fragment。fragment 是候选像素数据，pixel 是最终输出。

## 同步点

光栅化是管线的重要**同步点**：输入是顶点流，输出是 fragment 流——连接 Geometry 和 Pixel Processing 两大阶段。

## 保守光栅化

**Conservative Rasterization**：三角形触及像素任一部分就覆盖（而非中心点采样）。用于碰撞检测、体素化、voxel-based GI。

## 相关

- [[rendering-pipeline]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[triangle-primitives]]
- [[perspective-correct-interpolation]]
- [[pineda-edge-rasterization]] —— GPU 光栅化的算法本体
- [[hierarchical-rasterization]] —— coarse rasterizer 的剔除层
- [[triangle-setup]] —— 边方程系数的来源
- [[compute-vs-raster-points]] —— 何时 compute shader 比硬件光栅化更快
- [[bresenham-lines]] — 1962 年的纯整数直线算法，tile-grid 场景下的基础工具
- [[variable-length-bresenham]] — 支持"从起点沿方向走固定距离"的展开版 Bresenham

## Sources

- [[sources/rtr-day04]]
- [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]]
- [[sources/aras-gpu-point-rasterization]]
