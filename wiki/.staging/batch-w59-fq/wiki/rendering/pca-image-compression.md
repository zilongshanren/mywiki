---
tags: [image-compression, pca, color, dimensionality-reduction]
date: 2026-04-19
sources: 1
---

# PCA 图像颜色压缩实验

把 RGB 图当作 `N × 3` 的点云做 PCA，取前两个主成分作为「这张图的两种主色方向」，每个像素就变成两个标量，再加上把两个主方向向量存一份——整张图从三通道降到两通道，颜色空间退化成**一个连续的二色调色板**。[[pekka-vaananen]] 用 Windows XP 的 bliss 壁纸做了演示：RGB 点云主要沿「绿-蓝」和「暗-亮」两个方向散开，两个通道已经把大部分颜色信息捕捉到了；重建误差集中在深色区域，改用感知色彩空间（[[oklab-color-space]]）应能进一步改善。

## 思路概览

- `pca = PCA(n_components=2).fit(flattened_image_data)`；
- 编码：`model.transform(pixels)` → `[N × 2]`；
- 解码：`pca.inverse_transform(encoded)` → `[N × 3]`；
- 传输成本：两张 H×W 的单通道图 + 两个 3 维主向量 + 均值（6 + 3 个浮点数）。

## 与其他方法对比

| 方法 | 降维方式 | 连续 / 离散 |
|---|---|---|
| [[pca-image-compression]] | 把 RGB 投影到 2D 主轴 | 连续 |
| [[color-quantization-kmeans]] | 选 K 个 RGB 质心当调色板 | 离散 |
| [[color-quantization-som]] | 1D 自组织映射给出有序调色板 | 离散但有拓扑 |
| [[vector-quantization-tilemap]] | 把块聚类成码本 | 离散（块级） |

PCA 的优点是重建平滑、解码简单（2 个乘加）；缺点是只能表达数据云里的**线性子空间**，颜色饱和度分布成曲面时会丢。[[moving-basis-decomposition]] 正是针对这一缺陷把全局 PCA 换成**空间变化**的局部基。

## 相关

- [[pca-intro]] —— 数学背景
- [[moving-basis-decomposition]] —— 把 PCA 推到局部自适应
- [[oklab-color-space]]
- [[color-banding]]

## Sources

- [[sources/30fps-pca-colors]]
