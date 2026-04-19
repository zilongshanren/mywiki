---
tags: [source, unity, urp, shader, fresnel, iridescent, bubble]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Bubble（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Bubble** 参数手册——基于 Fresnel + color ramp + 折射的彩虹肥皂泡材质。

## 摘要

Bubble 在 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 的 Surface Options + Lit Properties 基础上加一段 Bubble Properties：*Color Ramp Texture* 是一张 1D 彩虹渐变，沿 Fresnel 值查色得到"薄膜干涉"的近似色——而非真实薄膜干涉（真物理需要波长级采样）；*Fresnel Power* 控 rim 曲线陡峭度；*Fresnel Noise Strength* + *Fresnel Noise Scale* 把噪声偏移叠到 ramp 查表的 U 坐标上，让彩虹色破开成斑块而非纯净渐变；*Iridescent Strength* 是 ramp 贡献的混合权重；*Iridescent Flow Direction* 是世界空间 2D 向量，让 ramp 查色随时间沿此方向滚动——模拟"彩虹流过肥皂泡表面"。*Refractive Index* 控屏幕 UV 扰动强度；*Camera Texture Mode* 是关键 toggle——在 `_CameraOpaqueTexture`（默认，URP 内置）与 Shader Toolbox 提供的自定义 `_CameraTransparentTexture` 之间切换，后者让透明泡泡之间互相折射。*Use Emission* 决定 Fresnel 彩虹层走 Emission 还是 Base Color 输出槽。

## 关键要点

- Fresnel 值作为 color ramp 的 U 坐标——是 [[iridescent-bubble-shader|thin-film 彩虹]]的廉价近似，不做波长级物理
- **noise offset + flow direction** 让彩虹色动起来是这个 shader 的主要风味参数——没有这两个的话彩虹像贴花
- `_CameraTransparentTexture` 是 Shader Toolbox pack 层面的渲染特性——单个 shader 无法实现，必须 render feature 配合；解决 URP 默认 `_CameraOpaqueTexture` 的透明物体互相看不见的缺陷
- *Use Emission* toggle + HDR 颜色 + Bloom = 发光彩虹泡；关掉则彩虹色受场景光照调制
- *Iridescent Flow Direction* 用**世界空间**而非 object space：泡泡旋转时彩虹不应随之旋转——这与薄膜厚度受空气流动决定的物理直觉一致

## 链接到的概念

- [[iridescent-bubble-shader]]
- [[fresnel-edge-highlight]]
- [[refractive-glass-shader]]
- [[unity-grabpass-blur]]
- [[color-lut]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/bubble/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-bubble.md`
