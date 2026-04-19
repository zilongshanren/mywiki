---
tags: [source, rendering, math, shader, graphics-api]
date: 2026-04-19
sources: 1
---

# The Ultimate Guide to Matrix Multiplication and Ordering（Jasper St. Pierre）

[[jasper-st-pierre]] 发表于 2024 年 10 月的一篇综合性博客，目标是"一次讲透图形 API 里关于矩阵乘法的所有混乱来源"。

## 摘要

文章把图形编程里纠缠不清的四个概念**彻底正交化**：矩阵乘法本身（永远是 across-times-down）、向量乘法方向（列向量乘法 vs 行向量乘法）、矩阵内存打包（row-major vs column-major）、shading language 差异（HLSL vs GLSL 的索引与构造器）。它通过"矩阵乘法只是联立方程代入化简的压缩写法"给出最基础的直观解释，然后逐条列出十条 "Matrix Facts"——从非交换、可结合、across-times-down、到 packing 只影响 I/O 不影响数学，再到 inverse 不改变乘法顺序等核心结论。最后给出一张 HLSL vs GLSL 速查表，推荐**列向量 + row-major packing + `A_from_B` 空间命名**三件套作为最不容易搞混的约定组合。

## 关键要点

- 所有着色语言的矩阵乘法底层都是"A 的行点乘 B 的列"。HLSL 用 `mul(A,B)`、GLSL 用 `A*B`，但算法一致。
- `A * v` 把 v 视作列向量，`v * A` 把 v 视作行向量——同一个 v 根据位置自动"转置"。
- Row-major 和 column-major 只是内存打包顺序，不改变矩阵形状也不改变乘法结果。
- `A*B = transpose(transpose(B)*transpose(A))`——这是为什么"反了顺序 + 转置"可以彼此抵消的数学基础。
- 推荐的空间链命名：`clip_from_view * view_from_world * world_from_model * model_P`——相邻矩阵的内外空间名对齐，一眼能看出链条对不对。
- Inverse 矩阵**不改变乘法顺序**：`world_from_model * model_P = world_P` ↔ `inverse(world_from_model) * world_P = model_P`。
- HLSL 的 `float3x4` 代表 3 行 4 列；GLSL 的 `mat3x4` 代表 4 行 3 列——命名约定相反，是 GLSL 开发者踩坑的常见来源。

## 链接到的概念

- [[matrix-multiplication-ordering]]
- [[row-major-column-major-packing]]
- [[mvp-transform]]
- [[scene-graph-matrix-stack-visitor]]

## 原文

- 链接：https://blog.mecheye.net/2024/10/the-ultimate-guide-to-matrix-multiplication-and-ordering/
- 本地：`raw/articles/blog.mecheye.net/2024-10-13_the-ultimate-guide-to-matrix-multiplication-and-ordering.md`
