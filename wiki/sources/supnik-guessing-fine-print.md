---
tags: [source, opengl, driver, fast-path, profiling]
date: 2026-04-19
sources: 1
---

# Guessing the Fine Print（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 6 月 1 日的姊妹篇博文。用伪代码展示 OpenGL 驱动内部判断 VBO 是否进 fast path 的 if 瀑布：结构体对齐、源是否在 AGP、size 区间、命令缓冲空闲量等几十个条件 `&&` 在一起，再叠上 `FIX_STALL_BUG` 这类临时补丁分支，最终才决定走加速路径还是 fallback。

## 摘要

驱动 fast path 是 API 文档之外的隐性契约，Supnik 称之为性能意义上的 leaky abstraction。他给出 X-Plane 的实际翻车案例：Instruments 2.x Time Profiler 里某帧 67% 时间卡在 `glCopyTexSubImage2D`——其中 57% 落在 `gldFinish`（Apple 等待 nVidia 完成像素 fill），8% 落在 `glgProcessPixelsWithProcessor`（CPU 做像素操作）；Driver Monitor 同时看到 time spent waiting in user code 与 texture page off bytes 非零。根因是代码用 `glCopyTexImage2D` 把 RGBA16F 回读到 RGBA8 以凑 gamma，驱动合理地 punt 到 CPU 路径。改用同格式 FBO blit 后问题消失。启示：fast path 只能通过 profile 反推，API 表面看不出。

## 关键要点

- OpenGL 驱动 fast path 由几十条隐式条件 `&&` 组成
- Joel Spolsky 的 leaky abstraction 在性能层也成立
- Instruments 2.x Time Profiler 能看到 driver 内部符号
- `glCopyTexImage2D` 跨格式（RGBA16F → RGBA8）必然 punt
- Driver Monitor 两个关键指标：user-code 等待 + texture page off
- 解法：同格式 + FBO，避开驱动内置 pixel ops

## 链接到的概念

- [[opengl-ext-vs-arb-fast-path-leak]]
- [[api-fast-path-design]]
- [[agp-vs-vram-streaming]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/06/guessing-fine-print.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-06-01_guessing-the-fine-print.md`
