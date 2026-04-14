---
tags: [source, 数学, 概率, 蒙特卡洛]
date: 2026-04-14
sources: 1
---

# Monte Carlo Crash Course — Continuous Probability（Max Slater）

[[max-slater|Max Slater]] *Monte Carlo Crash Course* 系列的**第一章 Continuous Probability**（2025 年 3 月）。整个系列计划有连续概率、蒙特卡洛指数改进、采样、渲染案例、QMC 共 5+ 章，本章是数学前置——为后续所有估计器、采样器、BRDF 积分打好记号。已存在的 [[sources/slater-qmc-crash-course]] 对应的是系列的**第 5 章**，本文与之**独立**。

## 摘要

文章假设读者熟悉离散概率与多变量微积分，用一章篇幅把连续概率重新梳理一遍：先说明为什么连续随机变量不能有「单点概率」——任何值都必须为零——从而引出**概率密度函数**（PDF）的定义，它是 $\mathbb{P}\{z \le Z < z+h\}/h$ 在 $h \to 0$ 极限下的值。随后联系 **CDF** $F_Z(z) = \mathbb{P}\{Z < z\}$，指出 PDF = CDF 的导数，CDF = PDF 的积分，用这个对偶去建立逆变换采样的基础。继续介绍联合 PDF、边缘化、独立 / 条件分布；然后是期望（及其对依赖变量的线性性）、方差、协方差、Markov 与 Chebyshev 不等式；最后用 **Dirac delta** 统一描述离散分布、混合分布与图形学里常见的完美镜面 BRDF。

## 关键要点

- **连续情形下单点概率恒为零**，必须谈密度而不是质量。
- **PDF 的几何意义**：区间概率对区间长度的极限比值。
- **CDF 是 PDF 的原函数**——逆变换采样的理论出处。
- **期望线性性对依赖变量也成立**，这是蒙特卡洛能拆项估计的基础。
- **方差不是线性的**：$\mathrm{Var}[X+Y] = \mathrm{Var}[X] + \mathrm{Var}[Y] + 2\mathrm{Cov}[X,Y]$。
- **零协方差不蕴含独立**，只说明线性相关为零。
- **Markov 不等式**：非负 $X$ 满足 $\mathbb{P}\{X \ge a\} \le \mathbb{E}[X]/a$；**Chebyshev** 是它套到 $(X-\mu)^2$ 的推论。
- **Dirac delta** 把离散分布装进连续 PDF 语言，对渲染里的完美镜面 BRDF 尤其好用——镜面项本质是 delta。
- **本文仅是前置**：蒙特卡洛估计器的方差分析、大数律、中心极限、重要性采样属于后续章节。

## 链接到的概念

- [[continuous-probability]]
- [[quasi-monte-carlo]]（系列第 5 章，另一篇同系列的 source summary 已存在）
- [[spherical-integration]]
- [[probabilistic-algorithms]]
- [[functions-as-vectors]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Probability/
- 本地：`raw/articles/thenumb.at/2025-03-29_monte-carlo-crash-course.md`
