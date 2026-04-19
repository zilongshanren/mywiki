---
tags: [source, unity, urp, shader, glass, fresnel, 折射]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Glass（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Glass** 参数手册——基于 `_CameraOpaqueTexture` 折射 + Fresnel 边缘的透明玻璃材质。

## 摘要

Glass 在 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 的表面基础上加一段 Glass Properties：*Refractive Index* 控制屏幕 UV 按法线方向的扰动强度（名字是物理量，但 shader 里只是线性系数，不做 Snell `sin` 解算）；*Glass Strength* 是折射采样结果与 base color 的混合权重——0 时只看背景、1 时只看玻璃本身色彩；*Fresnel Power* + *Fresnel Color* 做掠射角边缘高光，和 [[fresnel-edge-highlight|Fresnel Highlight]] 同源；*Use Emission* 决定 Fresnel 贡献走 Emission 还是 Base Color 输出槽；*Camera Texture Mode* 在默认的 `_CameraOpaqueTexture`（URP 内置的不透明队列帧拷贝）与 Shader Toolbox 额外提供的 `_CameraTransparentTexture`（含透明物体的完整拷贝）之间切换——后者解决两片玻璃前后叠放时"后一片不通过前一片折射进来"的 URP 默认缺陷。这个 shader 是 [[iridescent-bubble-shader|Bubble]] 的"无彩虹 ramp"版本，两者共享折射骨架。

## 关键要点

- URP 的 `_CameraOpaqueTexture` 是内建管线 [[unity-grabpass-blur|GrabPass]] 的替代——一次拷贝覆盖所有透明物体，成本 O(1) 而非 O(N)
- 折射走"法线 xy 作为 UV offset"的 shader-art 近似，不做真实 Snell 解算——90% 游戏场景视觉上够用
- *Camera Texture Mode* 的两档折射本质上在问"需要透明物体互相折射吗"——一般不需要选默认，透明嵌套场景选 transparent
- **不含 blur**——这是清澈玻璃而非毛玻璃；要做毛玻璃需要在 camera texture 上再叠一层 blur（Ronja / Linden Reid 的 foggy window 做法）
- 和 [[sources/danielilett-toolbox-urp-bubble|Bubble shader]] 是同族——差别在 Bubble 多了 color ramp + iridescent flow

## 链接到的概念

- [[refractive-glass-shader]]
- [[iridescent-bubble-shader]]
- [[fresnel-edge-highlight]]
- [[unity-grabpass-blur]]
- [[chromatic-aberration-post]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/glass/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-glass.md`
