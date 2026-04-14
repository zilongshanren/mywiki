---
tags: [source, rendering, shader, 高光, fresnel, blinn-phong, 风格化]
date: 2026-04-14
sources: 1
---

# Journey Sand Shader: Specular Reflection（Alan Zucconi）

[[alan-zucconi|Alan Zucconi]] 2019 年 10 月的文章，Journey Sand Shader 系列的第四篇，拆解 thatgamecompany《Journey》沙丘的两路主要镜面反射——**rim lighting** 和 **ocean specular**。

## 摘要

Journey 的沙丘有一种"像水一样流动"的高光，Lead Engineer John Edwards 明确说过团队想把沙当成流体来渲染。作者把 Journey 的高光拆成三条：rim lighting（轮廓 Fresnel 型）、ocean specular（大光斑 Blinn-Phong）、glitter reflection（闪点）。本文讲前两条。Rim lighting 用 $(1 - N \cdot V)^p \cdot s$——廉价 Fresnel 形式，专门解决"远处 dune 被单调色彩糊成一片"的问题，让每条山脊都有一圈轮廓光。Ocean specular 用经典 **Blinn-Phong** $(N \cdot H)^p \cdot s$，$H = \langle V+L \rangle$ 是半程向量，给相机正对太阳方向时拉出一条长条状镜面反射——和日落时湖面的视觉完全同构。两路合成时取 `max` 而非相加，避免同时 rim + ocean 爆白。整套做法是风格化渲染的普适范式：把材质拆成若干条解析项、每条用廉价模型独立调，不追求物理自洽但可控性强。

## 关键要点

- Journey 的沙被刻意渲染成"类流体"——三路 specular 分工
- Rim lighting：$(1 - N\cdot V)^p \cdot s$ 廉价 Fresnel，解决远景色彩糊化
- Ocean specular：Blinn-Phong $(N\cdot H)^p \cdot s$，$H = \langle V+L\rangle$ 是半程向量
- Blinn 1977 把 Phong 1973 的 $R\cdot V$ 换成 $N\cdot H$，更便宜更稳，是现代 NDF 的起点
- 两路高光取 `max` 合成，艺术选择优先于能量守恒
- Part 5 是 glitter reflection（闪点），难点是时域稳定 + 能量守恒
- 和纯 PBR 相反的思路：多条解析项各调参，而非统一 albedo/roughness/metallic

## 链接到的概念

- [[journey-sand-specular]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[shader-vector-math-primer]]

## 原文

- 链接：<https://www.alanzucconi.com/2019/10/08/journey-sand-shader-4/>
- 本地：`raw/articles/alanzucconi.com/2019-10-08_journey-sand-shader-specular-reflection-alan-zucconi.md`
