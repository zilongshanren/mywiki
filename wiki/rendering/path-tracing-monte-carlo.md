---
tags: [rendering, path-tracing, monte-carlo, global-illumination]
date: 2026-04-19
sources: 1
---

# Path Tracing 的 Monte Carlo 结构

Path tracing 是 Monte Carlo 积分应用到渲染方程的直接结果。[[max-slater]] *Monte Carlo Crash Course — Case Study: Rendering* 展示了把 2D 简化光传输一步步推到 3D 的过程。本页把这个主题作为连接 [[monte-carlo-integration]] 与实际渲染器的桥。

## 渲染方程回顾

```
L_o(x, ω_o) = Le(x, ω_o) + ∫_Ω  f_r(x, ω_i, ω_o) · L_i(x, ω_i) · cos θ  dω_i
```

积分遍布半球 Ω。**这个方程是无限递归的**——L_i 又等于某点的 L_o。直接数值求解不可行。

## 从 MC 估计器出发

单样本 MC 估计：

```
<L_o> = Le + f_r · L_i · cos θ / p(ω_i)
```

p 是采样 ω_i 的 PDF。选 p 的三大策略：

1. **Uniform hemisphere sampling**——p = 1/(2π)。可行但高方差。
2. **Cosine-weighted sampling**——p = cos θ / π，抵消 cos 因子，Lambert diffuse 下几乎免费减方差；
3. **BRDF importance sampling**——按 f_r 本身的形状采样，在 glossy/specular 下显著降方差。

## Next Event Estimation (NEE)

纯 BRDF 采样碰上**点光源或小面积光源**时几乎命不中，方差暴涨。**NEE** 在每个 hit 点额外做一次**显式向光源采样**：

```
<L_direct> = f_r · L_light · cos θ_x · cos θ_y / (|x-y|² · p_light)
```

覆盖了尖锐光源，但对 specular BRDF 又效果不好。

## Multiple Importance Sampling (MIS)

MIS 在 BRDF 采样和 light 采样间做**加权融合**，权重由 **balance heuristic** 决定：

```
w_s(x) = n_s · p_s(x) / Σⱼ n_j · p_j(x)
```

结果：glossy 表面自动偏 BRDF 采样；diffuse 表面 + 大光源自动偏 light 采样——不用手动调。MIS 是现代 path tracer 的标配。

## Russian Roulette

递归光路可以无限深，但深路径贡献小。RR 策略：

```
if recursion_depth > k:
    with probability q: terminate, return 0
    else: continue, but multiply throughput by 1/(1-q)
```

期望无偏，方差可控。q 通常取 1 - max(rgb_throughput)。

## 本 wiki 的渲染 MC 链

- **理论基础**：[[monte-carlo-integration]]、[[inversion-sampling-prng]]、[[continuous-probability]]；
- **采样技巧**：[[stratified-sampling]]、[[low-discrepancy-sequence]]、[[quasi-monte-carlo]]、[[poisson-disk-sampling]]；
- **表面模型**：[[microfacet-brdf]]、[[physically-based-shading]]；
- **球面数学**：[[spherical-integration]]、[[projected-solid-angle-sampling]]、[[spherical-harmonics]]；
- **专门应用**：[[instant-radiosity-vpl]]、[[radiance-cascades]]。

## Sources

- [[sources/slater-mc-rendering]]
