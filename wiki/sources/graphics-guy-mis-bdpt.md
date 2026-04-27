---
tags: [source, rendering, path-tracing, mis, bdpt, offline-rendering]
date: 2026-04-27
sources: 1
---

# Practical Implementation of MIS in Bidirectional Path Tracing（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2016 年 1 月的文章，系统讲解了在双向路径追踪（BDPT）中实现多重重要性采样（MIS）权重的完整推导与工程落地细节。

## 摘要

朴素双向路径追踪（Naive BDPT）对每条连接路径使用均匀权重 `1/(s+t)`，导致噪声与亮度异常并存——光追踪擅长焦散但整体噪声高，路径追踪焦散收敛极慢。MIS 通过 Veach 的 balance/power heuristic 对各采样策略进行加权混合，大幅降低噪声。文章聚焦一个关键工程技巧：利用相邻采样策略的 PDF 比值（forward/reverse PDF 的递推关系），将 MIS 权重计算简化为两个递推项 `vc_i` 和 `vcm_i`，每个顶点仅需额外存储两个浮点数即可高效完成权重评估，无需枚举所有路径。文章还针对 delta 光源（点光/方向光）和无穷远光源（天空球/方向光）给出了特殊处理方案。

## 关键要点

- 朴素 BDPT 的均匀权重几乎不带来比单向路径更好的质量，MIS 是使 BDPT 实用化的关键
- 路径 PDF 分解为前向 PDF（`p_s`）× 后向 PDF（`p_t`），MIS 权重依赖所有等长路径策略的 PDF 比值
- 利用递推关系 `p_{i+1}/p_i = forward_p / reverse_p` 避免逐策略重新求 PDF
- 两个辅助项 `vcm_i` 和 `vc_i` 可随路径追踪进行逐顶点递推，内存开销极小
- delta 光源使 `vc_i = 0`；天空球通过令 `g_0 = 1` 消去无穷远距离问题
- power heuristic 指数为 0 时退化为朴素 BDPT，方便对比调试

## 链接到的概念

- [[rendering/monte-carlo-integration]]
- [[rendering/path-tracing-basics]]
- [[rendering/importance-sampling-pdf-cancellation]]
- [[rendering/path-tracing-monte-carlo]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/practical_implementation_of_mis_in_bidirectional_path_tracing/
- 本地：`raw/articles/agraphicsguynotes.com/2016-01-16_practical-implementation-of-mis-in-bidirectional-path-tracin.md`
