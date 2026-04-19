---
tags: [source, 渲染, unity, urp, 后处理, noise, film-grain]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Noise Grain（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍模拟胶片颗粒噪点的后处理。

## 摘要

Noise Grain 给画面叠一层程序化噪声，模拟模拟胶片的物理杂色——既可静止（`Speed=0`）当复古颗粒、也可动态流动当电视雪花。用的是 [[classic-shader-noise|Perlin / value noise 家族]]的插值变体：`Noise Interpolation` 在 **Hermite**（`3t²-2t³`，cubic smoothstep）和 **Quintic**（`6t⁵-15t⁴+10t³`）之间切——Hermite 便宜一档、Quintic 贵一点但梯度更平滑（二阶导连续，画面走样更少）。`Strength` 控制噪声对颜色的扰动幅度、`Noise Size` 控制颗粒在屏幕上的尺度、`Speed` 控制噪声随时间滚动的速率。这四参数和 [[crt-shader-effects|CRT Shader]] 里的静电噪声、[[sources/danielilett-snapshot-pro-scanlines|Scanlines]] 的时间滚动是一套美学路线——都是给无菌数字画面"加脏"。

## 关键要点

- 四参数：`Strength` / `Speed` / `Noise Size` / `Noise Interpolation`
- `Hermite` vs `Quintic` 插值是显式的 CPU↔质量旋钮，对应 [[classic-shader-noise|value/Perlin noise]] 两档平滑
- `Speed=0` 冻结噪声做静态颗粒，配像素化做复古照片；`Speed>0` 做动态电视雪花
- `Noise Size` 大 → 粗颗粒（蒙太奇感）；小 → 细颗粒（高 ISO 胶片感）
- 和 [[crt-shader-effects|CRT]] / [[sources/danielilett-snapshot-pro-scanlines|Scanlines]] 都属"给数字画面加脏"的复古后处理家族

## 链接到的概念

- [[classic-shader-noise]]
- [[crt-shader-effects]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/noise-grain/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-noise-grain.md`
