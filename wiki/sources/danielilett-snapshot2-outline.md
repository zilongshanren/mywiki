---
tags: [source, unity, urp, post-processing, outline, edge-detection]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders 2 - Outline（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Snapshot Shaders 2* 撰写的 **Outline** 后处理参数手册——屏幕空间三通道 edge detection 组合，区别于 [[cel-shader-outline|inverted-hull extrude 描边]]。

## 摘要

与 cel-shader 的顶点外推 + stencil mask 不同，这是**屏幕空间 post 描边**：对 framebuffer 运行 edge detection 算子，找相邻像素差异。核心参数 *Outline Algorithm* 目前只有 `DepthNormalsColor` 一种——同时比较三个通道的差：**颜色差**（*Color Threshold* / *Color Strength*）、**深度差**（*Depth Threshold* / *Depth Strength*）、**法线差**（*Normal Threshold* / *Normal Strength*）。*Skybox Depth Cutoff* 把远处超出阈值的像素（一般是天空盒）排除在 edge 之外，避免天空与地面交界处产生无意义的满屏描边。*Outline Color* + 其 alpha（全局强度 multiplier）决定描边颜色。*Drawing Mode* 有四档——`Outline` / `Neon` × `Overlay` / `Only`：Outline 用指定色画线，Neon 保留原像素色并提亮；Overlay 在原画面上叠加，Only 只保留描边（丢掉原始画面），此时 *Background Color* 用作背景。Neon 模式还有 *Neon Saturation Floor* 和 *Neon Lightness Floor* 两个下限，强行把暗/灰色像素提到最低饱和与亮度，从而在黑画面上也能看到彩色霓虹边。

## 关键要点

- **三通道同时参与 edge detection**——colour/depth/normal 任一超过阈值即为边，比单通道（只 depth 或只 normal）鲁棒得多
- Depth edge detection 要求 URP 开 [[depth-texture-silhouette|_CameraDepthTexture]]；Normal edge detection 要求 Depth-Normals prepass 开启
- Skybox Depth Cutoff 是关键细节——天空远平面的深度值是一个特殊值（≈1），不设这个 cutoff 就会在"天空 vs 任何实体"的所有交界画出强 edge，反而湮没真正的物体边
- `Neon Only` 模式等价于 [[bloom-threshold-blur-composite|bloom]] 的语义亲缘——暗 framebuffer 上点缀亮线条，常用于 cyber/赛博朋克风
- Color edge detection 在 albedo 变化大的纹理上会产生"噪声 edge"——纹理内部的花纹也被画线；Color Strength 设低、Normal/Depth Strength 设高可以回避
- 与 [[sobel-edge-detection|Sobel]] 的差异：Sobel 是算子形态（3x3 卷积），这里没说具体算子，但从单阈值判断看更接近 Roberts Cross 或 `abs(diff)` 两像素比较——参数命名用 threshold 支持这一推测
- 本效果受 [[volume-mask-layers|Masking Layers]] 控制，可以只描边特定对象

## 链接到的概念

- [[cel-shader-outline]]
- [[sobel-edge-detection]]
- [[depth-texture-silhouette]]
- [[urp-volume-post-processing]]

## 原文

- 链接：https://danielilett.com/snapshot-shaders-2/outline/
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-2-outline.md`
