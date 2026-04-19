---
tags: [source, 渲染, unity, urp, 后处理, neon, sobel, hsl]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Neon (Sobel)（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍基于 Sobel 边缘的霓虹风格描边后处理。

## 摘要

Neon (Sobel) 把 [[sobel-edge-detection|Sobel]] 拿来当掩膜：先对原图做一次边缘检测得到边缘强度，再把原像素按 HSL 空间的饱和度和明度**分别向上钳到 Floor**，最后把"饱和 + 提亮"的颜色乘以 Sobel 强度。结果是边缘处颜色炸出来像霓虹灯管、内部变黑——和 [[sobel-edge-detection|Sobel 页]] 里描述的 Image Effects Part 5 Neon 变体思路一致。两个参数 `Saturation Floor` / `Lightness Floor` 都是"把颜色往鲜艳里拉"的兜底值：任何 saturation < Floor 的像素都被钳到 Floor 值，明度同理。Floor=1.0 会把整张图推成最饱和的原色霓虹，Floor=0 退化成普通 Sobel 黑底描边。

## 关键要点

- Sobel 强度当掩膜 × HSL 提饱和提亮后的原色 → 边缘发光
- `Saturation Floor` / `Lightness Floor` 是 HSL 空间的两个下限钳位
- 在 HSL 而非 HSV 里做——明度是对称的两端夹（0 黑 1 白），钳位方向明确
- 典型链路：Neon → Bloom 形成完整霓虹效果（产品外用户自己在 Volume 里叠）
- 和 [[sources/danielilett-snapshot-pro-outline-sobel|Outline (Sobel)]] 共用边缘计算核

## 链接到的概念

- [[sobel-edge-detection]]
- [[color-space]]
- [[bloom-threshold-blur-composite]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/neon-sobel/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-neon-sobel.md`
