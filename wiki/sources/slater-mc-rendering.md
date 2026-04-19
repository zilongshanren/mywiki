---
tags: [source, math, monte-carlo, path-tracing, rendering]
date: 2026-04-19
sources: 1
---

# Monte Carlo Crash Course — Case Study: Rendering（Max Slater）

[[max-slater]] *Monte Carlo Crash Course* 系列第四章（2025 年 4 月 19 日）。将前三章的 Monte Carlo 理论（积分收敛率 + 采样方法）应用到计算机图形学的核心方程：渲染方程。作者用 2D 简化光传输把思路讲清，再推回 3D。

## 摘要

- **Radiance 定义**：L_i(x, θ) 表示点 x 沿方向 θ 入射的光量。
- **Direct lighting**：追射线到 hit.light，返回 emission；不 hit 光源返回 0。这是最基本的 MC 估计器。
- **Hemisphere sampling**：渲染方程需要对半球 Ω 积分，cosine-weighted 样本能匹配 Lambert diffuse 反射的 cos θ 因子，有效降方差。
- **Indirect lighting / Path tracing**——递归地追射线、在每个 hit 点再采样新方向，直到 Russian roulette 终止或命中光源。
- **Importance sampling**：按 BRDF × Li × cos θ 的形状采样比均匀采样方差小得多。具体实现通常按 BRDF 采样（易于得到闭式 CDF）。
- **Russian roulette**：每步有概率 q 终止、1-q 继续乘 1/(1-q)——无偏地截断无限路径。
- **Next event estimation (NEE)**——在每个 hit 点额外显式向光源采样，大幅降低 Dirac 光源的方差。
- **Multiple Importance Sampling (MIS)**：把 BRDF 采样和 light 采样融合，用 balance heuristic 自动在 glossy/diffuse、小/大光源之间切换。

## 关键要点

- **Rendering equation 是 MC 的天然战场**——高维、递归、无显式解析形式，正是「从 quadrature 到 MC」的动机来源。
- **Cosine-weighted hemisphere sampling** 是一个最小可用 importance sampling 的落地范例。
- **NEE + MIS** 是现代 path tracer 的标配——没这两样，方差会在 glossy 或尖锐光源上暴涨。
- **Russian roulette** 不是 hack 而是保证无偏性的正式概率构造。

## 链接到的概念

- [[path-tracing-monte-carlo]]
- [[monte-carlo-integration]]
- [[inversion-sampling-prng]]

## 原文

- 链接：https://thenumb.at/Rendering/
- 本地：`raw/articles/thenumb.at/2025-04-19_monte-carlo-crash-course.md`
