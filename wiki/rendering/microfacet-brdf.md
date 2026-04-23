---
tags: [渲染, pbr, brdf, 微表面, 能量守恒]
date: 2026-04-14
sources: 2
---

# 微表面 BRDF（Microfacet BRDF）

**微表面 BRDF** 是当代 [[physically-based-shading|物理基础渲染]]（PBR）的通用材质模型。它把一小块表面看成无数朝向各异的理想镜面小面（microfacet），用一个**法线分布函数** $D$、一个**遮蔽 / 阴影项** $G$、一个**菲涅耳项** $F$ 组成镜面反射 BRDF：

$$f_r = \frac{D\,F\,G}{4\,(n\cdot l)\,(n\cdot v)}$$

实时渲染里几乎所有金属 / 塑料 / 漆面都从这个骨架出发——只是 $D$、$G$、$F$ 的具体选型不同。

## 三个项分别在干什么

- **$D$（NDF, normal distribution function）**：给定宏观法线 $n$，有多少比例的 microfacet 法线指向半程向量 $h$。GGX/Trowbridge-Reitz 因为长尾、高光边缘平滑，是目前最常见的选择。
- **$G$（geometry / shadowing-masking term）**：考虑入射和出射方向被相邻 microfacet 遮挡（masking = 出射被挡，shadowing = 入射被挡）的几何概率。目前的事实标准是 **Smith 模型**——假设 microfacet 高度之间统计独立，推出 masking 和 shadowing 的解析近似，配合 GGX 给出非常接近暴力模拟参考的结果（Heitz 2014 在 JCGT 上证明了这一点）。
- **$F$（Fresnel term）**：表面反射率随入射角变化的 Schlick 近似 $F_0 + (1-F_0)(1-n\cdot l)^5$ 最常用。

## 单次散射 vs 多次散射

标准微表面 BRDF 有一个常被忽视的重大简化：**它只模拟一次散射**——光打到一个 microfacet、反射一次、就离开。相邻 microfacet 之间的「再次反射」被 $G$ 当作能量损失直接吞掉了。这和「直接光照 vs 全局光照」的关系是同构的：单次散射 = 微表面的「直接光照」，多次散射 = 微表面的「GI」。

这个近似在光滑表面几乎没影响，但在粗糙金属和白色材质上会表现为**能量大量流失**：在均匀光照下（furnace test），粗糙的白色球看起来发灰而不是纯白。随着 roughness 趋近 1，丢失的能量可以超过总入射能量的一半。

两种补救思路：

- **模拟派**：Heitz et al. 2016 把 Smith 模型推广为 **random walk**，在 microsurface 高度场上随机游走至光线离开，所有散射阶自然收敛到正确解。这是离线渲染里的地面真值参考。
- **补偿派**：Imageworks（Kulla & Conty 2017 的 SIGGRAPH course）在单次散射 BRDF 上额外加一个 **Kelemen 型 lobe** $f_{ms}$，大小设计成恰好补回单次散射丢失的那部分能量 $1 - E(\mu_o)$，得到 $f_{ss} + f_{ms} = 1$ 的能量守恒。[[stephen-hill|Stephen Hill]] 的「A Multi-Faceted Exploration」系列博客对这个补偿项做了详细剖析，并在 $\Fms$ 的推导中发现 Imageworks 版本意外地把「一次散射」也算进了多次散射求和；修正后（把 numerator 从 $\Favg$ 改成 $\Favg^2$）能让着色结果明显靠近 Heitz 参考。

两派的取舍：模拟派更准、离线渲染友好；补偿派是纯解析式，不需要 random walk，几乎零额外成本，适合游戏实时渲染。

## 对着色管线的影响

这也解释了为什么游戏引擎在 2017 年前后开始补「multiscatter」这一项——白色粗糙塑料终于能在 furnace test 里守恒，环境光反射看起来不再发灰。Frostbite、Unreal、Filament 等都实现了类似的补偿。

## 相关
- [[spectral-brdf]] — 把 base-color + 纯白两权重扩展到整段可见光谱
- [[spherical-harmonics]] — 环境光积分的另一种常用展开
- [[stephen-hill]]
- [[journey-sand-specular]] — Blinn-Phong 作为 NDF 起点的风格化使用
- [[normalised-blinn-phong-shader]] —— 归一化 Blinn-Phong 作为 microfacet BRDF 教学起点，演示能量守恒 / Fresnel / gloss 线性化
- [[anisotropic-microfacet-sampling]] — GGX/Beckmann/Blinn 各向异性 importance sampling 推导
- [[bxdf-unit-test]] — PBRT 的 bsdftest 用 2π 收敛作为 BXDF 正确性检验
- [[importance-sampling-pdf-cancellation]] — GGX IS 代码里没有 D 项没有 weight 的代数根因

## Sources
- [[sources/selfshadow-multi-faceted-part-2]]
- [[sources/selfshadow-pbs-siggraph-2014]]
- [[sources/graphics-guy-anisotropic-microfacet-sampling]]
