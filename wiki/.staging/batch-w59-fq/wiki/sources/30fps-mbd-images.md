---
tags: [source, graphics, image-compression, precomputed-lighting, pca, notebook]
date: 2026-04-19
sources: 1
---

# Moving basis decomposition for images（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2024 年 3 月的 notebook，把 Silvennoinen & Sloan 2021 年提出的 **Moving Basis Decomposition (MBD)**（原本用于预计算光照传输压缩）简化落地到 2D 图像压缩，当作 PVRTC 式技术的一般化教学例。

## 摘要

MBD 用两张张量重建图像：**稀疏基张量 `B`**（`[N×M×L×D]`，低分辨率空间格子 × L 个 D=3 维主色方向）和**稠密系数张量 `c`**（`[H×W×L]`）。解码时双线性上采样两者到输出分辨率，按 `pixel = Σ_l c_l · B_l` 做加权和，等价于"每像素按周围插值出的 `L` 条色轴线性组合"。优化器（`torchmin` 的 `newton-cg`）同时调 `B` 和 `c`，损失是 MSE + `c` 的 L2 正则（否则 `B` 与 `c` 可以同比缩放造成不定）。初始化用全局 PCA 给 `L=2` 条主色轴，充当所有格子的起始基。作者刻意把 `c` 下采样 2×，重现 PVRTC 式的双线性插值伪影，并点明："**MBD 适合平滑变化的信号**（间接光照、AO），锐利边缘表现很糟"。

## 关键要点

- MBD 本质是 **PVRTC 广义化**：端点数从 2 变 `L`、权重连续可优化。
- 是 [[pca-image-compression]] 的空间变化版；把"全图一组主色"升级到"格子级自适应主色"。
- 对 PRT 探针、辉度图、低频信号压缩率很高；对高频图像无优势。
- 实现直接可套到 light probe 网格、volumetric lightmap 等场景。

## 链接到的概念

- [[moving-basis-decomposition]]
- [[pca-image-compression]]
- [[pca-intro]]
- [[spherical-harmonics]]

## 原文

- 链接：<https://30fps.net/notebooks/mbd-in-2d>
- 本地：`raw/articles/30fps.net/2024-03-16_moving-basis-decomposition-for-imagesp.md`
