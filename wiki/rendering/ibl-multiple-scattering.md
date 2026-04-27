---
tags: [rendering, pbr, ibl, brdf]
date: 2026-04-19
sources: 1
---

# IBL 多次散射补偿

基于图像的光照（IBL）通常用 Karis 2014 的 split-sum 近似把镜面积分拆成 [[split-sum-approximation|prefiltered env map × BRDF LUT]]，但这个近似只包含了 GGX [[microfacet-brdf]] 的**单次散射**事件。粗糙金属的炉子测试（furnace test，环境均匀白光）会出现明显的能量亏损：球体越粗越暗，违背能量守恒。真实情况下，粗糙表面会发生多次微面反弹，如 Heitz 2015 用光线追踪基线所示。

Fdez-Agüera 2019（JCGT）给出一个无需额外 LUT 的实时补偿：将总反射分解为单次散射 `FssEss = k_S · f_ab.x + f_ab.y` 和多次散射 `FmsEms = Ems · FssEss · F_avg / (1 - F_avg · Ems)`，其中 `Ems = 1 - (f_ab.x + f_ab.y)` 是 BRDF LUT 丢失的能量，`F_avg = F0 + (1-F0)/21` 是平均 Fresnel。多次散射项被近似为漫反射，使用已存在的 irradiance map 采样，因此不引入新纹理。对非白电介质再乘以 diffuse albedo。Fdez-Agüera 还引入了"粗糙度相关 Fresnel"修正 `k_S = F0 + (max(1-roughness, F0) - F0) · (1-NoV)^5`，在更光滑表面增强 Fresnel 爬升。Bruop 在 BGFX 实现，金属炉子测试后球体几乎消失——能量守恒恢复。

窄光源（解析点光/方向光）下该近似失效，但 Stephen McAuley 2019 指出高粗糙度下 radiance map 已经很糊、接近 irradiance，实际差别不大。

## Sources

- [[sources/bruop-ibl-multiple-scattering]]
- [[sources/c0de517e-misunderstanding-multiscattering]] —— Pesce 2019：用 split-sum LUT 直接归一化的替代方案
