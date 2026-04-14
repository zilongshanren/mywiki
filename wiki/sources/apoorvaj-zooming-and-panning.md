---
tags: [source, 渲染, 图像编辑, fragment-shader]
date: 2026-04-14
sources: 1
---

# Zooming and panning —— Papaya GPU 图像编辑器起步（Apoorva Joshi / apoorvaj.io）

[[apoorva-joshi]] 在 2015 年 7 月写的一篇 Papaya 项目早期笔记。Papaya 是他业余做的开源 GPU 图像编辑器，C++ + OpenGL + Dear ImGui。这篇博客对比 Papaya 和 GIMP 在**视图缩放平移**与**大直径笔刷绘制**两个场景的性能差距，并解释为什么 GPU 方案不是「优化了几毫秒」，而是差一个数量级。

## 摘要

Papaya 把整张画布做成一个 **textured quad**，缩放平移完全交给采样器，放大时走 nearest、缩小走 linear，CPU 完全不碰像素——而 GIMP 这类 CPU 方案每帧都要自己跑重采样。笔刷对比更极端：直径 2048、图 4096×4096 时，GIMP 的 `O(n²)` 距离测试 + 拖动路径上一连串圆的并集慢到无法交互；Papaya 在 [[fragment-shader]] 里把笔刷画到一张辅助 render target，然后交换主/辅纹理句柄，时间**与笔刷大小无关**。作者附了一张 `__rdtsc()` + `QueryPerformanceCounter` 测出的对比图，GPU 版本压倒性领先。UI 用 Dear ImGui ——所有按钮、工具栏也都是 textured quad。

## 关键要点

- CPU 图像编辑器的瓶颈不在算法复杂度，而在「每次视图变化都要自己做重采样」——这件事 GPU 的采样器是免费硬件。
- 笔刷不该用「圆内距离测试」的循环实现，应写成 fragment shader，按 UV 判定像素在不在笔刷范围内。
- 画 stroke 需要 ping-pong framebuffer：shader 采样主纹理 + 笔刷 → 输出到辅助纹理 → 交换句柄。
- 整套界面用 Dear ImGui，所有控件都是带纹理的 quad，避开了原生 UI 框架的重量级依赖。
- 性能测量方法：`__rdtsc()` 读周期，`QueryPerformanceCounter` 读毫秒，release build。

## 链接到的概念

- [[gpu-image-editor-brush]]
- [[fragment-shader]]
- [[image-resampling-filters]]
- [[alpha-compositing]]

## 原文

- 链接：https://apoorvaj.io/building-a-fast-modern-image-editor
- 本地：`raw/articles/apoorvaj.io/2015-07-03_zooming-and-panning.md`
