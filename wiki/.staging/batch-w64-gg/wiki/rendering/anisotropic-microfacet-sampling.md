---
tags: [渲染, pbr, brdf, 微表面, importance-sampling, ggx, beckmann, blinn]
date: 2026-04-19
sources: 1
---

# 各向异性微表面 BRDF 重要性采样

[[microfacet-brdf]] 的 isotropic 版本很多教程都有，但**各向异性**版本的 importance sampling 要难一个台阶——$\theta$ 和 $\phi$ 不再独立。[[Jiayin Cao]] 在 SORT 里加 brushed metal 时推了 GGX / Beckmann / Blinn 三种 NDF 的各向异性采样公式，这页摘录核心做法。

## 为什么变复杂

各向异性 NDF 里出现的项
$$A(\phi) = \frac{\cos^2\phi}{\alpha_u^2} + \frac{\sin^2\phi}{\alpha_v^2}$$
把 $\theta$ 和 $\phi$ 耦合在一起。联合 pdf $p(\theta, \phi)$ 不能简单分离，必须走「先对 $\theta$ 积出 **marginal** $p_\phi(\phi)$，再用 **conditional** $p_\theta(\theta \mid \phi)$ 采 $\theta$」两步法。

## 三个 NDF 的统一套路

**步骤**：
1. 写出 $D(h)$，定义匹配的 pdf（乘上 $\sin\theta$ 转立体角到球面）。
2. 对 $\theta$ 积分得到 $P_\theta(\theta, \phi)$。
3. 令 $\theta \to \pi/2$ 得 marginal $p_\phi(\phi)$。
4. 积 $p_\phi$ 得 $P_\phi$，inversion sampling 得 $\phi$。
5. conditional CDF $P_\theta / p_\phi$ 求逆得 $\theta$。

**GGX**（结果最干净）：
$$\phi = \arctan\!\Big(\tfrac{\alpha_v}{\alpha_u}\tan(2\pi\epsilon)\Big),\quad \theta = \arctan\!\sqrt{\tfrac{\epsilon}{(1-\epsilon)A(\phi)}}$$

**Beckmann**（指数形式，要用 $e^{A - A/\cos^2\theta}$ 技巧凑积分）：
$$\theta = \arctan\!\sqrt{\tfrac{\ln\epsilon}{A(\phi)}}$$

惊喜：Beckmann 和 GGX 的 **marginal $p_\phi$ 是一样的**——$\phi$ 公式可以复用，只有 $\theta$ 不同。

**Blinn**（用 $B(\phi) = \cos^2\phi\, e_u + \sin^2\phi\, e_v$ 替代 $A$）：
$$\phi = \arctan\!\Big(\sqrt{\tfrac{e_u+2}{e_v+2}}\tan(2\pi\epsilon)\Big),\quad \theta = \arccos\!\Big(\epsilon^{1/(B(\phi)+2)}\Big)$$

## arctan 的区间陷阱

$\arctan$ 只返回 $(-\pi/2, \pi/2)$，但 $\phi$ 需要覆盖 $[0, 2\pi]$。Cao 的做法是把随机数 $\epsilon$ 分三段分别加偏移 $0 / \pi / 2\pi$，在 $\epsilon = 0.25$ 和 $\epsilon = 0.75$ 两处做连续拼接。这是每个实现这套公式的人都会掉一次的坑。

## 工程建议

**visible normal sampling**（Heitz 2014 / Wenzel）是比 NDF-only sampling 更好的默认——特别是掠射角下 NDF 采样会大量产生半球外样本，visible normal sampling 天然避开。Cao 在博客末尾也推荐转到 VNDF。

## 相关

- [[microfacet-brdf]]
- [[bxdf-unit-test]]
- [[inversion-sampling-prng]]
- [[spherical-integration]]
- [[physically-based-shading]]
- [[graphics-guy-notes]]

## Sources

- [[sources/graphics-guy-anisotropic-microfacet-sampling]]
