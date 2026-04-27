---
tags: [source, procedural-generation, sampling, mathematics, infinite-world]
date: 2026-04-27
sources: 1
---

# Infinite Uniform Point Distributions（Boris The Brave）

[[boris-the-brave]] 2024 年 10 月发布的数学向文章，探讨如何在无限平面上生成真正均匀的随机点分布，并给出基于泊松点过程（Poisson Point Process）的正确解。

## 摘要

文章从「均匀分布」的定义出发，指出最常见的 **jittered grid（抖动网格）** 并不是真正独立均匀分布——每个格子恰好有一个点，导致点之间存在隐性负相关，无法出现自然均匀分布特有的「随机簇集与空洞」感。正确的无限均匀分布在数学上等价于**泊松点过程（Poisson Point Process）**：对任意形状区域，落在其中的点数服从以 `ρ·面积` 为参数的泊松分布，且各区域独立。推导路径是极限过程：把有限矩形里的二项分布 B(ρN²,1/N²) 在 N→∞ 时收敛到泊松分布。实现上沿用 chunking 策略——每个 chunk 先用泊松采样确定点数，再在 chunk 内均匀散布——chunk 大小取 1/√ρ 使平均每块恰好 1 个点，与 jittered grid 一致但不再有单点约束。

## 关键要点

- Jittered grid 不是独立均匀分布，每格强制 1 点导致点间负相关
- 真正的无限均匀分布 = Poisson Point Process，点数满足 Poisson(ρ·A) 分布
- 极限推导：B(ρN², 1/N²) → Poisson(ρ)
- 实现：chunk 内先采泊松分布得点数 n，再均匀散布 n 个点
- 推荐 chunk 大小 = 1/√ρ（平均每块 1 点，与 jittered grid 密度相同）
- 视觉差异微妙，但理论上更接近「无限均匀分布」的数学定义

## 链接到的概念

- [[poisson-point-process-infinite-plane]]
- [[rendering/poisson-disk-sampling]]
- [[rendering/poisson-rect-process]]
- [[game-development/infinite-chunked-procedural-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2024/10/30/infinite-uniform-point-distributions/
- 本地：`raw/articles/boristhebrave.com/2024-10-30_infinite-uniform-point-distributions.md`
