---
tags: [unity, 渲染, 后处理]
date: 2026-04-05
sources: 1
---

# 颜色 LUT（Color Lookup Texture）

颜色 LUT（Color Lookup Texture）用于 **color grading**——把一个输入颜色通过查找表映射到一个输出颜色，实现色调调整。

在 Custom SRP 中，颜色 LUT 由 `PostFXPass` 生成，每个相机独立。

## 分辨率

LUT 的 resolution 是一个整数（如 16、32、64）：
- resolution 16 → LUT strip 宽度为 256 像素
- resolution 32 → 1024 像素
- resolution 64 → 4096 像素

分辨率决定了颜色的量化精度，也决定了显示条带的宽高比。

## 调试可视化

Custom SRP 6.1.0 为颜色 LUT 添加了调试可视化：

- **启用方式**：在 Rendering Debugger 面板勾选「Show Color LUT」开关。
- **显示位置**：屏幕底部的矩形区域。
- **绘制方式**：不逐像素映射，而是按窗口宽度拉伸显示。
- **高度计算**：`height = 2 * _CameraBufferSize.y * _CameraBufferSize.z / _ColorLUTResolution`，即 LUT 的宽高比乘以 2（因为 clip space 宽度覆盖 -1 到 1 的两个单位）。
- **投影方向处理**：根据 `_ProjectionParams.x` 正负决定 top/bottom 坐标，与 DirectX/OpenGL 的 V 方向约定兼容。

## 对于设计原则的意义

颜色 LUT 的调试显示本质上是一次**把隐藏信息可视化**的操作——LUT 原本只通过 frame debugger 才能查看，现在暴露成一个运行时可见的 debug UI。这与 [[information-hiding]] 的方向相反：设计目的不是隐藏，而是让开发者能在运行时验证数据。

## 相关

- [[scriptable-render-pipeline]]
- [[custom-srp]]
- [[debug-visualization]]
- [[render-graph]]
- [[fourier-srgb-spectral-upsampling]] — 另一种 3D LUT 的用法：sRGB → Fourier sRGB 光谱上采样预处理
- [[frost-kiwi]] — Frost 关于视频游戏如何使用 1D/3D LUT 的长文（Left 4 Dead tinting、DaVinci Resolve 调色 LUT 烘焙）
- [[perceptual-colormaps]] — matplotlib 感知均匀 colormap 烘成 1D .cube LUT 给 DaVinci Resolve 热成像调色
- [[color-banding]] — dither 去色带的理论与 Jimenez 一行 GLSL 噪声
- [[skysaga-rendering-tech]] —— SkySaga 用 per-biome 3D LUT 取代 Reinhard/Filmic tonemap 做风格化 color grading

## Sources

- [[sources/custom-srp-6-1-0]]
- [[sources/frost-kiwi-luts-in-video-games]]
- [[sources/frost-kiwi-thermal-colormaps]]
