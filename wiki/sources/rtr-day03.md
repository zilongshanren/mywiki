---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 3 —— Geometry Processing：顶点的旅程

RTR 学习推送第 3 天。

## 摘要

顶点在多个坐标空间之间的变换（MVP），以及每个空间存在的设计意义。深度缓冲的精度分布、Reversed-Z、透视校正插值。

## 关键要点

- **MVP 变换**：Model → View → Projection 三矩阵分开的原因（光照计算需要中间空间位置）。
- 坐标空间序列：Model → World → View → Clip → NDC → Screen。
- 每个空间存在是为了某个操作的**数学简单性**。
- 剪裁在 Clip Space 的固定单位立方体 [-1,1]³——硬件简化。
- **透视除法**必须在剪裁前进行（近平面数值稳定性）。
- **Z-fighting**：深度缓冲非线性精度分布。
- **Reversed-Z**：1.0 = 近，0.0 = 远，改善远平面精度。
- **透视校正插值**：线性屏幕空间插值对应非线性 3D 空间。
- TBDR 的 Binning Pass 导致移动端 vertex shader 执行两次。

## 链接到的概念

- [[mvp-transform]]
- [[coordinate-spaces]]
- [[z-buffer]]
- [[z-fighting]]
- [[reversed-z]]
- [[perspective-correct-interpolation]]

## 原文

- 链接到：[[raw/articles/real time rendering/day3]]
