---
tags: [source, 渲染, 数学, 积分, 坐标变换]
date: 2026-04-14
sources: 1
---

# Spherical Integration（Max Slater）

[[max-slater|Max Slater]] 2023 年 1 月的短文，副标题「Or, where does that $\sin\theta$ come from?」。目标只有一个：把球面积分时凭空冒出的 $\sin\theta$ 因子的来龙去脉讲清楚。是 Slater 数学小品的典型一篇——短、直白、既给直觉也给形式推导。

## 摘要

从一个反例开始：对常数 1 在 $(\theta, \phi)$ 的矩形域上做双重积分，得到 $2\pi^2$，而不是球面积 $4\pi$——因为你积分的是一块平面矩形，不是球面。正确的微元面积是 $dS = \sin\theta\,d\theta\,d\phi$，文章用两种方式说明：(1) 直观上纬度越靠近极点，一圈经度对应的弧长越短（半径是 $\sin\theta$），所以等 $(d\theta, d\phi)$ 方块在球面上面积越小；(2) 形式推导：球坐标到 $\mathbb{R}^3$ 的参数化 $\Phi(\theta, \phi)$ 两条偏导的叉积模长恰好化简为 $|\sin\theta| = \sin\theta$（因 $\theta \in [0, \pi]$）。这也是渲染里经常写的**微分立体角** $d\omega = \sin\theta\,d\theta\,d\phi$。文章以脚注形式指出：这只是更一般的微分几何尺度因子（第一基本形式行列式开方 / 雅可比行列式）的一个特例。

## 关键要点

- **$\sin\theta$ 不是魔法**：是球坐标到笛卡尔坐标变换引入的参数化尺度因子。
- **一般公式**：对 $\mathbf{r}(u,v)$ 参数化的 3D 曲面，$dS = \|\partial_u \mathbf{r} \times \partial_v \mathbf{r}\|\,du\,dv$。
- **更一般的视角**：同维度坐标变换的尺度因子是雅可比行列式；嵌入子流形则是第一基本形式 $\mathrm{I}$ 行列式的开方 $\sqrt{\det\mathrm{I}}$。
- **差分直觉**：一个 $(\theta, \phi)$ 小矩形映到球面后变成曲面平行四边形，其面积就是两条切向量的叉积模长。
- **外微积分** 提供最干净的表述，作者说「以后会写」。
- 对渲染实践直接意义：均匀采样球面时的 $\theta$ 不能从 $U[0,\pi]$ 取，而要用 $\arccos(1 - 2u)$ 的反 CDF——$\arccos$ 来源正是这个 $\sin\theta$ 因子的积分。

## 链接到的概念

- [[spherical-integration]]
- [[spherical-harmonics]]
- [[projected-solid-angle-sampling]]
- [[continuous-probability]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Spherical-Integration/
- 本地：`raw/articles/thenumb.at/2023-01-08_spherical-integration.md`
