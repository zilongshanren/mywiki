---
tags: [source, 着色器, 数学, 平滑函数, 程序化渲染]
date: 2026-04-27
sources: 1
---

# Smoothen your functions（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2014 年 4 月的文章，介绍着色器中常用的平滑数学函数——smoothstep 变体、smooth min/max、sigmoid 函数族、Bias/Gain——以及为何应该优先使用连续可微函数。

## 摘要

文章从一个实用主义观点出发：**着色器里的阶跃函数（step、clamp、if）几乎都应该被平滑替代版本取代**。原因有二：一是物理上真实的光照本不存在硬边（光源有面积，遮挡是连续分数），硬步阶是对物理的近似偷懒；二是所有非连续函数经像素覆盖范围（box filter）卷积后都会产生锯齿，平滑函数自然地减缓这一问题。文章随后系统整理了一套可直接在着色器使用的数学工具：smooth min/max（可推广到多值，与 norm-infinity 存在深层联系）、不同阶 smoothstep 变体（含 piecewise 版本）、sigmoid 函数族（Logistic、Gompertz、Smooth Sigmoid）、以及 Perlin 原版 Bias/Gain 和 Schlick 优化版。文章还特别提到 smoothstep 与移位余弦的接近性，以及 smooth abs 的两种近似。

## 关键要点

- 在高光过渡处，即便是二阶导不连续的 smootherstep 也可能产生可见瑕疵，需用五次多项式
- Smooth min/max：`log(exp(x·s)+exp(y·s))^(1/s)` 的简化形式；负 s → 软 min，正 s → 软 max；可直接扩展到多值
- Schlick Bias/Gain 是 Perlin 原版的优化：① 更快；② 对角线对称（参数 a 与 1-a 互为逆曲线）
- Gompertz sigmoid 参数语义清晰（渐近线、位移、增长率）但不对称，用于色调映射时需注意
- Smooth abs：`sqrt(x²+ε)` 最简；带 d 参数的有理多项式版本在零附近更陡峭
- 链接到 IQ 的 smooth min、Functions、Ray Differentials 等参考，是该话题的标准阅读列表

## 链接到的概念

- [[shaping-functions]]
- [[sigmoid-functions]]
- [[smoothstep]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/04/smoothen-your-functions.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-04-26_smoothen-your-functions.md`
