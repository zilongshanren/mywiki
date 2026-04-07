---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 4 —— 光栅化：从三角形到像素

RTR 学习推送第 4 天。

## 摘要

**光栅化（Rasterization）**——从连续几何到离散像素的不可避免的信息丢失过程。三角形作为基本单元的理由。边方程、背面剔除、重心坐标。走样（Aliasing）与反走样（SSAA/MSAA）。"像素不是小方块"。

## 关键要点

- **三角形是最优图元**：总是平面、总是凸、重心坐标唯一、硬件易实现。
- Triangle Setup + Triangle Traversal 的硬件加速。
- **边方程**：几何点-三角测试。
- **Fragment ≠ Pixel**：MSAA 下一个 Pixel 对应多个 Fragment。
- **SSAA**：多次完整 shader 执行。**MSAA**：多次 coverage 测试 + 一次 shader + 混合。
- **像素不是小方块**：像素是 0.5 偏移处的点采样，不是面积采样。
- **走样**=采样率不足的信号处理失真；**反走样**=采样前的低通滤波。
- **保守光栅化**：三角形触及像素任一部分就覆盖。
- TBDR 下 MSAA 几乎免费（片上内存）。

## 链接到的概念

- [[rasterization]]
- [[aliasing]]
- [[msaa-ssaa]]
- [[triangle-primitives]]

## 原文

- 链接到：[[raw/articles/real time rendering/day4]]
