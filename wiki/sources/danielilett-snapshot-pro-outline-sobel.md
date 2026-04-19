---
tags: [source, 渲染, unity, urp, 后处理, outline, sobel]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Outline (Sobel)（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍最基础的 Sobel 全屏描边后处理。

## 摘要

Outline (Sobel) 是 Snapshot Pro 里最朴素的一档描边：纯粹对 color buffer 跑 [[sobel-edge-detection|Sobel 核]] 得到边缘强度，按 `Threshold` 二值化后，边缘像素染成 `Outline Color`、非边缘像素染成 `Background Color`。这和 [[sources/danielilett-image-effects-edge-detection-bloom|Image Effects Part 5]] 里的 Line Drawing 变体是同一算法——区别只是 Pro 版把参数化做成 Volume override。如果 `Background Color` 设成透明，原图就会从非边缘像素下透出来——这一档不做彩色擦除、只在上面叠一圈 Sobel 线稿，是四档 Snapshot Pro outline 里最轻量的一档（对比 [[sources/danielilett-snapshot2-outline|三通道 outline]] 做 color/depth/normal 三路 Sobel 合成）。

## 关键要点

- 单信号源：对 color 跑 Sobel，不碰 depth/normal
- `Threshold` 控制边缘灵敏度，典型 `0.1` 起调
- `Outline Color` / `Background Color` 两色覆盖——非边缘可透明以露出原图
- 与 [[sources/danielilett-snapshot-pro-neon-sobel|Neon (Sobel)]] 共用同一核，只是把边缘强度换了一种合成方式
- Volume `Enabled` 开关——URP Volume override 的标配

## 链接到的概念

- [[sobel-edge-detection]]
- [[toon-outline-post-process-modes]]
- [[cel-shader-outline]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/outline-sobel/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-outline-sobel.md`
