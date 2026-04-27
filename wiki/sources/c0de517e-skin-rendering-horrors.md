---
tags: [source, 渲染, 皮肤渲染, SSS, 实时渲染]
date: 2026-04-27
sources: 1
---

# The Three Skin Rendering Horrors You Want to Avoid（C0DE517E）

[[angelo-pesce]] 发表于 2011 年 12 月的文章，梳理实时皮肤渲染中三个最常见、最容易被忽视的视觉错误及其廉价修复思路。

## 摘要

Pesce 从 Fight Night Champion 的实践出发，将皮肤渲染失败归纳为三类：**色调错误（Bad Tone）**、**细节错误（Bad Detail）**、**体积感错误（Bad Volume）**。文章强调这三类问题并不需要复杂的离线技术才能改善——理解底层物理原理之后，用极简的 shader hack 就能得到明显提升。文章还附有关于头发、眼睛、牙齿和耳朵的补充部分。

## 关键要点

- **色调（Tone）**：皮肤漫反射颜色主要来自次表面散射，最廉价的 hack 是在 Lambert 之上加一个颜色渐变（ramp），不一定需要精确曲率估算。[[preintegrated-skin-shading|预积分皮肤着色]] 是当时实时 hack 中的首选，但即使简单的 ramp 只要色相正确也能得到合格结果。SSAO 不应直接与皮肤漫反射相乘，应加入微弱的基础色防止出现灰色死区。
- **细节（Detail）**：皮肤细节不来自漫反射，漫反射被 SSS 模糊；细节完全在高光层。漫反射与高光理想上应使用不同法线贴图或以不同 mip 偏移采样；皮肤毛孔作为高光自遮蔽比放入法线贴图效果更好。specular exponent 应随视距增大而展宽（可用 ddx/ddy 估计过滤宽度）。
- **体积（Volume）**：蒙皮后几何法线质量差，需额外处理（参见 [[skinning-normals-weighted-average]]）。环境光不应是常数，哪怕一个简单的半球方向 ramp（天空色 + 地面色）也比纯常数好很多。遮蔽（AO、弯曲法线、屏幕空间遮蔽）对体积感至关重要；每个光照分量都应该有合理的遮蔽。
- **VSM vs PCF**：FNC Champion 发现从 VSM 退回 PCF 反而改善了脸部——VSM 精度问题导致鼻影、眼眶阴影丢失，这些恰好对体积感最关键。
- **高光形状**：Phong 高光圆形过于均匀且缺少菲涅耳；Kelemen/Szirmay-Kalos 模型更适合皮肤但受限于 IBL 管线。实践中用 exponent map 打破均匀高光，用 Schlick 近似的菲涅耳驱动法线偏转或 exponent 下调，而非直接乘高光。

## 链接到的概念

- [[preintegrated-skin-shading]]
- [[skinning-normals-weighted-average]]
- [[microfacet-brdf]]
- [[physically-based-shading]]
- [[hair-shader-anisotropic]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/12/three-skin-rendering-horrors-you-want.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-12-12_the-three-skin-rendering-horrors-you-want-to-avoid.md`
