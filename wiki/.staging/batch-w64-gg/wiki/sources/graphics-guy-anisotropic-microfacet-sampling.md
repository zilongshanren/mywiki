---
tags: [source, 渲染, brdf, 微表面, importance-sampling]
date: 2026-04-19
sources: 1
---

# Sampling Anisotropic Microfacet BRDF（A Graphics Guy's Note）

[[graphics-guy-notes]] 2018 年 7 月的文章，给 GGX / Beckmann / Blinn 三种 NDF 的各向异性版本推出 importance sampling 公式。

## 摘要

作者在 SORT 里加 brushed metal，需要把原先只支持各向同性的 microfacet BRDF 扩展到各向异性。各向异性情况下 $\theta$ 和 $\phi$ 被项 $A(\phi) = \cos^2\phi/\alpha_u^2 + \sin^2\phi/\alpha_v^2$ 耦合，不能分离采样。文章走完「先对 $\theta$ 积 CDF，对极限得 $\phi$ 的 marginal pdf，再从联合 CDF 除出 conditional $\theta$ CDF」全套推导，三个 NDF 均给出闭式 sample 公式——尤其 GGX 结果最干净，Beckmann 的 $\phi$ marginal 意外与 GGX 相同（只 $\theta$ 公式不同），Blinn 用 $B(\phi)$ 代替 $A(\phi)$。另外专门讲了 $\arctan$ 只返回 $(-\pi/2, \pi/2)$ 的坑——要按 $\epsilon$ 分三段加偏移保证 $\phi$ 覆盖 $[0, 2\pi]$。结尾建议转向 VNDF（visible normal sampling）以进一步提升效率。

## 关键要点

- 联合 pdf 先 marginal 后 conditional 是各向异性 importance sampling 的通用套路。
- GGX：$\phi = \arctan(\alpha_v/\alpha_u \tan(2\pi\epsilon))$，$\theta = \arctan\sqrt{\epsilon / ((1-\epsilon)A(\phi))}$。
- Beckmann：同样 marginal pdf，$\theta = \arctan\sqrt{\ln\epsilon / A(\phi)}$。
- Blinn：用 cos 幂形式，$\theta = \arccos(\epsilon^{1/(B(\phi)+2)})$。
- $\arctan$ 值域坑：随机数 $\epsilon \in [0, 0.25] / (0.25, 0.75) / [0.75, 1]$ 三段加 $0 / \pi / 2\pi$ 偏移。
- 更好的 default：VNDF（Heitz 2014）替代 NDF-only sampling，避开半球外样本。

## 链接到的概念

- [[anisotropic-microfacet-sampling]]
- [[microfacet-brdf]]
- [[inversion-sampling-prng]]
- [[bxdf-unit-test]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/sample_anisotropic_microfacet_brdf/
- 本地：`raw/articles/agraphicsguynotes.com/2018-07-18_sampling-anisotropic-microfacet-brdf.md`
