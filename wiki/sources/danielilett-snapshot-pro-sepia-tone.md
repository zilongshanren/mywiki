---
tags: [source, 渲染, unity, urp, 后处理, sepia, color-grading]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Sepia Tone（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Sepia Tone 棕褐色调后处理的唯一参数。

## 摘要

Sepia Tone 是 [[image-effect-colour-transform|RGB → RGB 3×3 非对角矩阵乘法]] 风格化的最小实例：让画面看起来像泛黄的老照片。数学和 Daniel 在 *Image Effects Part 1* 里的教程完全一致——Rec.601 亮度点乘得出 luminance，再乘以经典棕褐色系数（近似 `[0.393, 0.349, 0.272] / [0.769, 0.686, 0.534] / [0.189, 0.168, 0.131]`）得到三通道结果。Pro 版只暴露一个 `Blend` 参数——`0` 无变化、`1` 完全 sepia——典型产品哲学：把一条色调映射固化成可调强度的开关。

## 关键要点

- 唯一参数 `Blend` —— 从原图到 sepia 结果的 lerp 权重
- 基于 pixel **luminance**（不是 3×3 矩阵直乘原 RGB，而是先取亮度再上色调）——因此饱和信息被压扁，只保留明暗分布
- 和 [[image-effect-colour-transform|教程版 Sepia]] 数学同源——Pro 版是 Volume override 化
- 和 [[color-lut|Color LUT]] 相比：3×3 矩阵 + Blend 两参数连续可调、成本更小、LUT 则表达任意非线性
- 典型用途：回忆镜头、老照片、复古过场

## 链接到的概念

- [[image-effect-colour-transform]]
- [[color-space]]
- [[color-lut]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/sepia-tone/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-sepia-tone.md`
