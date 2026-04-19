---
tags: [人物, 作者, 渲染, pbr]
date: 2026-04-14
sources: 6
---

# Stephen Hill（Selfshadow）

**Stephen Hill**，博客 [blog.selfshadow.com](https://blog.selfshadow.com/) 的作者，业界常用 ID 「Selfshadow」。长期在游戏主机 AAA 项目里做渲染工程师——**Splinter Cell: Conviction**（Ubisoft Montreal）的可见性系统是他和 Daniel Collin 合作的代表作——后来加入了 **Lucasfilm / ILMxLAB**（工业光魔），跨到 VFX / 实时混合制作的前沿。

他在社区里的主要影响力来自两块：

## 1. SIGGRAPH「Physically Based Shading in Theory and Practice」course 的长期组织者

从 2010 年起每年一届，是 **[[physically-based-shading|PBR]]** 这条技术线最权威的年度论坛。Brent Burley 的 *Physically Based Shading at Disney*（2012）、Sébastien Lagarde 的 *Moving Frostbite to PBR*（2014）、Eric Heitz 的 masking-shadowing 函数统一（2014）、Kulla & Conty 的 Imageworks multiscatter（2017）都首发在这里。Hill 本人会在博客上补充技术博文为这些 course note 做勘误和延伸。

最有代表性的是 **「A Multi-Faceted Exploration」** 系列：详细拆解了 Imageworks 的多次散射补偿 lobe，发现公式里无意中把单次散射也计入了求和，修正后让补偿方法更接近 Heitz random-walk ground truth。他还公开承认这一 bug 来自自己早先 slide 的误编辑——对着错误修正的坦率是这类技术博客的少见品质。

## 2. *Blending in Detail*（与 Colin Barré-Brisebois 合著）

2012 年的短文，系统对比了法线贴图混合的各种方法（Linear / Overlay / PD / Whiteout / UDN / Unity 基底版），提出了几何上干净、GPU 友好的 **[[normal-map-blending|Reoriented Normal Mapping]]**。3 行 HLSL、8 条 SM3.0 指令，现在是「细节法线叠加基础法线」的事实标准实现。

## 3. *Practical, Dynamic Visibility for Games*（与 Daniel Collin）

2011 年的深度文章，把 Conviction 的 GPU [[hierarchical-z-buffer|HZB]] 方案和 DICE Frostbite 的 SPU 软件光栅方案并列呈现——两种完全不同硬件哲学的 [[occlusion-culling|遮挡剔除]] 方案在同一篇文里对照。是看「真实游戏引擎怎么处理动态 visibility」的最佳入门材料。

## 风格

- **深度推导 + 坦率勘误**：每次涉及数学公式的博文都会给完整推导，发现错误后明示更正。
- **不教条**：同一个问题给多种方案对比（OQ vs HZB vs 软光栅、Linear vs RNM），让读者看清取舍。
- **连接学术和工业**：他是把 Heitz、Dupuy、Jakob 这些 JCGT / Eurographics 论文和实际游戏产品之间做翻译的枢纽。

## 相关

- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[normal-map-blending]]
- [[occlusion-culling]]
- [[hierarchical-z-buffer]]

## Sources
- [[sources/selfshadow-multi-faceted-part-2]]
- [[sources/selfshadow-blending-in-detail]]
- [[sources/selfshadow-pbs-siggraph-2014]]
- [[sources/selfshadow-practical-visibility]]
- [[sources/selfshadow-pbs-siggraph-2012]]
- [[sources/selfshadow-pbs-siggraph-2025]]
