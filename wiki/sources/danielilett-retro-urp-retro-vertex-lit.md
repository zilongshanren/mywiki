---
tags: [source, unity, urp, shader, 复古, psx, vertex-lit]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for URP - Retro Vertex Lit（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 URP 版 *Retro Shaders Pro* 撰写的 **Retro Vertex Lit** 参数手册——该 shader 在 **Version 1.5** 起功能已合并进 [[sources/danielilett-retro-urp-retro-lit|Retro Lit]]，这页作为旧版本兼容文档保留。

## 摘要

Retro Vertex Lit 是 PS1/N64 风光照里**强制 vertex-only Gouraud shading** 的独立 shader：每个顶点算一次 Lambert，光栅化器线性插值到 fragment——这是 PS1 的硬件现实（没有像素光照）和 N64/PS2 的常见选择（per-vertex 更便宜）。该 shader 的参数几乎是 Retro Lit 的严格子集：*Base Color* / *Base Texture* / *Resolution Limit*（texture 分辨率向下 2 次幂）、*Snaps Per Unit*（view-space 顶点吸附的密度，PS1 定点量化的复现）、*Color Bit Depth* + *Color Bit Depth Offset*（量化 + 防变暗偏移）、*Affine Texture Strength*（0 = perspective-correct、1 = 全 affine warping，PS1 典型的纹理"游泳"伪影）、*Point Filtering*、*Enable Dithering*（这里简化为 bool，而非 Retro Lit 的 Screen / Texture / Off 三档）、*Use Vertex Colors*。缺少 Retro Lit 的 Surface Options、Snapping Mode 四档、光照四档（Lit/Texel/Vertex/Unlit）——因为这里光照模式已被 hardcode 为 vertex-only。

## 关键要点

- v1.5 合并进 Retro Lit：作为兼容页保留，参数是 Retro Lit 的子集
- 强制 **vertex-only Gouraud** 光照，对应 PS1/N64/PS2 历史现实——高光呈菱形而非圆形是典型识别特征
- *Affine Texture Strength* 的连续滑块（0→1）是"可调复古"的典型：开发者可以选全 perspective-correct、全 affine、或两者线性混合
- *Enable Dithering* 简化为 bool——Retro Lit 的 Screen / Texture / Off 三档拆分在 v1.5+ 才引入
- view-space snapping 是最贴近 PS1 真实行为的选择——相对相机坐标量化，远处物体移动时抖动最明显

## 链接到的概念

- [[retro-rendering-techniques]]
- [[color-quantization-retro]]
- [[dither-alpha-clipping]]
- [[coordinate-spaces]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/retro-vertex-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-retro-vertex-lit.md`
