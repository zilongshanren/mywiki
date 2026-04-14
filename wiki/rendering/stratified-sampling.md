---
tags: [渲染, 蒙特卡洛, 采样, 方差缩减]
date: 2026-04-14
sources: 1
---

# 分层采样（Stratified Sampling）

**Stratified sampling** 把积分域 $\Omega$ 划分为 $M$ 个等大区域，每个区域独立取 $\tfrac{N}{M}$ 个样本。因为任一区域最多出现 $\tfrac{N}{M}$ 个样本，样本之间天然**负相关**——这就降低了方差。它是实现「负相关采样以降方差」最便宜的手段之一，而且是无偏的。

## 为什么它总不会更糟

把 $\mathrm{Var}[f(\Omega)]$ 按样本所属区域条件化，可以证明分层估计器的方差满足：

$$
\mathrm{Var}[F_\text{Strat}] \le \mathrm{Var}[F_\text{Unif}]
$$

等号成立当且仅当 $f$ 在各区域的均值都相等。也就是说：**$f$ 越「不均匀」，分层降方差越猛**。这和直觉一致——如果一块区域本身就比另一块亮，把样本挤在一起反而浪费。

## 动态分层（Dynamic Stratification）

固定 $M = 64$ 不会带来渐近改善：在 $d$ 维下，分层估计器的方差收敛率是

$$
\sigma \propto \frac{1}{M^{1/d}\sqrt{N}}
$$

受**维度诅咒**限制。一个巧妙的做法是让 $M \propto \sqrt{N}$ 动态增长：在 1D 下能达到 $\sigma \propto N^{-1}$（和 quadrature 同级别），2D 下 $N^{-3/4}$；高维则逐渐退化回 $N^{-1/2}$。所以**动态分层只在低维下划算**。

## 自适应采样（Adaptive Sampling）

如果各区域方差 $\sigma_m$ 不同，最优样本数应当**正比于 $\sigma_m$**（Lagrange 乘子法可证）。问题是 $\sigma_m$ 事先不知道，只能边积分边估计——维护每区域的 $\mathbb{E}[f]$、$\mathbb{E}[f^2]$ 两个矩，随时刷新。

估计会很吵，所以即使某区域估计方差是 0，也必须给它一个非零的采样概率——否则「看起来平」的区域可能被漏掉。把自适应采样和动态分层糅在一起就是 **multi-level Monte Carlo**。

## 高维退路：Latin Hypercube

当维度高到分层不可行（$M^d$ 爆炸）时，Latin hypercube 沿**每个维度独立分层再打乱**，本质是分层的稀疏近似——相关性弱很多，但计算可行。

## 相关

- [[quasi-monte-carlo]] — 另一条减方差路线（用确定性换随机性）
- [[low-discrepancy-sequence]] — Sobol 系列可以视为带分层的低差异序列
- [[poisson-disk-sampling]] — 空间分布上的「硬约束」式负相关
- [[max-slater]]

## Sources

- [[sources/slater-qmc-crash-course]]
