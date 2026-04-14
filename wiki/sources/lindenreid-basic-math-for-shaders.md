---
tags: [source, shader, 数学]
date: 2026-04-14
sources: 1
---

# Basic Math for Shaders（Linden Reid）

[[linden-reid]] 发表于 2018 年 8 月的入门教程，把 shader 需要的那点线性代数（向量加减、叉乘、归一化、点乘、矩阵乘向量）按"能做什么"而非"公式是什么"组织起来。

## 摘要

作者先讲清三件事：mesh 是 3D 空间里的点集、vector 是数列、matrix 是 table，然后逐一拆解 shader 里真正会用的运算。向量减法 = 两点射线、向量归一化 = 丢掉长度、点乘 = 夹角余弦（前提是归一化）、叉乘 = 垂直方向、矩阵乘向量 = 换坐标空间。整篇教程以"视觉化数学"为线索——她自己自称"数学很差"，靠把每个公式翻译成纸上的箭头才学会——并把每个概念落到 Unity shader 的具体 API：`UNITY_MATRIX_MV`、`dot(N, L)` 式光照、`cross` 求法线。续读推荐 *3D Math Primer for Graphics and Game Development*。

## 关键要点

- 向量的"位置 / 方向 / 颜色"三种身份在 shader 代码里长得一样，bug 多半来自混淆语义。
- `dot` 返回夹角信息的前提是**两边都归一化**；否则得到 `|a||b|cos(t)`，长度污染角度。
- 叉乘用来求表面法线时，只需要三角形的两条边——但生产里几乎都靠 `RecalculateNormals` 或美术工具，不手算。
- 4×4 矩阵在 shader 里的唯一用途就是换坐标空间，Unity 已经把 MVP 变成 `UnityObjectToClipPos`。
- 作者的教学主张：可视化 > 抽象符号。

## 链接到的概念

- [[shader-vector-math-primer]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[fragment-shader]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2018/08/25/basic-math-for-shaders/
- 本地：`raw/articles/lindenreid.wordpress.com/2018-08-25_basic-math-for-shaders.md`
