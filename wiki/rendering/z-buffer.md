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
- **[[logarithmic-depth-buffer|Logarithmic Depth Buffer]]**：顶点着色器输出 log2 深度，全厂商可用，32 位精度约为 reversed-Z 的 4 倍，行星引擎处理 9 个数量级深度范围的标准方案。
- **Clustered depth**：近远分段，各自独立 Z buffer。
- **[[linear-z-trick|Linear-Z VS trick]]**：`hPos.z *= hPos.w / far` 软件模拟 W-buffer，不破坏纹理透视插值；代价是屏幕空间非线性导致 Hi-Z 退化。

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
- [[hierarchical-z-buffer]] — Z-buffer 的 max-downsample 金字塔，用于遮挡剔除
- [[scene-color-depth-nodes]] —— 在 shader 里采样 `_CameraDepthTexture` 并线性化
- [[depth-texture-silhouette]] —— 在 image effect 里采样 `_CameraDepthTexture` 做距离着色
- [[logarithmic-depth-buffer]] —— 对数深度映射：行星引擎处理 9 个数量级深度范围的完整推导

## Sources

- [[sources/rtr-day03]]
- [[sources/rtr-day05]]
- [[sources/supnik-custom-z-buffer-early-z]]
- [[sources/outerra-depth-buffer-precision]]
