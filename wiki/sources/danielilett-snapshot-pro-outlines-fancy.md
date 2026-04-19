---
tags: [source, 渲染, unity, urp, 后处理, outline, sobel, depth, normals]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Outlines (Fancy)（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 color / depth / normals 三通道合成的高级描边后处理。

## 摘要

Outlines (Fancy) 是 Snapshot Pro outline 家族里**最完整**的一档：同时对 color buffer、`_CameraDepthTexture`、`_CameraNormalsTexture` 跑 [[sobel-edge-detection|Sobel 式梯度]]，三路独立出一对 `Sensitivity / Strength` 参数，最后加权叠合成单色描边。这正是 [[toon-outline-post-process-modes|Toon Shaders Pro]] 里 *Depth Normal Color Outlines* 的同款算法，也是 [[sources/danielilett-snapshot2-outline|Snapshot 2 outline]] 的产品化版本。三通道组合能解决单通道的盲区：color 抓不到同色相邻物体（靠 depth 补）、depth 抓不到同平面不同朝向（靠 normals 补）、normals 抓不到同朝向不同颜色（靠 color 补）。`Depth Threshold` 是远裁距离——超过这个归一化深度就不做检测，避免天空/远景被误判边缘。

## 关键要点

- 三路 Sobel 合成：color + depth + normals，各给独立 `Sensitivity / Strength`
- `Outline Colour` 单色覆盖——不像 Outline (Sobel) 暴露 Background Color
- `Depth Threshold`（归一化深度）用来裁掉远距离误判，天空/远景不出线
- 三通道互补覆盖单通道盲区——同色相邻、同平面不同朝向、同朝向不同颜色都能画出边
- 和 [[toon-outline-post-process-modes|Toon Shaders Pro 的第 1 档 Outline Type]] 是同一算法

## 链接到的概念

- [[sobel-edge-detection]]
- [[toon-outline-post-process-modes]]
- [[depth-texture-silhouette]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/outlines-fancy/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-outlines-fancy.md`
