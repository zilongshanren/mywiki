---
tags: [source, 渲染, brdf, 微表面, importance-sampling, ggx, beckmann, blinn, ndf]
date: 2026-04-27
sources: 1
---

# Sampling Microfacet BRDF（Jiayin Cao / A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 11 月的文章，推导 GGX / Beckmann / Blinn 三种 NDF 的 isotropic importance sampling 公式。

## 摘要

文章从一个直观问题出发：用默认 cosine-weighted 采样（pdf ∝ cosθ）对 roughness=0 的 microfacet BRDF 采样时，蒙克效果极差（图示左右两只猴子对比）。原因是 NDF 在 roughness→0 时趋近 delta 函数，余弦采样极少命中非零 BRDF 区域；偶然命中的样本因 pdf 极小而权重爆炸，方差剧增。正确做法是直接对 NDF 采样：先推导 pdf $p_h(\theta, \phi) = D(h)\cos\theta\sin\theta$，由于各向同性，$\phi$ 可均匀采样；$\theta$ 通过反变换法（inversion method）求解 CDF 的逆函数。GGX CDF 反解给出 $\theta = \arccos\sqrt{(1-\epsilon)/(\epsilon(\alpha^2-1)+1)}$；Beckmann 给出 $\theta = \arccos\sqrt{1/(1-\alpha^2\ln(1-\epsilon))}$；Blinn 最简洁 $\theta = \arccos(\epsilon^{1/(\alpha+2)})$。最后一步：NDF 采出半程向量法线，需通过 Jacobian $d\omega_h/d\omega_i = 1/(4(\omega_o\cdot\omega_h))$ 转换到入射方向的 pdf。

## 关键要点

- 所有三种 NDF 的 $\phi$ 方向均匀采样，只有 $\theta$ 不同。
- Jacobian 转换是经常遗漏的最后一步，将半程向量 pdf 转为入射方向 pdf。
- Blinn 在 PBRT 与 Mitsuba 中采用 $(\alpha+1)$ 而非 $(\alpha+2)$，差异源自对 NDF 归一化条件的不同定义——实际渲染差异微小。
- 这是各向同性版本；各向异性版本需要将 $\theta$ 和 $\phi$ 耦合推导，见 [[anisotropic-microfacet-sampling]]。

## 链接到的概念

- [[microfacet-brdf]]
- [[anisotropic-microfacet-sampling]]
- [[importance-sampling-pdf-cancellation]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/sample_microfacet_brdf/
- 本地：`raw/articles/agraphicsguynotes.com/2015-11-01_sampling-microfacet-brdf.md`
