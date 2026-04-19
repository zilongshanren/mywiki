---
tags: [source, unity, urp, shader, 复古, psx, retro-lit]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for URP - Retro Lit（Daniel Ilett）

[[daniel-ilett]] 为 URP 版 *Retro Shaders Pro* 撰写的 **Retro Lit** 参数手册——复古 pack 的核心 shader 的 URP 通用版本（非 terrain 专用）。

## 摘要

相比 [[sources/danielilett-retro-terrain-lit|Retro Terrain Lit]]，通用 Retro Lit 多了一整组 **Surface Options**（Opaque/Transparent、Front/Back/Both、Alpha Clip + 阈值），这是非 terrain shader 必须自己处理的基础表面控制。颜色纹理段的 *Color Bit Depth / Offset / Resolution Limit / Affine Strength / Filtering Mode (Bilinear/Point/N64)* 与 terrain 版一致；Dithering 提供 Screen / Texture / Off 三模式。Vertex Snapping 相比 Godot 版暴露四种 *Snapping Mode*（Object / World / View / Off），对应三种完全不同的抖动风格——view space 最贴近 PS1。光照段是和 terrain 版最大的共同点：*Lit / Texel Lit / Vertex Lit / Unlit* 四档，并加上 *Use Flat Shading*（整三角面着色）、*Receive Shadows*、*Ambient Light Override + Strength*（黑影下限）、*Use Specular Lighting + Glossiness*（PS1 本来没有，是现代人"可选复古"的开放项）、*Use Reflection Cubemap + Cubemap Rotation*（绕 y 轴旋转 cubemap）。整体是一份比 terrain 版更通用、比 Godot 版更完整的 PSX-look 参数矩阵。

## 关键要点

- 通用 Retro Lit 在 terrain 版基础上加了 Surface Options（Opaque/Transparent、双面渲染、Alpha Clip）——terrain 着色器不需要这些因为 terrain 总是不透明单面
- *Use Flat Shading* 是 terrain 版没有的选项——把三角面着成完全平面（无 Gouraud 插值），模拟 PS1 低多边形雕塑感
- Specular 高光 + Reflection Cubemap 是"可选复古"——真实 PSX/N64 不做这些，但允许现代开发者在复古美学之上点缀一些
- Cubemap 的 Y 轴旋转参数让场景调色师能把反射对齐到特定朝向而不必重新烘焙 cubemap
- 光照四模式 (Lit / Texel Lit / Vertex Lit / Unlit) 与 terrain 版一致，其中 Vertex Lit 对应 N64/PS2 Gouraud 光照

## 链接到的概念

- [[retro-rendering-techniques]]
- [[color-quantization-retro]]
- [[dither-alpha-clipping]]
- [[sampler-filter-wrap-modes]]
- [[parallax-corrected-cubemap]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/retro-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-retro-lit.md`
