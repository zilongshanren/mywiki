---
tags: [source, 渲染, 蒙特卡洛, importance-sampling, mis, 方差]
date: 2026-04-27
sources: 1
---

# Monte Carlo Integral with Multiple Importance Sampling（Jiayin Cao / A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 8 月的文章，基于 Veach 博士论文详解 MIS 的数学推导与三种权重启发式。

## 摘要

文章先铺 Monte Carlo 积分的标准形式，证明无偏性（$E[F_N] = I$）和一致性（$V[F_N] = V[f/p]/N \to 0$），并澄清这两个性质的区别——unbiased 看期望、consistent 看收敛，二者不互相蕴含（光子映射是 consistent 但 biased 的例子）。重要性采样的核心是让 pdf 形状逼近被积函数，从而降低方差常数因子。MIS 的核心贡献：当无法找到单一最优 pdf 时，用多套 pdf 各自采样后按权重合并，构造仍无偏的估计器 $F_{mis}$，只需满足权重之和为 1（$f(x)\neq 0$ 处）且 $p_i(x)=0$ 时 $w_i(x)=0$。Balance Heuristic 是最直接的权重选择：$w_i = n_i p_i / \sum_k n_k p_k$。Power Heuristic（$\beta=2$，PBRT 默认）把权重进一步集中到主导 pdf；Cutoff 和 Maximum Heuristic 则是更激进的近似。

## 关键要点

- Balance Heuristic 无偏且方差可证明不超过单 pdf 估计器。
- 极端尖峰形 pdf 应慎用于 MIS——在非尖峰区域 pdf 极小会放大其他 pdf 的权重，反而引入高方差。
- Monte Carlo $O(\sqrt{N})$ 收敛率与维度无关，这是它用于渲染方程的根本原因。
- 标准 MC 可看作 MIS 的特殊情形（所有 pdf 相同、$w_i = 1/N$）。

## 链接到的概念

- [[monte-carlo-integration]]
- [[importance-sampling-pdf-cancellation]]
- [[path-tracing-basics]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/monte_carlo_integral_with_multiple_importance_sampling/
- 本地：`raw/articles/agraphicsguynotes.com/2015-08-10_monte-carlo-integral-with-multiple-importance-sampling.md`
