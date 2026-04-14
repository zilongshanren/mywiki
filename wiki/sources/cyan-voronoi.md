---
tags: [source, shader, shadergraph, 噪声, 程序化纹理]
date: 2026-04-14
sources: 1
---

# Voronoi（Cyan）

[[cyanilux|Cyan]] 2019 年 7 月发表的 Shader Graph 教程，逐行拆解 Unity 内置 **Voronoi 节点**生成的 HLSL 代码，并给出两种**Voronoi 边缘**（cell border）的自定义实现。文章的价值不在数学新意，而在它把 [[worley-voronoi-noise|Worley/Voronoi 噪声]] 在 Shader Graph 里如何被一段 30 行 HLSL 落地讲到「每个变量是什么」的级别——对入门技术美术非常实用。

## 摘要

文章先复习 Voronoi 的基本概念：空间分成均匀网格，每个 cell 内放一个伪随机偏移的特征点；当前像素扫相邻 3×3 个 cell，取最近距离 = **F1**、次近 = **F2**，依此类推。距离度量除了常见的欧氏距离，还可以用 Manhattan、Chebyshev、Minkowski（参数化的统一公式，`n=1` 是 Manhattan、`n=2` 是欧氏、`n→∞` 趋近 Chebyshev——但实践中超过 `n=10` 就没差，太大反而出 artefact）。

Shader Graph 内置的 Voronoi 节点只输出 F1。Cyan 拆解了 `Unity_Voronoi_float` 函数：`floor(UV * CellDensity)` 是当前 cell 整数坐标，`frac(UV * CellDensity)` 是 cell 内局部位置；double `for(-1..1)` loop 扫邻居，每个邻居 cell 用 `unity_voronoi_noise_randomVector(cell, AngleOffset)` 哈希出 `[0,1]^2` 偏移得到特征点；`distance(...)` 取最小。

为了拿到「**cell 边缘**」（裂纹、皮肤鳞片那种 hard line 效果），Cyan 给了两种自定义 Custom Function：

- **F2 - F1 法**：在同一个循环里同时跟踪最近和次近距离，输出 `sqrt(F2) - sqrt(F1)`。便宜但在某些 cell 里有明显误差，且跟 `Step` 节点配合做硬边时 cell 形状会偏圆。`distance` 换成 `dot(v,v)` 避免循环里跑 `sqrt`。
- **两次循环法**（基于 [iquilezles 的 voronoilines 文章](https://iquilezles.org/www/articles/voronoilines/voronoilines.htm)）：第一遍找最近 cell 和它的特征点 `mv`、cell 坐标 `ml`；第二遍以 `ml` 为中心 5×5 扫邻居，对每个邻居用 `dot(0.5*(mv+v), normalize(v-mv))` 算「到那条 cell 边的垂直距离」，取最小。更精确，能产出真正的直线段 cell border。Cyan 加了一个 `cellDifference` 大于 `0.1` 的 if 来跳过自己（避免 `normalize(0)` 在不同硬件上的未定义行为）。

## 关键要点

- Shader Graph 内置 Voronoi 节点只能给 F1；想要 cell 边缘必须 Custom Function。
- F1 = 最近距离（流行用法：金属颗粒、细胞、水焦散）；F2-F1 ≈ cell 边缘（裂纹、龟裂）；两次循环法 = 真正的直线段 cell border。
- `dot(v, v)` 在循环内代替 `distance` 避免 `sqrt`，最后再开方一次——经典优化。
- 距离度量参数化（Minkowski）能让 Voronoi 看起来从「圆形 cell」连续变成「方形 cell」，但 `n > 10` 之后没差且容易 artefact。
- 自定义 HLSL 用 Custom Function 节点接入 Shader Graph 时，函数名必须和 hlsl 文件里一致，参数列表要逐一匹配 Inputs/Outputs。

## 链接到的概念

- [[worley-voronoi-noise]]
- [[cellular-texture-generation]]
- [[shaping-functions]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2019/07/16/voronoi/
- 本地：`raw/articles/cyangamedev.wordpress.com/2019-07-16_voronoi.md`
