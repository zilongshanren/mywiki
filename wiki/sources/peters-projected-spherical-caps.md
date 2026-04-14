---
tags: [source, 渲染, 采样, 光源, 实时渲染, 论文]
date: 2026-04-14
sources: 1
---

# Sampling Projected Spherical Caps in Real Time（Peters & Dachsbacher, i3D 2019）

[[christoph-peters|Christoph Peters]] 和 Carsten Dachsbacher 在 **ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2019** 发表的论文的博客登记页。论文正文解决「球形面光源 + 漫反射表面」场景下的最优采样问题；博客页主要是发布告示加一条重要勘误。

## 摘要

对漫反射表面做面光源着色时，**按投影立体角**（立体角 × $\cos\theta$）采样在理论上是零方差的，因为它恰好消去被积函数里的 Lambertian 余弦项。但对球形光源，「投影后的形状」既不是圆也不是椭圆，离线渲染已有的算法不适合 GPU。Peters 的核心做法是把球形光源的投影立体角**精确分解（或良好近似）为若干 cut disk 的并集**——cut disk 是一个被某条直线切去一部分的圆盘，它有高效的直接采样算法。整个方案比「简单按立体角采样」贵 2-3 倍，但噪声几乎消失，在 1 spp 的 ray-traced soft shadow 中直接出干净图像。对不是精确分解的情形，误差有可证上界。

## 关键要点

- **最优策略 = 按投影立体角采样**：可消去漫反射表面的余弦项，方差几乎为零。
- **难点**：球形光源的投影形状没有简洁的反 CDF。
- **Peters 的 trick**：分解为 cut disk。cut disk 是可高效直接采样的基本形，复合成近似投影立体角分布。
- **性能**：比朴素立体角采样贵 2-3×，但噪声 **数量级**降低——1 spp 出干净软阴影的代价。
- **误差可证**：即使是近似分解，也给出上界。
- **勘误**：论文 Algorithm 2/3/4 里传给 `SampleCutUnitDisk()` 的第一参数应减 $\pi/2$。**附带源代码一直是正确的**，实现者请以源码为准。

## 链接到的概念

- [[projected-solid-angle-sampling]]
- [[poisson-disk-sampling]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/I3D2019.html
- 论文：[Official version](https://doi.org/10.1145/3320282)
- 本地：`raw/articles/momentsingraphics.de/2019-05-22_sampling-projected-spherical-caps-in-real-time.md`
