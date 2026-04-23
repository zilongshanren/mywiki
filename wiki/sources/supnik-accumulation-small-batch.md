---
tags: [source, 图形, opengl, batching, 性能]
date: 2026-04-19
sources: 1
---

# Accumulation to Improve Small-Batch Drawing（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015-03 的文章，讲 X-Plane 10 Mobile 在 OpenGL ES 上救 naive 单三角形 API 性能的**累加器**方案。

## 摘要

当 2D 游戏或低强度 GL 应用的上层代码已经写成「一次一三角形」的便利函数（`draw_colored_triangle_2d(...)` / `draw_textured_triangle_3d(...)`），短期内无法推倒重来。Supnik 提出在 GL 调用之前插入**累加器**：同状态三角形先存后发，一次 state setup + 一次大 draw 把吞吐提升约 200×。累加器同时成为 usage 统计点——记录 flush 时的 run 长度，能暴露「平均 batch=2」这类交替 shader 的结构问题。解决这类问题有两招：**draw reordering** 给渲染分层让累加器重排（X-Plane 10 Mobile UI 把「背景 × 文字」从每控件两次 shader 切换降到整窗口两次），**state merging** 用 1×1 白贴图/纯白颜色/预乘 alpha 让异质 state 走同一条管线。关键判断：合并 state 是**量准再合**，可能得不偿失，依赖具体模型 profile。批量生成几何的代码应该直接走 bulk API，累加器只是给已经长成 naive API 的代码的渐进式升级通道。

## 关键要点

- 3D 硬件**设 setup 贵、每三角形便宜**；naive 单调用 API 最大化 setup、最小化吞吐。
- profile 里 `glDrawArrays` 的 CPU 时间实际是**驱动 sync 脏状态**——见 [[opengl-state-change-deferral]]。
- 累加器合并**相同 state** 的连续三角形，同时减少驱动 state change call。
- 「平均 batch=2」通常是**上层交替 shader**——UI 背景/文字是典型例。
- **Draw reordering**：给累加器 layer 和 barrier，打乱顺序把同类运行拼到一起。
- **State merging**：白贴图代替无贴图、纯白代替无颜色、预乘 alpha 让 additive/non-additive 共存。
- 永远不要 for 循环外层发单三角形——批量几何生成应走 `draw_lots(color, count, xyz[])` 式 bulk API。

## 链接到的概念

- [[gl-draw-accumulator-batching]]
- [[batching]]
- [[draw-call]]
- [[opengl-state-change-deferral]]
- [[streaming-quads-drawing-strategies]]
- [[iphone-4-opengl-es-perf-gap]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/03/accumulation-to-improve-small-batch.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-03-17_accumulation-to-improve-small-batch-drawing.md`
