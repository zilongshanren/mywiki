---
tags: [source, 渲染, srgb, alpha, 纹理压缩]
date: 2026-04-19
sources: 1
---

# sRGB, Pre-Multiplied Alpha, and Compression（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2022 年 6 月的纹理管线三角问题笔记——sRGB、预乘 alpha 与块压缩如何互动。

## 摘要

作者先澄清术语：**sRGB encoded** 是用 sRGB 曲线把 linear 值压到 8 bit 存储（暗部密、亮部稀，契合人眼），**alpha 永远是线性**，blend 在哪里做则决定是 "linear blending"（gamma-correct）还是 "sRGB blending"（错误但有时美术要）。接着讨论预乘 alpha 的两个动机：节省 multiply（90 年代 NeXT CPU 合成关键）、滤波/mipmap 不出现边缘 bug（非预乘纹理必须"stuff" alpha=0 像素）。核心是预乘 + sRGB 的正确顺序：(1) decode 到 linear（保持 >8 bit 精度）；(2) RGB × alpha；(3) re-encode 回 sRGB。反之——在 sRGB 值上直接 `RGB *= A`——等于在非线性曲线上乘，暗部压缩过度、边缘偏灰。文章以压缩纹理收尾（这一节原文偏短），提醒 BC/ASTC 的块内插值假设线性数据，因此预乘必须发生在压缩之前、而压缩前必须 linear。

## 关键要点

- sRGB 不是色彩空间而是 TRC（tone response curve）：8 bit 预算"花在暗部"。
- alpha 通道无论如何是线性；blend 空间由渲染管线决定，不由纹理格式决定。
- 预乘 alpha = 存 `(RGB*A, A)` 而非 `(RGB, A)`，让 `over` 算子在 filter/resample 下仍然数学正确。
- 正确顺序：**linear decode → premultiply → encode**；任何一步搞反都会产出脏色。
- 压缩纹理 + sRGB + alpha 是 AAA 资产管线最常见 bug 来源之一。

## 链接到的概念

- [[srgb-premultiplied-alpha-compression]]
- [[alpha-compositing]]
- [[alpha-blending]]
- [[gamma-correction-srgb]]
- [[color-space]]
- [[bc7-solid-color-blocks]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2022/06/srgb-pre-multiplied-alpha-and.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2022-06-11_srgb-pre-multiplied-alpha-and-compression.md`
