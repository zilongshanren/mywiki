---
tags: [source, 线性代数, 渲染, 坐标变换]
date: 2026-04-19
sources: 1
---

# Change of Basis, Revisited（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 11 月的教学短文，用 X-Plane 的相机/模型变换做具体背景，把「矩阵的列是基向量」这个线性代数核心事实讲得工程化。

## 摘要

Supnik 把一个 3x3 矩阵看成「预制零件套装」：向量的每个分量是在下「一份某件零件」的订单，矩阵的列就是那些预制零件。当三根列向量是标准正交基时，矩阵本身是 orthogonal matrix——不会缩放、不会扭曲模型，还能用转置代替求逆。把平移合进第 4 列得 affine matrix；X-Plane 刻意只用「左上 3x3 为正交」的 affine 子集，因为能享受许多结构性质：法线直接变换不需要重新归一化、多个变换相乘仍保持同型、camera 位置和 billboard 方向可以从 model-view 矩阵直接推出。最后他解释为什么 `glScale` 和镜像在 X-Plane 里都不用：前者打破正交性（法线变向），后者改变 triangle winding（back-face cull 会反）。

## 关键要点

- 矩阵列 = 旧坐标系的基在新坐标系里的表达。
- 正交矩阵性质：转置即逆、相乘仍正交、法线可直接变换。
- Affine matrix = 线性 + 平移；affine-orthogonal 子集组合后性质依然成立。
- 相机位置 = -transpose(upper3x3) · translation_column，不是简单的右列取负。
- X-Plane 不用 glScale（破坏正交）也不用 mirror（翻 winding）。

## 链接到的概念

- [[matrix-as-basis-vectors]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[matrix-multiplication-ordering]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/change-of-basis-revisited.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-28_change-of-basis-revisited.md`
