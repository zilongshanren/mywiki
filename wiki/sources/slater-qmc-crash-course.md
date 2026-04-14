---
tags: [source, 渲染, 蒙特卡洛, 采样, 数值积分]
date: 2026-04-14
sources: 1
---

# Monte Carlo Crash Course – Quasi-Monte Carlo（Max Slater）

[[max-slater|Max Slater]] 在 2025 年 8 月发布的 *Monte Carlo Crash Course* 系列的**第 5 章 Quasi-Monte Carlo**。整个系列从概率论基础讲到渲染应用，这一章专门讲「如何让蒙特卡洛收敛得更快」。

## 摘要

标准蒙特卡洛的误差是 $\sigma \propto \tfrac{1}{\sqrt{N}}$——在高精度场景下还是太慢。文章先讨论怎么用**负相关样本**打破独立假设来降方差：Poisson 盘采样（拒绝 + 最小距离）、[[stratified-sampling|分层采样]]（把域切成 $M$ 块每块等样本）、adaptive sampling（按方差估计分配样本）、Latin hypercube（每维度独立分层再打乱，避开高维诅咒）。然后换轨道讨论**放弃随机**的另一条路：[[quasi-monte-carlo|QMC]] 用确定性序列代替 PRNG，收敛率由点列的**星差（star discrepancy）**决定——Koksma–Hlawka 不等式给出误差上界。最后介绍 **Halton 序列** 作为最简单的 [[low-discrepancy-sequence|低差异序列]] 例子，以及高维退化 + scrambling 修正。

## 关键要点

- **Monte Carlo 收敛率上界来自方差**，不一定需要独立同分布；负相关样本可以突破 $N^{-1/2}$。
- **分层采样总不会更糟**：$\mathrm{Var}[F_\text{strat}] \le \mathrm{Var}[F_\text{unif}]$，等号成立当且仅当 $f$ 在各块上均值相同。
- **动态分层**：让 $M \propto \sqrt{N}$ 在 1D 能逼近 quadrature 的 $N^{-1}$ 收敛，但高维下退化到 $N^{-1/2}$。
- **Latin hypercube** 是分层的稀疏近似，适用于中等维度。
- **QMC 有偏但一致**：同种子同结果，只能加样本不能平均。
- **Koksma–Hlawka**：估计器误差 $\le V(f) \cdot D^*_N$，完全把误差推给点列本身。
- **低差异序列**的 $D^*_N \propto \tfrac{\log^d N}{N}$——低维下渐近优于随机。
- **Halton 序列**：每维用不同底的 radical inverse；高底在低样本数下分布差，scrambling 来救场。
- Sobol 是实践中更常用的低差异序列，但本章只预告未详细讲。

## 链接到的概念

- [[quasi-monte-carlo]]
- [[stratified-sampling]]
- [[low-discrepancy-sequence]]
- [[poisson-disk-sampling]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/QMC/
- 本地：`raw/articles/thenumb.at/2025-08-02_monte-carlo-crash-course.md`
