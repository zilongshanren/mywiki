---
tags: [source, rendering, marching-squares, procedural-generation]
date: 2026-04-27
sources: 1
---

# 2D Marching Cubes with Multiple Colors（Boris The Brave）

[[boris-the-brave]] 发表于 2021 年 12 月的文章，设计了一种将标准 [[marching-cubes]]（2D，即 Marching Squares）扩展至支持多种颜色区域的简洁方案。

## 摘要

标准 Marching Squares 以每个顶点的二值状态（"内"/"外"）驱动边界绘制，无法直接处理多色场景。本文的关键洞察是：四个角顶点最多只有 4 种颜色，而我们关心的不是具体颜色标签而是**颜色间的等价关系**。通过规范化重标签（以右上角顶为颜色 0，逆时针依序命名新颜色），所有可能的组合均可归约为 15 种基本情形，与标准版本的 16 种（其中 1 种为全相同色）规模相当。

自适应定位方面，文章将标准 Marching Squares 的"有符号距离值"推广为多色场景的"权重（weight）"——正数，表示该顶点推开边界的强度（通常是顶点到真实边界的距离）。两顶点间边界点的位置用调和加权插值确定；格中心顶点同样使用调和加权平均，或借鉴 [[dual-contouring]] 方式获得更精确位置。

## 关键要点

- 多色 Marching Squares 只需 15 种基本情形（与二值版本相比增加极少）
- 核心技巧：颜色重标签（按顺序命名新颜色），消除与具体颜色的耦合
- 情形 17（ABAB 对角交叉）同样存在歧义，与标准版本的歧义情形对应
- 自适应定位用"权重"替代"有符号距离"，公式推广自线性插值
- 仅适用于 2D；3D 场景推荐标准 Marching Cubes + 着色器着色

## 链接到的概念

- [[marching-cubes]]
- [[marching-squares-multicolor]]
- [[marching-squares-ambiguities]]
- [[dual-contouring]]

## 原文

- 链接：https://www.boristhebrave.com/2021/12/29/2d-marching-cubes-with-multiple-colors/
- 本地：`raw/articles/boristhebrave.com/2021-12-29_2d-marching-cubes-with-multiple-colors.md`
