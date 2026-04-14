---
tags: [source, 渲染, pbr, brdf, 微表面, 能量守恒]
date: 2026-04-14
sources: 1
---

# A Multi-Faceted Exploration (Part 2)（Stephen Hill）

[[stephen-hill|Stephen Hill]] 2018 年 6 月的博客长文，*A Multi-Faceted Exploration* 系列的第二篇。承接 Part 1 关于单次散射微表面 BRDF 会丢失能量的分析，这一篇把 Heitz 等 2016 年的 **random-walk 多次散射模型**当作地面真值参考，然后细致审视 Kulla & Conty（Imageworks）在 2017 SIGGRAPH course 上提出的**补偿式** multiscatter lobe，并给出一个关键修正。

## 摘要

标准 [[microfacet-brdf|微表面 BRDF]] 只建模一次散射——microfacet 间的相互反射被当作能量损失直接扔掉。Heitz et al. 2016 的 random walk 模型在 Smith 的 microsurface 假设上做完整的多阶散射模拟，得到的结果在 furnace test 中能量完美守恒，作为参考解。

Imageworks 选了一条便宜得多的路：在单次散射 BRDF $f_{ss}$ 之外叠加一个 Kelemen 型的 $f_{ms}$，让 $f_{ss} + f_{ms} = 1$——具体做法用 $E(\mu)$（去 Fresnel 后的方向-半球反射率）和它的半球平均 $E_{avg}$ 构造。纯反射材质下两种方案视觉几乎看不出差别。

对**有色 conductor**（铜、金），Imageworks 用了一个 multiple-scattering Fresnel $F_{ms} = F_{avg} E_{avg} / (1 - F_{avg}(1 - E_{avg}))$（从 Jakob 2014 的 diffuse multiscatter 模型改造而来）。Hill 发现这个推导**无意中把一次散射也计进了多阶求和**——正确的做法是从 $k=1$ 开始求和，得到 $F_{ms} = F_{avg}^2 E_{avg} / (1 - F_{avg}(1 - E_{avg}))$。这只需把分子上的 $F_{avg}$ 换成 $F_{avg}^2$，结果立即向 Heitz ground truth 靠拢。这个修正后来被合并进 Imageworks 的更新版 slides。

## 关键要点

- **多次散射的两条路**：Heitz random walk（模拟，精确，离线）vs Imageworks 补偿（近似，解析式，实时）。
- **Kelemen lobe 的设计原则**：让补偿项大小恰好等于 $1 - E(\mu_o)$，以保证能量完全守恒。
- **$F_{ms}$ 推导 bug**：原公式用几何级数 $\sum_{k=0}$ 把一次散射也算进来了；应该从 $k=1$ 开始。
- **修正后的 $F_{ms}$**：$F_{avg}^2 E_{avg} / (1 - F_{avg}(1 - E_{avg}))$——一个字符的差别但结果可见地更准。
- **工程启示**：PBR 的「看起来一致」背后有大量细节需要推导检查；Hill 本人承认 bug 源自自己之前的 slide 误编辑。

## 链接到的概念

- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[stephen-hill]]

## 原文

- 链接：https://blog.selfshadow.com/2018/06/04/multi-faceted-part-2/
- 本地：`raw/articles/blog.selfshadow.com/2018-06-04_a-multi-faceted-exploration-part-2.md`
