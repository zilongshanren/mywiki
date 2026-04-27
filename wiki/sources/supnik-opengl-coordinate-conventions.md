---
tags: [source, rendering, opengl, metal, vulkan, coordinate, framebuffer]
date: 2026-04-27
sources: 1
---

# Keeping the Blue Side Up: Coordinate Conventions for OpenGL, Metal and Vulkan（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2019 年 4 月发表的文章，系统梳理 OpenGL、Metal、Vulkan 三套图形 API 在帧缓冲坐标（framebuffer coordinates）方向约定上的差异，以及 X-Plane 实际采用的跨平台适配策略。

## 摘要

三套 API 在纹理坐标和多边形绕序（winding order）上完全一致，分歧出在帧缓冲坐标的 Y 轴方向。OpenGL 最奇特但最自洽：NDC、Clip Space、帧缓冲坐标全部以左下角为原点，Y 轴向上，与所有窗口系统相反（驱动在最后悄悄翻转）。Metal 采用"Clip 空间 Y 向上、帧缓冲 Y 向下"的混合策略：viewport 变换内置一次 Y 翻转，与 D3D 程序员的直觉吻合，但 render-to-texture 场景下会导致"两次翻转抵消"的连锁问题。Vulkan 默认"全部 Y 向下"——与 OpenGL 整套反转——但 Vulkan 1.1 允许负值 viewport height 来补偿，使其与 Metal/DX 对齐。X-Plane 的策略：在 Metal 上主动把 Y-flip 注入 transform stack，让 render-to-texture 结果与 OpenGL 一致（草在低内存、天在高内存），但因此 viewport、front-face winding、以及使用 `gl_FragCoord`/`[[position]]` 采样时都需要单独校正。文章详细列出了 Metal 场景下 X-Plane 要做的三类后续处理：翻转 front face、不翻转普通 render-to-texture、对 gl_FragCoord 重建世界坐标时交换四角系数。

## 关键要点

- 三套 API 在纹理 UV 原点（低地址=左上角）和多边形绕序定义上一致，分歧只在帧缓冲 Y 方向
- OpenGL：全局 Y 向上，驱动为你翻转给窗口系统
- Metal：Clip 空间 Y 向上，帧缓冲 Y 向下；viewport/scissors 在帧缓冲坐标下，渲染到纹理时产生"两次翻转"问题
- Vulkan：默认全 Y 向下；Vulkan 1.1 负 viewport height 修正为 Y 向上，与 Metal/DX 对齐
- X-Plane 选择主动将 Metal 帧缓冲翻转回 OpenGL 方向，而非调整所有 UV 采样代码
- `gl_FragCoord` / Metal `[[position]]` 在翻转后需要额外处理，否则重建的世界坐标上下颠倒

## 链接到的概念

- [[framebuffer-coordinate-conventions]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[metal-api-overview]]
- [[vulkan-explicit-performance]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2019/04/keeping-blue-side-up-coordinate.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2019-04-06_keeping-the-blue-side-up-coordinate-conventions-for-opengl-m.md`
