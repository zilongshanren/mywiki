---
tags: [source, unity, shadergraph, urp, stencil, 宝可梦]
date: 2026-04-19
sources: 1
---

# Holofoil Cards in Shader Graph and Unity URP（danielilett.com / Daniel Ilett）

[[daniel-ilett]] 2025 年 10 月 URP 教程：复刻宝可梦 holo 闪卡的"视角相关彩虹条纹 + 分层 parallax"效果。

## 摘要

两个独立技巧组合：(1) 多层 sprite 在同一张卡片的不同"深度层"上，用 stencil mask + Render Objects feature 把每层按 stencil 掩回画面，得到视差分层效果；(2) holo 彩虹条纹用视角方向 + UV 的线性组合采 Hue 循环（或 Color Ramp 贴图），再乘一张 Holo Mask 限制在卡面特定区域；Height map 转 Normal map 给 holo 条纹加细节反光。

## 关键要点

- stencil mask + URP Render Objects feature 是 layer-based parallax 的干净抓手
- holo 彩虹：`dot(viewDir, uv)` 驱动 Hue 循环，Color Ramp 是等价 LUT 路径
- Height → Normal：用 `DDX/DDY` 或 `Unpack Normal` 把高度图转成法线扰动

## 链接到的概念

- [[stencil-parallax-card-layers]]
- [[holofoil-rainbow-shader]]
- [[stencil-buffer]]

## 原文

- 链接：<https://danielilett.com/2025-10-13-holofoil-cards-in-shader-graph-and-unity-urp/>
- 本地：`raw/articles/danielilett.com/2025-10-13_holofoil-cards-in-shader-graph-and-unity-urp.md`
