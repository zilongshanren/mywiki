---
tags: [source, rendering, importance-sampling, monte-carlo, brdf, ggx]
date: 2026-04-19
sources: 1
---

# Importance Sampling: Look Mom, No Weights（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 12 月一篇小结帖，解决从普通 Monte Carlo 跳到渲染专用 importance sampling 时"为什么代码里没有 weight 了"的常见 卡壳。

## 摘要

经典 importance sampling 的写法是"按 PDF 正比于 f 的形状采样，每个样本乘以与密度成反比的权重"——通用，但当 PDF 恰好取成 BRDF 某个分布项的形状（GGX 的 D、Lambert 的 cosine），最终估计里**分子的 BRDF 项与分母的 PDF 被精确抵消**，剩下的是一个更简的表达。实现层面的含义是：**你根本不需要再调用那个分布项函数**，也不需要带 sample weight。所以论文代码里 GGX 的 IS 版本只出现 Fresnel、geometry、lighting 的组合，没有 D 项、没有 weight，并非作者省略——作者**替你做了代数化简**。若故意选一个与 BRDF 不匹配的 PDF（比如对 GGX lobe 用 cosine-weighted PDF），IS 仍然无偏，但要把 weight 加回来、每个样本重算完整 BRDF——比均匀采样强，但离理想 IS 差一个数量级。这一条就是 Epic 的 Split-Sum / prefiltered environment map 能用的前提。

## 关键要点

- IS 用"按 PDF 采样" + "估计值为 f / PDF" 的框架
- 选 PDF ∝ BRDF 的分布项形状时，BRDF 与 PDF 在最终表达式里抵消
- 抵消后代码不再调用分布函数、不再乘 weight
- 错配的 PDF 仍然正确但收敛慢、必须手动加 weight
- GGX 的 inversion sample + D 消除是实时 IBL 预过滤的核心代数

## 链接到的概念

- [[importance-sampling-pdf-cancellation]]
- [[monte-carlo-integration]]
- [[inversion-sampling-prng]]
- [[microfacet-brdf]]
- [[path-tracing-monte-carlo]]
- [[parallax-corrected-cubemap]]
- [[anisotropic-microfacet-sampling]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/12/importance-sampling-look-mom-no-weights.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-12-10_importance-sampling-look-mom-no-weights.md`
