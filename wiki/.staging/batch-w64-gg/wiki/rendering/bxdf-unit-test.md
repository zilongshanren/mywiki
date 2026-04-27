---
tags: [渲染, 测试, brdf, bxdf, pbrt, 验证]
date: 2026-04-19
sources: 1
---

# BXDF 单元测试（PBRT 的 bsdftest）

离线渲染器调 BDPT 的痛，一半来自 BXDF 的小 bug——sample 与 pdf 不一致、能量不守恒、遮蔽下采样到半球外。直到 [[Jiayin Cao]] 花很久才定位出一个 BXDF bug 导致 BDPT 和 path tracing 分叉。教训：**BXDF 在接入 integrator 之前就要有单元测试**。PBRT 自带 `bsdftest`，这页解释它怎么工作，以及为什么每格都必须收敛到 $2\pi$。

## 一个 BXDF 需要满足什么

1. **Evaluate**：给定 $\omega_i, \omega_o$，返回 BRDF 值。
2. **Sample**：给定 $\omega_i$ 与某个 pdf，采样 $\omega_o$。
3. **Pdf**：给定 $\omega_i, \omega_o$，返回**同一个** pdf。第三点必须和第二点严格自洽——否则 path tracing 直接引入偏差（分母和 sample 分布不一致）。
4. **Pdf 与 BRDF 形状相近**：这不是正确性要求，而是 importance sampling 效率。

## 为什么每格要收敛到 2π

`bsdftest` 把上半球划成 10×10 个 sub-domain。**关键点**：$\phi$ 均匀切分，但 $\theta$ 切分的是 $\cos\theta$ 均匀而不是 $\theta$ 均匀。这样每格的立体角都恰好是 $2\pi/100$：

$$\int_{\Omega_{ij}} d\omega = \int_{2\pi i/10}^{2\pi(i+1)/10}d\phi \int_{\arccos((j+1)/10)}^{\arccos(j/10)} \sin\theta\, d\theta\, = \frac{2\pi}{100}$$

用 Monte Carlo 估计 $\int_\Omega d\omega$，估计量是 $\frac{1}{N}\sum \frac{1}{p(\omega_i)}$。真值是 $2\pi$（上半球面积），所以：

- **每格**样本乘以 100 后应该 → $2\pi$；
- **整张** histogram 平均 → $2\pi$。

取 1000 万样本后仍不收敛 → bug。

## 典型能查出的 bug

- **sample 函数根本没按 pdf 分布**（pdf 是 cos-weighted，sample 却是均匀）；
- **pdf 函数算错**，给 evaluate 返回的值和 sample 时用的不一致；
- **数值垃圾**（NaN radiance、负 pdf）被统计为 bad sample；
- **采到半球外**的 outside sample 数：数量多说明 importance sampling 效率差但不是 bug。

## 不能查出的

`bsdftest` **不测 BRDF 本身的物理正确性**，也不测 importance sampling 与 BRDF 形状是否匹配。形状匹配度要用 furnace test / chi-square test 之类的补充手段。

## 教训

BXDF 是 rendering 里最容易隐藏 silent bias 的地方。**在 BXDF 加进 integrator 之前先跑 bsdftest**——比在 BDPT 里追几天的 bug 便宜得多。

## 相关

- [[microfacet-brdf]]
- [[anisotropic-microfacet-sampling]]
- [[inversion-sampling-prng]]
- [[monte-carlo-integration]]
- [[path-tracing-basics]]
- [[graphics-guy-notes]]

## Sources

- [[sources/graphics-guy-pbrt-bxdf-verify]]
