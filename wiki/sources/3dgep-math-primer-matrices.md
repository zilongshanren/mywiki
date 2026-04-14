---
tags: [source, math, matrices, primer]
date: 2026-04-14
sources: 1
---

# 3D Math Primer for Game Programmers — Matrices（Jeremiah van Oosten）

[[jeremiah-van-oosten]] 数学入门系列第二篇，承接 [[sources/3dgep-math-primer-vectors|向量篇]]，把矩阵从线性变换、构造、运算性质一路讲到逆矩阵和正交矩阵。

## 摘要

文章定义了线性变换的两条公理（保加法 + 保数乘）并指出 *translation 不是线性变换*——非零平移把零向量送到非零向量，必须放进齐次坐标里才能用矩阵表达，从而引出 4×4 齐次矩阵和**仿射变换**。然后是绕 X/Y/Z 轴的标准旋转矩阵、绕任意轴的 Rodrigues 形式、各向同性与各向异性 scale 矩阵、行列式（含 2×2、3×3、4×4 cofactor 展开）、矩阵的逆 `M⁻¹ = adj(M)/|M|`，以及正交矩阵的判定（`MMᵀ = I` ⇔ 列向量两两单位且正交）和它最有用的性质——`Mᵀ = M⁻¹`，可以省掉昂贵的求逆。约定上文章使用 column-major 矩阵 + 右手坐标系。

## 关键要点

- 平移不是线性变换，只在齐次坐标下才能塞进 4×4 矩阵；这是为什么图形管线全程用 4×4 而不是 3×3 矩阵。
- 3×3 行列式恰好是其行向量的 triple product `(a × b) · c`，几何意义是平行六面体的有向体积。
- 旋转矩阵是正交矩阵，因此**求逆 = 转置**——这是引擎里频繁切换坐标系时的关键性能优化。
- 任意带 scale 的矩阵都不再正交，所以法线变换需要用 `(M⁻¹)ᵀ` 而不是 `M`。

## 链接到的概念

- [[mvp-transform]]
- [[3d-rotation-math]]
- [[coordinate-spaces]]
- [[shader-vector-math-primer]]

## 原文

- 链接：https://www.3dgep.com/3d-math-primer-for-game-programmers-matrices/
- 本地：`raw/articles/3dgep.com/2011-02-04_3d-math-primer-for-game-programmers-matrices.md`
