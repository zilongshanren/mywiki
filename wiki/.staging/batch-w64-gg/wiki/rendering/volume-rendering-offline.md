---
tags: [渲染, 体积渲染, 离线渲染, pbrt, 光线追踪]
date: 2026-04-19
sources: 1
---

# 离线渲染中的体积渲染（Volume Rendering）

离线体积渲染把「雾、烟、水、光柱」统一建模为微观粒子与光线的四类交互——**absorption（吸收）、emission（发射）、out-scattering（外散射）、in-scattering（内散射）**。实时方案多用 billboard 粒子加 alpha 混合来假装体积，是有偏近似；离线方案的优势是把所有情况纳入同一套物理，代价是积分变重。[[Jiayin Cao]] 在博客里啃了 PBRT 第二版的体积章节，把书里跳过的若干推导补齐——这页记录他的核心结论。

## 四种相互作用

- **Absorption**：光穿过体积时按指数衰减，微分形式 $dL = -\sigma_a L\, dt$。均匀体积积分起来就是熟悉的 Beer-Lambert 定律 $e^{-\int \sigma_a dt}$。
- **Out-scattering**：与 absorption 在「衰减」这一面等价，只是把光偏转到别的方向。工程上把二者合并成 **extinction coefficient** $\sigma_t = \sigma_a + \sigma_s$，并定义 **beam transmittance** $T_r = e^{-\int \sigma_t dt}$。
- **Emission**：最简单，$dL = L_e dt$。
- **In-scattering**：最复杂——别处的光被粒子偏转进当前方向。微分方程形式 $\frac{dL}{dt} = -\sigma_t L + S(p)$ 是**一阶线性 ODE**，可通过积分因子法解出经典形式：

$$L(p_0) = \int_0^{\infty} T_r\!\big(p(t) \to p_0\big)\, S\!\big(p(t)\big)\, dt$$

含义：观察点沿 $-\omega$ 方向的辐亮度 = 沿途所有位置的内散射源 $S$，各自被对应段的 beam transmittance 衰减后累加。

## PBRT 没讲清楚的推导

PBRT 给出上述方程但略过了从微分式到积分式的细节。Cao 的做法：先把方向反转（因为微分沿 $\omega$、积分沿 $-\omega$），再用标准一阶 ODE 解公式
$$L(t) = \frac{1}{e^{-\int \sigma dt}}\Big(-\!\int e^{-\int \sigma dt} S dt + C\Big),$$
用边界条件 $L(\infty) = 0$ 定 $C$，最终简化到上述 beam transmittance 形式。

## 与其他主题的关系

- **与 BRDF 渲染方程的对照**：体积渲染方程是把面积积分拓展到体积积分，结构相似但维度多一维。
- **Subsurface Scattering**：SSS 本质就是局限在物体内部的体积渲染，[[sss-practical-implementation]] 的 BSSRDF 与这里的 extinction/phase function 同源。
- **离线 vs 实时**：Shadertoy 的 volumetric demo 会用 ray marching + 常数 step 近似这套积分；PBRT 级别的实现会做 ratio tracking / delta tracking 无偏采样。

## 相关

- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[spectral-rendering]]
- [[volumetric-raymarching-intro]]
- [[sss-practical-implementation]]
- [[graphics-guy-notes]]

## Sources

- [[sources/graphics-guy-volume-rendering-offline]]
