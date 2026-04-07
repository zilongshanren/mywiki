---
tags: [渲染, 深度缓冲]
date: 2026-04-05
sources: 2
---

# Z-Buffer（深度缓冲）

每像素存储当前最近表面的深度值，实现**隐面消除**。

## 性能特征

- **O(n) in 图元数**——无需排序不透明物体。
- 允许任意渲染顺序（对不透明而言）。
- **无法处理半透明**：只能存一个深度。
- 硬件加速极深（GPU 内置）。

## 精度非线性分布

投影矩阵让 Z 在 NDC 中非线性分布：**近平面得到 ~50% 的精度**，远平面密集、精度低。这是 [[z-fighting|Z-fighting]] 的物理根源。

近=0.1, 远=1000 时，500m 处的深度分辨率约 1cm——近处过剩，远处不足。

## 改进方案

- **Reversed-Z**：见 [[reversed-z]]，把近远翻转到 1→0，结合 float 精度分布改善远平面。
- **Logarithmic Depth**：手动对数映射，均匀化精度。
- **Clustered depth**：近远分段，各自独立 Z buffer。

## 与 Alpha 混合的不兼容

半透明物体必须：
- 从后往前渲染（画家算法）。
- **不写** Z buffer（只读）。
- 否则后面物体会被拒绝。

## 相关

- [[z-fighting]]
- [[reversed-z]]
- [[early-z-late-z]]
- [[alpha-blending]]
- [[coordinate-spaces]]

## Sources

- [[sources/rtr-day03]]
- [[sources/rtr-day05]]
