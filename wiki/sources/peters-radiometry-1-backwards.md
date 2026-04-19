---
tags: [source, 渲染, 辐射度量, 路径追踪, 数学, 教学]
date: 2026-04-19
sources: 1
---

# Radiometry, part 1: I got it backwards（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2025 年 1 月的 radiometry 系列第 1 篇，主张用**积分的视角**重新组织辐射度量的概念体系——radiance 为第一公民，其它量都是 radiance 的积分。

## 摘要

PBRT 等传统教材从 radiant energy 出发，用"可疑的 differential" 记号逐步推出 radiance。Peters 认为这个路径对"写 path tracer"不友好——记号 $\mathrm{d}\Phi / \mathrm{d}A$ 不是高中意义下的导数，初学者易困惑。他的反向路径：从**radiance** $L(x, t, \omega)$ 起步（物理意义：理想 pinhole 相机像素值的线性对应），其关键性质是**真空中沿射线守恒** $L(x) = L(x + s\omega)$，这直接解释 ray tracing 为什么管用。其它量都从 radiance 积分而来：**Irradiance** $E(x, t, n) = \int_{\mathbb{S}^2} L \cdot |n \cdot \omega|\,d\omega$（Lambertian 表面能收到的光）；**radiant flux** $\Phi = \int_A E\,dx$（表面总收光量，area light 标定用）；**radiant energy** $Q = \int \Phi\,dt$（时段总能量，接通 SI 焦耳）；**intensity** $I_A(\omega) = \int_A L \cdot |n \cdot \omega|\,dx$（某方向总辐射，IES profile 用）。相机的曝光可以看成"从 radiant energy 经 flux、irradiance 一路限到 radiance"的近似。用积分替代可疑 differential 后，"要不要乘 cos、除 $4\pi$ 或 $r^2$" 等日常问题可以直接从定义里读出答案。

## 关键要点

- **Radiance 为第一公民**：沿射线守恒，对应相机像素值。
- **其它量都是 radiance 的积分**：irradiance 在 $\mathbb{S}^2$ 上积、flux 在 area 上、energy 在 time 上。
- **cosine term 是几何原因**，不是 Lambert 反射模型强加的。
- **光源标定选 flux/watts**：灯泡大小变化时总能量守恒。
- **不用 differential 记号**：path tracer 本来就在算积分，和本质直接对齐。

## 链接到的概念

- [[radiometry-integral-view]]
- [[path-tracing-basics]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/Radiometry1Backwards.html
- 本地：`raw/articles/momentsingraphics.de/2025-01-12_radiometry-part-1-i-got-it-backwards.md`
