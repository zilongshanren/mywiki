---
tags: [source, 渲染, brdf, 镜面反射, fresnel, delta-function]
date: 2026-04-27
sources: 1
---

# Derivation of Pure Specular Reflection BRDF（Jiayin Cao / A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 10 月的文章，补清 PBRT 第 8.2.2/8.2.3 节中一个令人困惑的 delta BRDF 推导。

## 摘要

PBRT 第 2 版 p.439 直接写下 $L_o = f_r L_i$，让读者误以为 $f_r = L_o / L_i$，丢失了 cosine 与立体角。Cao 按 errata 建议将等式修正为从渲染方程出发，并进一步推导完整的 delta BRDF。关键步骤：（1）从菲涅耳对辐通量的约束 $d\Phi_o = F_r d\Phi_i$ 出发，展开成辐射亮度形式，利用镜面条件 $\theta_i = \theta_o$、$\phi_i = \phi_o + \pi$ 消去对称项，得到 $L_o(\omega_o) = F_r(R(\omega_o)) L_i(R(\omega_o))$；（2）将 BRDF 分解为 $f_{other} \cdot \delta(\omega_i - R(\omega_o))$，代入渲染方程后 delta 函数消除积分，与步骤（1）连立消去辐射亮度，得到 $f_{other} = F_r / |\cos\theta_i|$，最终 BRDF 为 $f = F_r \delta / |\cos\theta_i|$。折射 BTDF 形式类似，多出 $(\eta_o/\eta_i)^2$ 因子与 Snell 定律的折射方向 $T$。

## 关键要点

- 纯镜面 BRDF 是 delta 函数：$f(\omega_i, \omega_o) = F_r(\omega_i)\,\delta(\omega_i - R(\omega_o)) / |\cos\theta_i|$。
- 分母 $|\cos\theta_i|$ 与渲染方程中的 $\cos\theta_i$ 因子互相抵消，求和时可以化简。
- 折射 BTDF：$f = (1-F_r)(\eta_o/\eta_i)^2 \delta(\omega_i - T(\omega_o)) / |\cos\theta_i|$。
- 这两个公式是 microfacet BRDF 在 roughness → 0 极限情形的解析形式。

## 链接到的概念

- [[microfacet-brdf]]
- [[importance-sampling-pdf-cancellation]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/derivation_of_pure_specular_reflection_brdf/
- 本地：`raw/articles/agraphicsguynotes.com/2015-10-22_derivation-of-pure-specular-reflection-brdf.md`
