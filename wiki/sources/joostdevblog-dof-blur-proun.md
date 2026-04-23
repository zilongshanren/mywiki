---
tags: [source, rendering, depth-of-field, bokeh, indie]
date: 2026-04-19
sources: 1
---

# Depth of field blur in Proun（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 9 月发表的文章，讲 *Proun*（抽象赛车独立游戏）为什么选用 ATI Scheuermann 的**按 CoC 变采样半径 gather DoF**，而不是当时主流的 "sharp + blur + lerp"。

## 摘要

主流 DoF 做法是先渲一张清晰图、再整屏重度模糊一张、按深度在两张之间 lerp——问题是轻度失焦的像素被"稀释成两张图的平均"，而不是真正做了一次小半径模糊，视觉会脏。Scheuermann 的 *Advanced Depth Of Field*（GDC 2004）改成每个输出像素做 gather、**采样圆盘半径由 CoC 决定**，稍失焦小半径、大失焦大半径。代价是不再可分离：同样想要 81 次采样的质量必须一 pass 里真的打 81 次 tap。Proun 最终 Very High 64 tap、High 32、Medium 16、Very Low 关。DoF 吃掉全游戏 90% GPU，因为抽象艺术下景深是玩家判断深度的唯一线索，不能省。尝试过噪声掩盖欠采样，但 Proun 画面几乎无纹理细节掩护不住，只能放弃。文章也点名表扬了 *Outcast*（1999）早了所有人十年做实时 DoF，顺带批评了 *StarCraft II* 过场里典型的"前景 sharp 边缘被背景 blur 污染出 glow"问题——而 Scheuermann 的方案因为按本像素 CoC 控制半径，天然没这毛病。

## 关键要点

- 主流 sharp + blur + lerp 的本质缺陷：两张图平均 ≠ 一次中等模糊
- 解决方案：每像素 gather，采样半径 ∝ CoC
- 不再可分离 —— N² 采样成本无法拆成 2N
- Proun 愿意花 90% 预算在 DoF，是因为抽象风格下景深承担了判断距离的唯一线索
- 噪声 trick 在低频美术风格里露馅 —— 美术风格决定能不能欠采样
- sharp + blur + lerp 的另一老毛病："sharp 前景被 blurred 背景吃掉轮廓"——variable-size gather 天生免疫
- 参考实现 shader 就在游戏目录里的 `DofPostEffect.cg`

## 链接到的概念

- [[variable-size-gather-dof]]
- [[gather-bokeh-dof]]
- [[scatter-bokeh-dof]]
- [[separable-gaussian-blur]]
- [[thin-lens-model]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/09/depth-of-field-blur-in-proun.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-09-12_depth-of-field-blur-in-proun.md`
