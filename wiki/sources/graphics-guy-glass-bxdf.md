---
tags: [source, 渲染, pbr, 微表面, 折射, bxdf, agraphicsguynotes]
date: 2026-04-27
sources: 1
---

# Glass Material Simulated by Microfacet BXDF（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2015 年 11 月的文章，把 [[microfacet-brdf]] 模型从粗糙金属推广到粗糙玻璃材质，推导微表面 BTDF（折射项）并在 SORT 渲染器中实现。

## 摘要

文章基于 Walter et al. 2007（Cornell/EGSR）的论文，将微表面理论从纯反射扩展为同时处理反射与折射的完整 BXDF。核心思路是把「微表面由理想镜面组成」改为「微表面由理想透射面组成」，则同一套 NDF、几何遮蔽项 $G$ 就能推导出微表面 BTDF。最终 BXDF 等于微表面反射 BRDF 加微表面折射 BTDF。折射方向由 Snell 定律给出（含折射率 IOR 表格），全内反射的判定通过根号项负值检测；Fresnel 项决定反射/折射的能量分配，采样时先按 Fresnel 权重随机选择折射或反射路径，再按 NDF 采样微表面法线，最后计算对应 BXDF 值。BTDF 的 Jacobian $|\partial \omega_h / \partial \omega_o|$ 与 BRDF 不同，需要单独推导。

## 关键要点

- 微表面折射假设：微表面由理想透射面而非镜面组成，$D$、$G$ 复用，BTDF 多出 $\eta^2$ 因子和不同的 Jacobian
- Snell 定律：折射方向 $V_r = -(\eta_i/\eta_o) V_i + N((\eta_i/\eta_o)(V_i \cdot N) - \sqrt{1 - (\eta_i/\eta_o)^2(1-(V_i \cdot N)^2)})$
- 全内反射：当 $1 - (\eta_i/\eta_o)^2(1-(V\cdot N)^2) < 0$ 时触发，Fresnel 项须为 1，必须正确处理否则路径在介质内终止
- 纯折射 BTDF vs 纯反射 BRDF：反射 BRDF 的 Fresnel 项用 transmittance 方向而非反射方向求值（此处作者注明原因不明，遵循其他渲染器实践）
- 采样策略：按 Fresnel 权重在反射 / 折射路径中随机二选一，再按 NDF 采样微表面法线，计算对应 BXDF

## 链接到的概念

- [[microfacet-brdf]]
- [[refractive-glass-shader]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/glass_material_simulated_by_microfacet_bxdf/
- 本地：`raw/articles/agraphicsguynotes.com/2015-11-11_glass-material-simulated-by-microfacet-bxdf.md`
