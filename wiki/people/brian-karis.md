---
tags: [人物, 作者, 渲染, unreal, ue5]
date: 2026-04-14
sources: 3
---

# Brian Karis

**Brian Karis** 是当代实时渲染领域最具影响力的图形工程师之一。博客 [Graphic Rants](http://graphicrants.blogspot.com/) 的作者。早年在 **Human Head Studios**（Prey 2 首席渲染工程师），2012 年后加入 **Epic Games**，最终成为 Unreal Engine 5 的 **[[nanite|Nanite]]** 虚拟化几何系统和 **[[lumen|Lumen]]** 动态全局光照系统的技术负责人。他的 2013 年 SIGGRAPH 讲稿 *Real Shading in Unreal Engine 4* 是游戏业 [[physically-based-shading|PBR]] 事实上的实践起点——GGX + Schlick Fresnel + split-sum IBL 近似，至今仍是几乎所有商业引擎 PBR 管线的骨架。

## Prey 2 时代的博客（2010-2012）

Graphic Rants 的几篇早期博文以「半成品想法」（rants）形式公开讨论了他正在 Human Head 为 Prey 2 做的渲染研究，也超越具体项目地预告了 next gen 渲染的若干方向：

- **[[virtualized-volume-textures]]**（2011-01）：把 2D 虚拟纹理和稀疏体素八叉树（SVO）的思路拓展到体积纹理上——irradiance volume 用索引贴图做页表、按屏幕反馈加载 brick，回避空间浪费。
- **[[tiled-light-culling]]**（2012-04）：在 tiled deferred / tiled forward 的光照剔除基础上，提出**把光源的 specular 反射方向和光泽度一起参与剔除**——利用能量守恒特性，用 specular cone 做额外剔除。
- **[[sparse-shadows-cone-tracing]]**（2012-05）：next gen 渲染需要**多套几何表示**（栅格化的 mesh + trace 友好的 SDF/SVO/surfel/ adaptive depth），diffuse 用传统 shadow map、超出 shadow map 半径的 specular 靠反射向量的 cone trace 解决——这正是后来 [[lumen|Lumen]] 的架构雏形。

2013 年的 *Real Shading in Unreal Engine 4* 正是在这些早期探索上长出来的工程成果——他在 Prey 2 上推进的分块光照 + 物理化光源落地到 UE4 的 deferred 管线里。

## UE5 Nanite / Lumen（2021-至今）

Nanite 解决了「把几亿三角形的艺术资产原封不动塞进引擎」这一长期梦想，核心是 cluster-based LOD + [[visibility-buffer]] + software rasterization for small triangles。Lumen 是相应的动态全局光照系统，架构上正好对应他 2012 年博客里提出的**多套几何表示 + cone trace**的构想：静态场景用 SDF 做远场 cone trace、屏幕空间做近场、surface cache 做着色缓存。

他经常在 Twitter 上和业界同行讨论渲染细节，对新人友好，承认自己的失败实验（见 RGBD post 的坦率自嘲——整篇被他亲手划掉并称之为「hogwash」）。

## 风格

- **Rants 而非 tutorials**：博客多是半成品想法、邀请同行讨论的 open sketch——正好是 [[angelo-pesce]] 同时代的博客文化。
- **从物理出发倒推工程**：从 inverse-square 光衰减、能量守恒、BRDF 归一化这些基本公式出发，推导出剔除、culling、IBL 近似等工程决策。
- **架构连贯**：2010-2012 的博客想法和 2021 的 UE5 Nanite/Lumen 有直接血脉关系——他坚持了十年。

## 相关

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[deferred-rendering]]
- [[visibility-buffer]]
- [[tiled-light-culling]]
- [[sparse-shadows-cone-tracing]]
- [[virtualized-volume-textures]]

## Sources

- [[sources/karis-virtualized-volume-textures]]
- [[sources/karis-tiled-light-culling]]
- [[sources/karis-sparse-shadows-tracing]]
