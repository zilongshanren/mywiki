---
tags: [人物, 作者, shader, unity]
date: 2026-04-14
sources: 8
---

# Alan Zucconi

独立开发者、技术作家、前伦敦大学金史密斯学院讲师，以大量免费的 Unity shader 教程闻名于游戏开发社群。博客 [alanzucconi.com](https://www.alanzucconi.com/) 覆盖物理光学（彩虹、衍射光栅、薄膜干涉、虹彩）、次表面散射、体积渲染、SDF、程序化纹理等主题，每个系列都附带 Unity 工程下载（Patreon）。他的写作风格偏教学：先从物理直觉出发，再推导数学，最后落到一段可复制的 Cg / HLSL 片段，非常适合 shader 入门者按图索骥。

## 代表系列

- **Improving the Rainbow**（2017）——推导 branchless 的波长→RGB 拟合 `spectral_zucconi` / `spectral_zucconi6`，改进自 GPU Gems 的 bump 方案
- **CD-ROM Shader: Diffraction Grating**（2017）——基于 grating equation 的物理光栅着色器，结合 [[spectral-zucconi-rainbow]] 和从 UV 推出的切向
- **Fast Subsurface Scattering in Unity**（2017）——把 DICE Frostbite 在 GDC 2011 提出的「back light + subsurface distortion」廉价 SSS 近似移植到 Unity Surface Shader
- **Volumetric Rendering**（2016-）——从 raycasting 入门到 [[volumetric-raymarching-intro|distance-aided raymarching]] + SDF 的完整 Unity 教程系列
- **Journey Sand Shader**（2019）——逆向分析《Journey》沙丘的 diffuse、rim、ocean specular、glitter、ripples 六个 pass

## 相关

- [[spectral-zucconi-rainbow]]
- [[diffraction-grating-shader]]
- [[fast-translucency-wraplight]]
- [[volumetric-raymarching-intro]]
- [[journey-sand-specular]]
- [[physically-based-shading]]
- [[gpu-driven-grass-tiles]] —— Marco Giordano 的 grass 系统直接用了 Alan Wolfe 的蓝噪声采样代码
- [[worley-voronoi-noise]] —— 2015 年的 To Voronoi and Beyond 教程补充到此页
- [[color-quantization-kmeans]] —— 2015 年用 K-Means 从截图提主色

## Sources

- [[sources/alanzucconi-improving-rainbow-2]]
- [[sources/alanzucconi-cdrom-diffraction-2]]
- [[sources/alanzucconi-fast-sss-1]]
- [[sources/alanzucconi-volumetric-rendering]]
- [[sources/alanzucconi-journey-sand-specular]]
- [[sources/alanzucconi-flixel-retro-crt]]
- [[sources/alanzucconi-to-voronoi-beyond]]
- [[sources/alanzucconi-main-colours-kmeans]]
- [[sources/alanzucconi-shader-intro-unity]]
