---
tags: [source, rendering, spherical-harmonics, mathematica, math]
date: 2026-04-27
sources: 1
---

# Mathematica and Spherical Harmonics（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 9 月的文章，继皮肤渲染之后，用 Mathematica notebook 演示球谐函数的计算：从归一化系数、基函数构造，到投影、重建与卷积。

## 摘要

文章以完整的 Mathematica 代码片段（含符号化注释）展示球谐函数工具链的实现：`shNormalizationCoeffs`（归一化系数）、`shGetFn`（逐 degree/order 生成基函数，含三分支 piecewise 处理 m=0/m>0/m<0）、`shGenCoeffs`（球面积分投影）、`shReconstruct`（系数重建）、`shSymConvolution`（与带旋转对称核的卷积）。代码通过 Mathematica 的 `SphericalPlot3D` 可视化原始函数与 SH 重建的对比，并演示了卷积（等价于逐 band 系数相乘）。文章没有理论介绍，纯代码展示，意在作为可运行参考。

## 关键要点

- 基函数分 m=0、m>0、m<0 三支，关联 Legendre 多项式 + 三角函数，Mathematica 的 `Piecewise` 简洁表达
- 球面积分用 `Integrate[f * Sin[θ], {θ,0,π}, {φ,0,2π}]` 对每个基函数分别做（二维积分，Sin[θ] 是 Jacobian）
- 卷积的实现：带状核（zonal harmonics）的卷积等价于逐系数按 band 乘归一化常数 `sqrt(4π/(2l+1))`
- `MapIndexed` 用于同时遍历元素和下标（list of lists 的情形）
- `Simplify` 附带 `Assumptions` 参数可以对变量域做假设以化简三角表达式

## 链接到的概念

- [[spherical-harmonics]]
- [[preintegrated-skin-shading]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/09/mathematica-and-spherical-harmonics.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-09-20_mathematica-and-spherical-harmonics.md`
