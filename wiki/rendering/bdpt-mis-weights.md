---
tags: [rendering, path-tracing, bdpt, mis, offline-rendering]
date: 2026-04-27
sources: 1
---

# 双向路径追踪中的 MIS 权重（BDPT MIS Weights）

双向路径追踪（Bidirectional Path Tracing，BDPT）将从相机和从光源分别追踪的子路径相连，形成多种采样策略。朴素做法对每条路径使用均匀权重，效果很差。[[rendering/monte-carlo-integration|多重重要性采样（MIS）]]通过 Veach 的 power heuristic 对不同策略加权，使 BDPT 真正实用。

## 为什么均匀权重不够

对于长度为 k 的路径，朴素 BDPT 有 k+1 种连接方式，均匀权重为 `1/(k+1)`。这意味着无论某种策略多么适合当前光照条件，其贡献都被平均稀释。实验表明，朴素 BDPT 在焦散场景中噪声极大，而有 MIS 的 BDPT 在相同渲染时间内明显更优。

## PDF 递推简化

MIS 权重的分母需要枚举所有同长度路径策略的 PDF 之和。直接计算每种策略的完整 PDF 既繁琐又容易出错。关键观察是：相邻策略（s 个相机顶点 vs s+1 个相机顶点）的 PDF 之比只与连接边附近的局部量有关：

```
p_{i+1} / p_i = forward_p_i / reverse_p_i
```

这个比值可以通过两个在路径追踪时逐顶点递推的辅助项来维护：

- `vcm_i = 1 / forward_p_i`
- `vc_i = (reverse_g_{i-1} / forward_p_i) × (vcm_{i-1} + reverse_p_{σ,i-2} × vc_{i-1})`

每个顶点只需额外存储两个浮点数，即可在路径追踪的同时完整跟踪所有策略的权重信息。

## 边界情况处理

**Delta 光源**（点光、聚光、方向光）：无法被随机光线命中，少一种采样策略，令 `vc_1 = 0`。

**无穷远光源**（天空球、方向光）：采样点在无穷远处，通过令 `g_0 = 1` 抵消距离项，使 MIS 权重计算数值稳定。

## 与 SmallVCM 的关系

SmallVCM 将 BDPT 扩展为 Vertex Connection and Merging（VCM），在此基础上引入光子映射式的顶点合并。文章中的 `vc` / `vcm` 命名直接来自 SmallVCM 论文，有助于对照阅读代码。

## Sources

- [[sources/graphics-guy-mis-bdpt]]
