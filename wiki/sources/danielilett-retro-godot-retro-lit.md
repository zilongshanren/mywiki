---
tags: [source, godot, shader, 复古, psx, retro-lit]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for Godot - Retro Lit（Daniel Ilett）

[[daniel-ilett]] 为 Godot 版 *Retro Shaders Pro* 撰写的 **Retro Lit** 参数手册——这是整个包的核心 shader，把 PSX 风格的复古渲染套到普通 mesh 上。

## 摘要

Godot 版 Retro Lit 的参数组构比 URP 的 Terrain 版精简一层：合并为单一的 Retro Properties 段落，参数包括 *Base Color / Base Texture*、*Resolution Limit*（向下取最接近的 2 的幂次）、*Snaps Per Meter*（顶点吸附，在 view space 下相对相机量化）、*Color Depth* + *Color Depth Offset*（每通道量化级数 + 补偿偏移）、*Affine Strength*（0 = 透视正确、1 = 完全仿射贴图映射）、*Filtering Mode*（Bilinear / Point / N64 3-point）。光照只提供三种模式——*Standard Lit*（逐像素）、*Texel Lit*（光照吸附到贴图 texel）、*Unlit*——相比 URP 版缺了 *Vertex Lit*、specular、reflection cubemap、ambient override 等高级项。Dithering 通过单一布尔 *Use Dithering* 开关（Bayer 矩阵），而 URP 版细化为 Screen / Texture / Off 三模式。整体看 Godot 版是这套 PSX 复刻技术的**最小可用集合**，把 [[retro-rendering-techniques]] 的四个支柱（vertex snap / color quantization / affine UV / N64 filtering）都收齐，但省去了 URP 版扩展的 lighting-model 矩阵。

## 关键要点

- Retro Lit 是整个 pack 的核心 shader，把 PSX 风格套在普通 mesh 上，是 [[retro-rendering-techniques]] 技术的一站式暴露面
- Godot 版顶点吸附默认使用 view space——最接近 PS1 真实硬件表现，不给多空间选项
- 光照只有 Standard / Texel / Unlit 三档——比 URP 版少 Vertex Lit 和 cubemap 反射
- *Affine Strength* 作为连续参数暴露仿射贴图扭曲，0~1 之间线性可调——不是简单的开关
- Dithering 用 Bayer 矩阵在色阶之间"混色"，只有一个开关，比 URP 版的 Screen/Texture 双模式简单

## 链接到的概念

- [[retro-rendering-techniques]]
- [[color-quantization-retro]]
- [[dither-alpha-clipping]]
- [[sampler-filter-wrap-modes]]

## 原文

- 链接：https://danielilett.com/retro-shaders-godot/retro-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-godot-retro-lit.md`
