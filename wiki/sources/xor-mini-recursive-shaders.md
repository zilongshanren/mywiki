---
tags: [source, 渲染, shader, 后处理, 多趟渲染]
date: 2026-04-14
sources: 1
---

# Mini: Recursive Shaders（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 8 月的一篇 Mini，讲**多趟 shader 和 ping-pong surface**——怎样用两张 surface 完成任意多趟后处理和反馈效果。

## 摘要

文章从一个实际问题开篇：9×9 盒模糊要 81 次采样，太贵了；拆成两趟 5×5 模糊只要 50 次，再大的半径差距更夸张。同理适用于描边、bloom、辉光等卷积类效果——所以"要不要分多趟"是每个 graphics coder 都该习惯问自己的问题。朴素做法是为每趟建一个新 surface，10 趟 bloom 就要 10 张显存开销（还要乘以 surface depth 的副本）。Xor 的解法是 **ping-pong**：只建两张 surface `A`、`B`，反复 `A → B → A → B` 倒腾。对于"用上一帧输入这一帧"的反馈 shader（feedback），用一个 boolean `surface_swap` 每帧取反来切换读写目标即可。代码样板只有 3 行。

## 关键要点

- **多趟拆分 = 采样数降维**：把一次 N×N 模糊拆成 k 次小模糊，总采样从 O(N²) 降到 O(k·M²)。
- **Ping-Pong**：两张 surface 轮流当源和目标，显存占用与 pass 数解耦。
- **Dual-Kawase**：作者自己有一个更快的模糊库 [Dual-Kawase](https://github.com/XorDev/Dual-Kawase)，思路同源。
- **Feedback shader**：跨帧 ping-pong 能产生随时间演化的视觉效果（流体、粒子、残影）。
- GameMaker 里的实现只需一个布尔开关 `surface_swap = !surface_swap;` 和两个三元选择。

## 链接到的概念

- [[ping-pong-surfaces]]
- [[fragment-shader]]
- [[render-graph]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-recursive-shaders-1308459
- 本地：`raw/articles/mini.gmshaders.com/2022-08-19_mini-recursive-shaders.md`
