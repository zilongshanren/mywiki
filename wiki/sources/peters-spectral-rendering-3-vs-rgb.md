---
tags: [source, 渲染, 光谱, rgb, 颜色科学, 路径追踪]
date: 2026-04-19
sources: 1
---

# Spectral rendering, part 3: Spectral vs. RGB（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2025 年 11 月光谱渲染三部曲的收官篇——实证对比 RGB 和光谱渲染在不同光源下的颜色再现差别。

## 摘要

在同一个 path tracer（有 spectral 分支）里切换 RGB vs 光谱模式，同一场景（气球 + 地毯）在多种光源下渲染对比。**Illuminant E**（常数谱）：几乎完全一致，因为 Fourier sRGB lookup table 本就用常数谱训练。**Illuminant D65**：可见但轻微的红色区偏差。**Warm-white LED**：红绿小偏移、可见但不戏剧。**白炽灯**：光谱渲染下蓝色表面**去饱和**——RGB 渲染做不到这种效果。**CFL（荧光灯）**：绿气球变亮。**金卤灯（MH）**：光源"接近白"但光谱下大量饱和色变蓝、去饱和，RGB 因为光源先被压成三数无法还原。**HPS 高压钠（589 nm 近单色）**：光谱下所有像素只差亮度，RGB 仍把它看成红+绿保留表面色。**500 nm 完全单色**：光谱完全单色，RGB 当绿+蓝。后者 sRGB 表示为 (-1, 1, 0.36)——**负分量**即 out-of-gamut。光谱渲染对此天然免疫，只在最后一步进 RGB；RGB 渲染一开始就丢信息。Peters 直接 clamp 了负值，正规场景应用 ACES gamut compression。结论：RGB 渲染在平滑白光下"错得不多"，但在窄谱 / 峰谱 / 单色下错得非常多。Wētā FX 自 Avatar: The Way of Water 起全管线用 Peters 的 Fourier sRGB 做光谱——已产业验证。

## 关键要点

- 平滑白光谱下差别小（D65、LED）——多数 offline/real-time 无痛。
- **窄谱 / 峰谱**（CFL、MH、白炽）差别显著——RGB 无法做 desaturation 效果。
- **准单色 / 完全单色**（HPS、500 nm）差别戏剧——RGB 把单色当红+绿+蓝混合。
- **Out-of-gamut**：单色光 sRGB 表示含负分量，光谱天然免疫。
- **产业 case**：Wētā FX 全管线 spectral，用 Peters 的方法。
- 多光源 + 长路径下的波长重要性采样仍是开放问题。

## 链接到的概念

- [[spectral-vs-rgb-comparison]]
- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[hero-wavelength-spectral-sampling]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/SpectralRendering3Results.html
- 本地：`raw/articles/momentsingraphics.de/2025-11-20_spectral-rendering-part-3-spectral-vs-rgb.md`
