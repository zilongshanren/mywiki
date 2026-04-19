---
tags: [source, 渲染, shader, anti-aliasing, sdf]
date: 2026-04-19
sources: 1
---

# GM Shaders: Anti-Aliasing（mini.gmshaders.com / Xor）

[[xor-shader-artist]] 2025 年 1 月 mini 短教程：shader 解析抗锯齿的三档方案。

## 摘要

不走多采样 / 超采样路线，而是在 shader 里用连续函数的 1 像素 smooth step 来直接抗锯齿。三档：(1) SDF 直接拿距离做 `smoothstep(0, pixel_width, distance)`；(2) 没有 SDF 时用 `fwidth(f)` 拿屏幕空间导数作为 step 宽度；(3) 极端情况手动算 `ddx/ddy` 的梯度长度。适用于纯 procedural 图形。

## 关键要点

- SDF 天然支持解析 AA：`smoothstep(0, px, dist)`
- `fwidth(x)` = `abs(ddx(x)) + abs(ddy(x))` 是便宜的屏幕空间梯度近似
- 极端情况：手动算 `length(float2(ddx(x), ddy(x)))` 更精确

## 链接到的概念

- [[fwidth-derivative-antialiasing]]
- [[analytical-antialiasing]]
- [[sdf-operations-shader]]

## 原文

- 链接：<https://mini.gmshaders.com/p/anti-aliasing>
- 本地：`raw/articles/mini.gmshaders.com/2025-01-11_gm-shaders-anti-aliasing.md`
