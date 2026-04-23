---
tags: [source, 渲染, alpha, blend-state, opengl]
date: 2026-04-19
sources: 1
---

# Alpha Blending, Back To Front, Front To Back（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 2 月的短文，从 NVIDIA smoke particles 论文里提取出**前向 alpha 混合**的 blend state 配方，并顺便补了个「back-to-front 累积 alpha 正确」的反转 alpha 变体。

## 摘要

前向合成要求 framebuffer 有 alpha 通道记录「还剩多少光可穿透」。配方：初值 `(0,0,0,0)`，blend 设 `GL_ONE_MINUS_DST_ALPHA, GL_ONE`，并在 shader 里把 `RGB *= alpha` 自行预乘。这样画完的半透明层在贴回主场景时用 `GL_ONE, GL_ONE_MINUS_SRC_ALPHA`（因为已经是 premultiplied）。作者顺带讨论 back-to-front 的一个老问题：4 层 50% 不透明叠起来 framebuffer 的 alpha 仍近 0.5，而物理正确值是 0.9375，后续 blit 到外层就会失真。解法是**反转 alpha 语义**——0 当不透明、1 当透明——用 `glBlendFuncSeparate` 让 alpha 通道走 `GL_ZERO, GL_ONE_MINUS_SRC_ALPHA`（乘法累积透明度），最后 composite 时用 `GL_ONE, GL_SRC_ALPHA` 把反转过的 alpha 吃回去。

## 关键要点

- 前向 blend：`GL_ONE_MINUS_DST_ALPHA, GL_ONE` + shader 自行预乘。
- Compose 前向层回主场景：`GL_ONE, GL_ONE_MINUS_SRC_ALPHA`。
- back-to-front 的累积 alpha 失真，解法是反转 alpha 通道 + 分通道 blend。
- 反转方案需要 GL 1.4 / `glBlendFuncSeparate`。
- 本质都是让 hardware blend state 精确匹配 [[alpha-compositing|Porter-Duff]] 方程。

## 链接到的概念

- [[alpha-blending-front-to-back]]
- [[alpha-blending]]
- [[alpha-compositing]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/02/alpha-blending-back-to-front-front-to.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-18_alpha-blending-back-to-front-front-to-back.md`
