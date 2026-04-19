---
tags: [source, 渲染, 实时光追, ReSTIR, 采样]
date: 2026-04-19
sources: 1
---

# Understanding The Math Behind ReSTIR DI（A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2022 年 12 月的长文，是对原 ReSTIR DI 论文（NVIDIA 2020）的数学补完——不谈工程实现，专门把作者自己读论文时踩过的坑一一解释清楚。

## 摘要

作者把 ReSTIR DI 背后的数学拆成两半：前半覆盖 importance sampling、MIS（及其两条合法性条件）、Sample Importance Resampling、Resampled Importance Sampling、Weighted Reservoir Sampling，交代每个算法的证明与"坑点"（例如 uniform MIS weight 为何不满足 MIS 第二条件、为何 SIR target function 不需要归一化、WRS 的分治性质）。后半回到 ReSTIR DI 本身，逐一回答作者读论文时没搞懂的问题：为什么所有像素实际用的是同一个 proposal PDF（light 候选 × 条件 PDF 的乘积才是完整 PDF）；邻居 target function 不同为何还无偏（把邻居当 SIR PDF，套 MIS+RIS）；`W` 作为 SIR PDF 倒数的无偏估计如何合法替换；邻居 reservoir 的 "N 倍权重" 代表什么；temporal reuse 为何比 TAA 无偏；visibility reuse 背后的 per-initial-candidate target function 性质。最后解释 ReSTIR DI 的偏差根源（uniform MIS weight 不满足第二条件）及修正（数 non-zero PDF 的个数）。

## 关键要点

- target function 不需归一化，恒定缩放被 RIS 分子分母自动抵消。
- SIR PDF 不可解析，但 `W = (1/M) (1/p̂(y)) Σ p̂(x_i)/p_i(x_i)` 的期望精确等于 SIR PDF 的倒数，可在 RIS 估计器里替换。
- 邻居 target sample 合并时权重为 `(p̂_a/p̂_b) · r_b.w_sum`；邻居 reservoir 用 `p̂(x)·W(x)·N` 一次性"带 N 倍"入主 reservoir，O(1) 完成等价的 N 次投递。
- uniform MIS weight 是为了兼容 SIR PDF 不可解析 + streaming + 计算量约束而做的妥协；代价是 bias 修正需要数"非零 PDF"的个数——SIR PDF 是否非零可从 target function 与 proposal PDF 同时非零来预测，这一性质也可解决 visibility reuse 的偏差判定。
- Temporal reuse 存的是**未评估的 light sample**，最坏是低质量样本，不破坏无偏性；TAA 存的是**已评估的颜色**，遮挡与光照变化会让它偏。
- Visibility reuse 的正当性：把前半段"用无阴影 target 选 light sample"视为独立 SIR，后半段当前像素 reservoir 从未见过这些 light proposal，允许换 target function。

## 链接到的概念

- [[restir-di-math]]
- [[monte-carlo-integration]]
- [[importance-sampling]]
- [[mis-balance-heuristic]]
- [[path-tracing-basics]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/understanding_the_math_behind_restir_di/
- 本地：`raw/articles/agraphicsguynotes.com/2022-12-05_understanding-the-math-behind-restir-di.md`
