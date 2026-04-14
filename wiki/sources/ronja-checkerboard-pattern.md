---
tags: [source, rendering, shader, unity, 程序化纹理]
date: 2026-04-14
sources: 1
---

# Checkerboard Pattern（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 2018 年 5 月发表的系列第 011 篇，**零纹理**在 shader 里生成一张棋盘图案，是程序化图形的入门练习。

## 摘要

文章从 1D 条纹出发：`floor(p.x)` 把位置量化到整数单元、`frac(c * 0.5)` 产生偶数 0、奇数 0.5、再 `* 2` 归一到 0/1。然后换维几乎不要代价——`floor(p.x) + floor(p.y)` 相加，相邻格子奇偶翻转产生 2D 棋盘；再加一维就是 3D。作者特意强调**必须先 `floor` 每个分量再求和**，而不是 `floor(p.x + p.y)`——后者会得到斜条纹而非棋盘。接着用 `_Scale` 在 `floor` 之前做除法控制单元格大小（`<1` 变密、`>1` 稀疏），最后把 `_EvenColor` / `_OddColor` 两个 Inspector 颜色走 `lerp(_Even, _Odd, c)`——因为 `c` 只有 0/1 两个值，`lerp` 在这里实际上是二选一的选择器。文章明确引用它前一篇 color interpolation 作为 `lerp` 数学的背景。

## 关键要点

- **量化 → 奇偶 → 归一**：`floor` → `frac(c*0.5)` → `*2` 是核心三步。
- 加维靠「每个分量各自 `floor` 后相加」——相邻格子在任何轴上都翻转奇偶。
- 世界坐标 vs 物体坐标决定图案是钉在世界还是跟物体移动（和 [[planar-mapping]] 同逻辑）。
- `_Scale` 必须在 `floor` 之前除法，`>1` 稀疏、`<1` 密集。
- 二值 mask 走 `lerp` 是一个通用技巧：`lerp` 在 `t∈{0,1}` 时就是二选一选择器。
- 本文是「周期性二值图案」的最小可复用模板，可以推广成条纹、网格线、色块噪声。

## 链接到的概念

- [[procedural-checkerboard]]
- [[shader-color-interpolation]]
- [[planar-mapping]]
- [[coordinate-spaces]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/011-chessboard/>
- 本地：`raw/articles/ronja-tutorials.com/2018-05-18_checkerboard-pattern.md`
