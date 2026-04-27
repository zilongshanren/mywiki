---
tags: [source, graphics, image-compression, pca, notebook]
date: 2026-04-19
sources: 1
---

# PCA image color compression experiment（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2024 年 3 月的短 notebook：用 `sklearn.decomposition.PCA(n_components=2)` 把 Windows XP bliss 壁纸的 RGB 颜色降到 2 维，再 `inverse_transform` 反投回 RGB 做重建，讨论"连续二色调色板"这种压缩视角。

## 摘要

把图像像素 flatten 成 `[N × 3]` 点云后做 2D PCA，图像被编码成两张单通道图 + 两个主方向向量 + 一个均值；重建时把 2D 坐标线性映回 3D RGB 即可。bliss 这种色调集中在"绿-蓝 vs 亮-暗"的壁纸在 2D PCA 下几乎看不出视觉差异，L1 误差主要集中在深色区。作者猜测用感知色彩空间（LAB 或 OkLab）做距离会更好——RGB 欧氏距离不对应感知距离，这和 K-Means 调色板的老问题一致。这份实验本身不 production-ready，但给 [[moving-basis-decomposition]] 做了直接铺垫：那篇就是把这里的"全局两条色轴"推广成"空间变化的局部色轴"。

## 关键要点

- 2 维 PCA 能把大部分自然图像的颜色信息捕获 ≥95%。
- 深色、暗部细节是 PCA 的重建短板。
- PCA 与 K-Means 是"连续降维 vs 离散聚类"的对照。
- 可作为 MBD、PRT 压缩的最简参照基线。

## 链接到的概念

- [[pca-image-compression]]
- [[pca-intro]]
- [[moving-basis-decomposition]]
- [[oklab-color-space]]

## 原文

- 链接：<https://30fps.net/notebooks/pcacolors>
- 本地：`raw/articles/30fps.net/2024-03-05_pca-image-color-compression-experimentp.md`
