---
tags: [source, rendering, pbr, ibl]
date: 2026-04-19
sources: 1
---

# Image Based Lighting with Multiple Scattering（bruop.github.io）

[[bruno-opsenica|Bruno Opsenica]] 2019 年 8 月的 IBL 实战教程，从 Karis 2014 的 [[split-sum-approximation]] 走到 Fdez-Agüera 2019 的 [[ibl-multiple-scattering|多次散射补偿]]，全部在 BGFX 里用 compute shader 串起来。

## 摘要

文章先复述 GGX [[microfacet-brdf]]、Schlick Fresnel、Smith G2 以及 glTF 的 metal-rough 材质模型，然后解释为什么 IBL 不能在 shader 里对半球直接积分。接着分 Lambertian 漫反射（64³ 球形采样 irradiance map）、GGX 重要性采样（Hammersley + mip 采样技巧）、Karis split-sum（prefiltered env cubemap mip 链 + 128² RG16F BRDF LUT）三部分给代码。单次散射的 furnace test 暴露金属粗糙时明显变暗的能量亏损，作者因此实现 Fdez-Agüera 的多次散射补偿：仅用已有的 irradiance/LUT/prefiltered env 三张图再算 `FssEss + FmsEms`，炉子测试中金属球体完全消失。最后讨论 roughness-dependent Fresnel（`k_S = F0 + (max(1-r, F0) - F0)(1-NoV)^5`）与未覆盖事项（area light、LTC、prefilter 低粗糙度 aliasing）。

## 关键要点

- Karis split-sum：`∫ L_i D = (prefiltered env) × (environment BRDF LUT)`
- 用 [[microfacet-brdf|Smith height-correlated G2]]，BRDF LUT 存 `(f_a, f_b)` 的 scale/bias
- prefilter 时 Křivánek-Colbert 的 mip 采样技巧加速收敛
- Fdez-Agüera 多散射：`Ems = 1 - (f_a+f_b)`、`F_avg = F0 + (1-F0)/21`、`FmsEms = Ems·FssEss·F_avg/(1 - F_avg·Ems)`
- roughness-Fresnel 修正使光滑面 Fresnel 爬升更早

## 链接到的概念

- [[ibl-multiple-scattering]]
- [[split-sum-approximation]]
- [[microfacet-brdf]]

## 原文

- 链接：https://bruop.github.io/ibl/
- 本地：`raw/articles/bruop.github.io/2019-08-19_image-based-lighting-with-multiple-scattering.md`
