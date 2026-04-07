---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 5 —— 像素的命运

RTR 学习推送第 5 天。

## 摘要

**Pixel Processing 阶段**：Fragment Shader + Merging（不可编程但高度可配置）。深度/模板/Alpha 混合测试的性能含义。**Early-Z vs Late-Z**、**HSR（TBDR 独有）**、**discard 的高成本**。Stencil Buffer 的低成本强大效果（描边/传送门/延迟光照）。

## 关键要点

- **Z-Buffer**：O(n) in 图元数，允许任意渲染顺序（对不透明物体）。
- Z-Buffer 无法处理半透明（只能存一个深度）。
- **Early-Z** 在 shader 前剔除，被 `discard`/`gl_FragDepth`/alpha test 破坏。
- **HSR（Hidden Surface Removal）**：TBDR 在 tile 粒度消除被遮挡 fragment。
- 一个 `discard` 可让 TBDR GPU 从 1× 变 4× 过度绘制代价。
- 透明物体必须从后往前渲染，不写 Z。
- **Stencil Buffer**：8bit 每像素，性能几乎零成本，效果极多。
- **MRT（Multiple Render Targets）**：一 pass 写多纹理。
- **Overdraw**：多 fragment 对应一 pixel = 多次 shader 执行。

## 链接到的概念

- [[fragment-shader]]
- [[z-buffer]]
- [[early-z-late-z]]
- [[hsr-tbdr]]
- [[alpha-blending]]
- [[stencil-buffer]]
- [[overdraw]]

## 原文

- 链接到：[[raw/articles/real time rendering/day05]]
