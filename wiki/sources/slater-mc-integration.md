---
tags: [source, math, monte-carlo, rendering]
date: 2026-04-19
sources: 1
---

# Monte Carlo Crash Course — Exponentially Better Integration（Max Slater）

[[max-slater]] *Monte Carlo Crash Course* 系列第二章（2025 年 4 月 5 日）。这是整个系列最核心的一章——解释为什么 Monte Carlo 在高维积分上比传统 quadrature 快到「不可比」的地步。已有 [[sources/slater-qmc-crash-course]] 记录系列最后一章，本页补上中间骨架。

## 摘要

作者从朴素梯形/矩形求积开始：一维 √x 的积分误差随 N 线性降低。进入二维开始暴露问题：为了保持同样精度，N² 个采样点才能达到类似效果。**d 维空间下错误随 1/√M 其中 M 是采样数**——这就是维度诅咒。对高维积分（渲染方程是无限维的重复弹射）quadrature 完全不实用。

Monte Carlo 的救赎：用**均匀随机采样**代替确定网格采样，平均值估计积分。它的关键性质是**误差 ∝ 1/√M**，**与维度无关**。数学上这由大数定律保证，方差上则由 Var(F_M) = σ²(f)/M 线性缩减得出。

章节还讨论：

- **无偏性**（bias）——MC 估计器的期望等于真积分；
- **一致性**（consistency）——M → ∞ 时几乎必然收敛；
- **均匀 MC 估计器公式**：F_M = |Ω|/M · Σᵢ f(Uᵢ)；
- **非均匀采样**的引入——为何我们还要做 importance sampling（减方差）。

## 关键要点

- Quadrature 在高维**失败**是因为 O(N^d) 样本需求，而 MC 的 O(1/√M) **不依赖维度**。
- 误差 ∝ 1/√M 可从方差线性叠加 + std dev = √variance 导出；前提是 f 有有限方差。
- **MC 估计器本身是个随机变量**——每次运行结果不同，讨论「收敛」要区分几乎必然收敛与依概率收敛。
- 均匀 MC 只是基线——真正好用的 MC 估计器要结合 **importance sampling**（下一章）减方差。

## 链接到的概念

- [[monte-carlo-integration]]

## 原文

- 链接：https://thenumb.at/Monte-Carlo/
- 本地：`raw/articles/thenumb.at/2025-04-05_monte-carlo-crash-course.md`
