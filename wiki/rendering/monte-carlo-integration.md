---
tags: [math, monte-carlo, integration, numerical-methods]
date: 2026-04-19
sources: 2
---

# Monte Carlo 积分

Monte Carlo 积分是渲染（尤其是 path tracing）能够工作的数学基础。[[max-slater]] 的 *Monte Carlo Crash Course* 把这个主题讲得比多数教科书都通——既有数学严谨（无偏、一致、方差）又有工程直觉（为什么高维非它莫属）。本页归拢本 wiki 中所有 MC 相关分支的**中心概念**。

## 核心公式

```
F_M = |Ω|/M · Σᵢ f(Uᵢ),   Uᵢ ~ Uniform(Ω)
```

- **F_M 是随机变量**——每次运行不同；
- **E[F_M] = ∫_Ω f dx**（无偏，unbiased）；
- **Var[F_M] = Var[f] / M**——所以**标准差 ∝ 1/√M**，与维度无关。

## 为什么「维度无关」这么重要

| 方法 | 误差缩放 | M 达到 ε 需要 |
|---|---|---|
| 1D 矩形 quadrature | O(1/N) | O(1/ε) |
| d 维 quadrature | O(1/N^(1/d)) | O(1/ε^d) — 指数爆炸 |
| Monte Carlo（任意维） | O(1/√M) | O(1/ε²) |

对于渲染方程（每次弹射引入两维方向 + 一维距离，递归深度 D 则 3D 维），quadrature 要的样本数是天文数字。MC 的 **1/√M 与维度无关** 让它成为唯一可行选项。

## 无偏 vs 一致

- **无偏**（unbiased）：E[F_M] = 真值，即「平均运行无穷多次一定对」；
- **一致**（consistent）：M → ∞ 时以概率 1 收敛到真值，但单次运行可能有偏。

很多渲染 biased 方法（photon mapping、light caching）虽然有偏但一致，实际使用中只要偏差可控就接受。

## 降方差是 MC 的主修课

原始 1/√M 虽与维度无关，但常数因子可能大到不可接受。**减方差**就是 MC 的工程重心：

1. **Importance sampling**——按 PDF 正比于 f 的形状采样（见 [[inversion-sampling-prng]]）；
2. **Stratified sampling**——把 Ω 切成子区域，每区域均匀采样（[[stratified-sampling]]）；
3. **Quasi-Monte Carlo**——用低差异序列替代随机（[[quasi-monte-carlo]] + [[low-discrepancy-sequence]]）；
4. **Russian roulette** 等递归截断技巧——保证无偏地终止无限递归；
5. **Next event estimation + MIS**——见 [[path-tracing-monte-carlo]]。

## 本 wiki 的 MC 链
- 本页：基础积分 + 为什么 1/√M；
- [[inversion-sampling-prng]]：如何在目标分布里采样；
- [[path-tracing-monte-carlo]]：把 MC 套到渲染方程；
- [[quasi-monte-carlo]]：用确定性替代随机进一步减方差；
- [[stratified-sampling]] / [[low-discrepancy-sequence]]：前置采样技巧；
- [[spherical-integration]]：球面/立体角的专门实践；
- [[continuous-probability]]：前置概率基础（Slater 系列第一章）。
- [[importance-sampling-pdf-cancellation]]：PDF 与 BRDF 分布项互相抵消——GGX prefilter 没有 weight 也没有 D 项的代数根因

## Sources

- [[sources/slater-mc-integration]]
- [[sources/slater-continuous-probability]]
