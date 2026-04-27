---
tags: [渲染, pbr, 微表面, 折射, bxdf, 透射]
date: 2026-04-27
sources: 1
---

# 微表面 BTDF（Microfacet BTDF / 粗糙透射项）

**微表面 BTDF** 是将 [[microfacet-brdf|微表面理论]] 推广到折射（透射）的对应项。它把宏观表面的粗糙折射行为建模为无数理想透射微表面的统计平均，与反射 BRDF 一起组成完整的粗糙玻璃/介质 BXDF。

## 物理直觉

普通微表面 BRDF 假设每个 microfacet 是理想镜面。把这个假设换成「每个 microfacet 是理想透射面」，相同的 NDF $D$ 和遮蔽函数 $G$ 就能描述粗糙折射。当粗糙度趋近 0 时，BTDF 退化为纯 Snell 折射；当粗糙度较大时，透射方向发散为一个有宽度的 lobe，视觉上表现为磨砂玻璃效果。

## 微表面 BTDF 公式

Walter et al. 2007 推导的微表面折射 BTDF：

$$f_t(\omega_i, \omega_o) = \frac{|\omega_i \cdot h_t|\ |\omega_o \cdot h_t|}{|\omega_i \cdot n|\ |\omega_o \cdot n|} \cdot \frac{\eta_o^2 (1-F(\omega_i, h_t))\ G(\omega_i, \omega_o, h_t)\ D(h_t)}{(\eta_i(\omega_i \cdot h_t) + \eta_o(\omega_o \cdot h_t))^2}$$

其中 $h_t = -(\eta_i \omega_i + \eta_o \omega_o) / |\eta_i \omega_i + \eta_o \omega_o|$ 是折射半程向量（与反射半程向量定义不同）。$\eta_i / \eta_o$ 是两侧介质的折射率（IOR）。

与 BRDF 的主要差异是 Jacobian 不同：

$$\left|\frac{\partial \omega_h}{\partial \omega_o}\right| = \frac{\eta_o^2 |\omega_o \cdot h_t|}{(\eta_i(\omega_i \cdot h_t) + \eta_o(\omega_o \cdot h_t))^2}$$

这一因子在推导蒙特卡洛采样的权重时必须正确代入，否则能量不守恒。

## Snell 定律与全内反射

折射方向由 Snell 定律给出：$\eta_i \sin\theta_i = \eta_o \sin\theta_o$。向量形式：

$$V_r = -\frac{\eta_i}{\eta_o} V_i + N\left(\frac{\eta_i}{\eta_o}(V_i \cdot N) - \sqrt{1 - \frac{\eta_i^2}{\eta_o^2}(1-(V_i \cdot N)^2)}\right)$$

当光从高折射率介质（如玻璃，IOR≈1.5）进入低折射率介质（如空气）且入射角超过临界角时，根号项为负，发生**全内反射**——此时 Fresnel 项应严格等于 1，折射路径不存在。正确处理全内反射对避免路径在介质内部错误终止至关重要。

## 采样策略

完整的粗糙玻璃 BXDF 是反射 BRDF + 折射 BTDF 之和。采样时按 Fresnel 权重随机二选一（反射或折射），再从 NDF 采样微表面法线，最后计算对应的 BRDF 或 BTDF 值与 PDF 比值。这保证了反射与折射能量的正确分配。

## 相关

- [[microfacet-brdf]] — 反射侧的微表面 BRDF
- [[refractive-glass-shader]] — 实时渲染中的屏幕空间近似折射
- [[physically-based-shading]] — PBR 体系概览

## Sources

- [[sources/graphics-guy-glass-bxdf]]
