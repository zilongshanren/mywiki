---
tags: [source, 渲染, 皮肤渲染, 着色器]
date: 2026-04-27
sources: 1
---

# Addendum to Mathematica and Skin Rendering（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 11 月的补遗文章，紧接其 Mathematica 皮肤渲染推导篇，直接给出了可在着色器中使用的拟合函数实现代码。

## 摘要

本文是 Pesce 用 Mathematica 拟合 Penner 预积分皮肤散射近似之后的实用补遗：把拟合参数以 HLSL 硬编码系数的形式给出，得到 `PSSFitFunction(float NdL, float r)` 函数，输入法线与光源夹角（NdL）以及曲率半径（r），输出 RGB 三通道的散射系数。作者同时指出当前版本在半径范围上过宽——对大半径侧退化到标准 NdotL 的过渡方式还可以做得更精确——并把 Mathematica 源码留给读者自行改进。

## 关键要点

- 给出 6 组系数（a0–a5）的 RGB 三通道数组，可直接 copy 到 shader
- 实现了「大曲率退化到标准 Lambert NdotL」的平滑过渡，通过 `fade` 变量混合
- 作者自评：当前 clamping 半径范围过宽，可进一步优化
- 属于对 [[preintegrated-skin-shading]] 的代码落地补充，非新技术

## 链接到的概念

- [[preintegrated-skin-shading]]
- [[angelo-pesce]]

## 原文

- 链接：http://c0de517e.blogspot.com/2012/11/addendum-to-mathematica-and-skin.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-11-03_addendum-to-mathematica-and-skin-rendering.md`
