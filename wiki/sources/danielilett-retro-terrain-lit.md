---
tags: [source, unity, urp, shader, 复古, terrain]
date: 2026-04-14
sources: 1
---

# Retro Shaders Pro for URP - Retro Terrain Lit（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Retro Shaders Pro* 资产包的 **Retro Terrain Lit** shader 文档页。表面是一份商业 shader 包的参数说明，但展开来看是一份**复古主机画面复刻技术的清单**——每一个参数都对应 PS1/N64 时代某一条具体硬件限制的模拟手段。

## 摘要

Retro Terrain Lit 是 *Retro Lit* 的 terrain 版本，专为 Unity 的 Terrain 系统设计，会把 Texel Lit 模式下的光照对齐到 `Splat0` 贴图的 texel 网格，因此要求所有 splat 贴图保持一致分辨率。参数分三组：**Color & Texture**（色深量化、分辨率降采样、双线性/point/N64 3-point 采样模式切换、屏幕或纹理空间 dither）、**Vertex Snapping**（object/world/view 三种空间下的顶点量化，以及每米 snap 点数）、**Lighting & Shadow**（Lit / Texel Lit / Vertex Lit / Unlit 四种光照模式、环境光下限、可选 specular 和反射 cubemap）。

## 关键要点

- "色深"参数控制每通道量化级数（PNG 最多 256），配合一个 offset 防止减色后整体变暗——公式是 `floor(col * depth + offset) / depth`。
- 分辨率降采样**向下舍入到 2 的幂次**——填 196 实际会得到 128。这是 texture unit 限制的直接表达。
- N64 filtering mode 还原 Nintendo 64 纹理单元的 **3-point bilinear** 采样（只混 2×2 四样本中的三个），这是一个非常具体的硬件特性。
- Vertex snapping 的三种空间（object/world/view）对应三种完全不同的视觉风格——view space 最贴近 PS1 真实效果但实现最复杂。
- Texel Lit 模式用 terrain 第一张 splatmap 的分辨率作为光照"像素"参照，这是它和非 terrain 版 Retro Lit 的主要差异。

## 链接到的概念

- [[retro-rendering-techniques]]
- [[dither-alpha-clipping]] —— 同一种 dither 数学用在 alpha 通道
- [[sampler-filter-wrap-modes]]
- [[coordinate-spaces]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/retro-terrain-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-retro-terrain-lit.md`
