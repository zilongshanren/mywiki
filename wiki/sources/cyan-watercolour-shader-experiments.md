---
tags: [source, shader, shadergraph, urp, 风格化, 后处理]
date: 2026-04-14
sources: 1
---

# Watercolour Shader Experiments（Cyan）

[[cyanilux|Cyan]] 2020 年 10 月发表的 shader breakdown，记录他为 [[harry-alisavakis|Harry Alisavakis]] 主办的 `#TechnicallyAChallenge` 「水彩」主题做的一组 URP shader。源码托管在 [`URP_WatercolourShaders`](https://github.com/Cyanilux/URP_WatercolourShaders)。

## 摘要

整套效果由**三层 shader** 协同：

1. **Object Shader**：mesh 材质。Unlit Master + 自定义 Lambert（`saturate(dot(N, L)) + 0.7` 再 saturate 让暗面提亮）；Triplanar 节点采样噪声纹理避开 UV 接缝；最关键是「**水彩阴影**」——把 Shadow Attenuation 经过 `OneMinus → 0.5` 当 Lerp.B、`Step(Atten, 0.95)` 当 Lerp.T、Lerp.A = 1，得到「shadow 边缘暗、shadow 中心淡」的水彩湿笔触观感。阴影位置先用 World Position 噪声扰动，但为了避免 offset 把阴影推进 mesh，用 C# 把主光旋转矩阵作为 `_WorldToMainLightMatrix` 全局属性传给 shader，offset 量乘以这个矩阵——只沿光源方向扰动。
2. **Image Effect Shader**：通过 [[blit-render-feature|Blit Render Feature]] 跑全屏。三件事：Simple Noise（scale ≈ 200）轻微 UV 扭曲；**Roberts Cross 边缘检测**（4 次对角 Scene Depth 采样）做描边；从扭曲坐标算到 `(0.5,0.5)` 的距离 + Smoothstep 做白色 vignette 模拟纸面留白。
3. **Decal Shader**：transparent cube + Scene Depth。从 `Screen Position(Raw).w` 拿 fragment 深度，`View Direction / fragmentDepth * Scene Depth` 重建世界坐标（[[scene-color-depth-nodes|Scene Color & Depth]] 文里的同一个 trick），再 Transform 到 object space 当 UV 采样噪声。Length 出距离场后 `DDXY/fwidth` 做 anti-aliased 边缘 mask——这是经典「从距离场拿到清晰像素边」的标准技巧。

## 关键要点

- 风格化 shader 通常是「多层 shader 协同」而不是一个超级 shader 包打天下：Object（光照 + 表面噪声 + 阴影暗边） + Post（描边 + vignette + 扭曲） + Decal（斑点）。
- 水彩阴影的边缘加深 = `Lerp(1, 0.5, Step(ShadowAtten, 0.95))`——硬切让 shadow 边缘有一道浅色环，中心反而暗。
- 通过 C# 传 `_WorldToMainLightMatrix` 全局矩阵，让阴影 offset 只沿光源方向扰动，避免穿透 mesh。
- Roberts Cross 边缘检测只采 4 次（vs Sobel 的 9 次），对斜边敏感——风格化描边足够。
- Decal 用 cube + 从 Scene Depth 重建世界位置 + Transform 到 Object space 的「假 decal」实现，限制是相机不能进 cube。
- URP 的 `View Direction` 节点不归一化，正好用于 `/depth` 反推；HDRP 它是归一化的，必须换成 `Camera Position - Absolute World Position`。

## 链接到的概念

- [[watercolour-shader-experiments]]
- [[blit-render-feature]]
- [[triplanar-mapping]]
- [[scene-color-depth-nodes]]
- [[diffuse-lighting-lambertian]]
- [[harry-alisavakis]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/10/06/watercolour-shader-experiments/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-10-06_watercolour-shader-experiments.md`
