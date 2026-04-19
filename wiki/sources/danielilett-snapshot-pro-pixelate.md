---
tags: [source, 渲染, unity, urp, 后处理, pixelate, retro]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Pixelate（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Pixelate 像素化后处理的唯一参数。

## 摘要

Pixelate 是 *Snapshot Shaders Pro* 里最经典的复古风格后处理：把屏幕图像降到更低的有效分辨率再拉回屏幕。参数极简——只有一个 `Pixel Size`，表示输出"大像素"的尺寸。底层实现是 [[pixelate-postfx|`uv = floor(uv * grid) / grid` 再 point filter 放大]]，空间维度的量化，独立于 [[color-quantization-retro|颜色维度的量化]]。想做完整 NES 风格需要把 Pixelate 串上 SNES override 一起用。

## 关键要点

- 唯一参数 `Pixel Size` —— 大像素的尺寸
- 空间量化，和 color quantization 正交——两者串联才能复刻 NES/SNES 风
- 产品把 `FilterMode.Point` / UV 中心偏移 / 方形 vs 比例等细节全部锁死
- 常和 [[crt-shader-effects|CRT]]、[[color-quantization-retro|SNES]]、[[sharpen-filter|Sharpen]] 组成复古后处理链

## 链接到的概念

- [[pixelate-postfx]]
- [[color-quantization-retro]]
- [[retro-rendering-techniques]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/pixelate/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-pixelate.md`
