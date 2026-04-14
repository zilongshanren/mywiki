---
tags: [source, 渲染, 球谐, 小波, 全局光照, 球面基]
date: 2026-04-14
sources: 1
---

# Implementing Needlets（Robin Green / Bases and Frames）

[[robin-green]] 2016 年的文章，讲解如何把宇宙学家用来分析 Cosmic Microwave Background（CMB）的球面小波基 **Needlet** 实现出来，作为[[spherical-harmonics|球谐]]的局部化替代品用于[[needlets|PRT 类场景]]。这篇是他和 Mannie Ko 在 GDC 2012 *Math for Game Programmers* 课程中 *Frames, Quadratures and Global Illumination: New Math for Games* 讲座的技术补充。

## 摘要

SH 作为全局基在处理带掩码（galactic cut）的信号时会在 mask 边界发生严重振铃——因为 SH 基是整个球面同时定义的。宇宙学家面对 Planck 等仪器给出的 50M 像素全天图数据，需要一个**本地化**、**球面原生**、**旋转不变**且**保范数**的基，Needlet 恰好满足全部性质。代价是 Needlet 不是正交基而是 **tight frame**——于是失去了渐进逼近的能力，但保留了其它所有性质。

实现过程按 Marinucci 等 2008 年论文的配方走：

1. 构造 [[needlets|Littlewood-Paley 分解]]：从一个 piecewise 指数 bump 函数 $f(t)$ 开始，对其做数值积分（Simpson 二次规则）得到单位分划函数 $\psi(x)$，分母常数为 0.4439938162；再构造分段函数 $\varphi(x)$，最后取正根得到权重函数 $b(\xi) = \sqrt{\varphi(\xi/B) - \varphi(\xi)}$。
2. 这些权重以整数索引采样后得到一张 band 级别的离散权重表，非零段的索引范围是 $[B^{j-1}, B^{j+1}]$。
3. Needlet 本身定义为一组 [[spherical-harmonics|SH]] 基的加权和，但单 band 内所有 SH 之和可以化简为一个 **Legendre 多项式** $P_\ell(\cos\gamma)$，其中 $\cos\gamma = \vec{e}_i \cdot \vec{e}_k$ 是两个方向向量的点积。
4. Legendre 多项式用 Bonnet 递推 $(n+1) P_{n+1} = (2n+1)\,x\,P_n - n\,P_{n-1}$ 迭代生成，从 $P_0 = 1, P_1 = x$ 开始——代码中顺便把预热和累加两段共享同一个递推。
5. 最终每个 Needlet 是一个关于 $x = \vec{e}\cdot\vec{e}_k$ 的一维函数，可以查表 + 线性/二次插值重建，而不用像 SH 一样现场评估每个基。

Needlet 的图形直观是「高度方向性的球面 wavelet」：能量几乎全部集中在主方向，几乎没有 SH 那种绕到球面另一侧的「ghost light」伪影；每个 Needlet 在球面上的积分为零（因为是零均值函数的正加权和）。

文章结尾读者指出 `integrate_g_simpson` 循环条件有打字错误（原文 `for (uint32_t i=1; i < t; nn; i += 2)` 应为 `for (uint32_t i=1; i < nn; i += 2)`）。

## 关键要点

- Needlet 是球面上的**局部化**基，解决 SH 在 galactic-cut / 遮挡 mask 边界振铃的问题。
- Needlet 是 tight frame 而非 ONB：失去 successive approximation，保留能量保持、旋转不变、自然球面嵌入。
- 实现配方完整：Littlewood-Paley 权重 → 离散 $b(j)$ 表 → 对每个 band 用 Bonnet 递推累加 Legendre 多项式 → 得到一个关于 $\cos\gamma$ 的 1D 函数。
- 单 band 内 SH 之和 = 单个 Legendre 多项式，这让评估代价退化到 $O(\ell)$ 而不是 $O(\ell^2)$。
- Needlet 可以提前打成 1D 查找表做线性/二次插值，非常适合实时 lookup。

## 链接到的概念

- [[needlets]]
- [[spherical-harmonics]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2016/05/22/implementing-needlets/
- 本地：`raw/articles/basesandframes.wordpress.com/2016-05-22_implementing-needlets.md`
