---
tags: [source, rendering, sss, skin, mathematica]
date: 2026-04-27
sources: 1
---

# Mathematica and Skin Rendering（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 9 月的文章，配合 Eric Penner 的 SIGGRAPH 2011 皮肤着色演讲，用 Mathematica 演示如何对预积分皮肤散射 LUT 求解析近似。

## 摘要

文章分两部分：前半部分是 Mathematica 速成课，演示 notebook 操作流程、延迟赋值语法（`:=`）、函数式编程和列表操作；后半部分针对 Eric Penner 的预积分皮肤着色模型，用 Mathematica 的 `NIntegrate` 计算散射积分样本，再用 `NonlinearModelFit` 拟合出一个含 6 个参数的解析函数，从而**消灭 LUT 查询，用纯代数计算还原着色结果**。文章以 Mathematica 的符号运算 + 数值库 + 可视化三位一体为切入点，展示了计算机代数系统在实时图形研究原型中的效用。

## 关键要点

- 预积分皮肤 LUT 的两个轴是 NdotL（cos θ）和曲率半径 r；散射剖面使用 d'Eon & Luebke 2007 的六高斯模型
- 拟合函数含 `Clip`/`Max`，模型非光滑，需要用 `NMinimize` 而非 `GradientDescent` 求参数
- 拟合目标：大 r 极限退化为 Lambert 余弦（物理正确约束）
- Mathematica 的 delayed assignment（`:=`）类似 Lisp 的 quote，`=` 则立即求值
- 函数式操作 `/@`（Map）、`@@`（Apply）、`/.`（ReplaceAll）是核心惯用法

## 链接到的概念

- [[preintegrated-skin-shading]]
- [[physically-based-shading]]
- [[spherical-harmonics]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/09/mathematica-and-skin-rendering.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-09-08_mathematica-and-skin-rendering.md`
