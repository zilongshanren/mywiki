---
tags: [source, opengl, vbo, 驱动, 同步, 渲染]
date: 2026-04-19
sources: 1
---

# When Is Your VBO Double Buffered?（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 8 月的第四篇 VBO 流式写入系列文，用「如果是我来写 GL driver」的视角把前三篇（[[sources/supnik-double-buffering-vbos|double-buffering-vbos]]、[[sources/supnik-agp-vs-vram|agp-vs-vram]]、[[sources/supnik-glbuffersubdata|glbuffersubdata]]）的散论收成一个更清晰的解释框架。

## 摘要

OpenGL 开发者写「每帧刷 VBO」的粒子系统时，profiler 几乎都会卡在 `glMapBuffer` 或 `glBufferSubData`——原因不是带宽，是 GPU 持有 buffer 锁没放。为什么 driver 不帮你做双缓冲？Supnik 把驱动侧的困难一条条摆开：(1) **VRAM 不是天然的第二份 buffer**：VBO 不总是 shadow 在 VRAM，就算在，重新 DMA 要阻塞，把 VRAM 当双缓冲还会让 「do not purge」的数据挤爆 VRAM；pending `glReadPixels` 更是复杂化一切。(2) **buffer 不按 region 管理**：`glBufferSubData` 并不知道你打算只改一半留一半，要知道得追踪每个 range 的 pending draw，成本太高。(3) **一种真正可用的双缓冲方式**：`glBufferData(target, size, NULL, usage)` —— 告诉 driver「我扔掉原内容」，driver 就会在内部 rename 成一块新 physical 内存，老的挂在 pending draw 上慢慢回收。或者用 OS X 的 `APPLE_flush_buffer_range` / GL 3.0 的 `MAP_UNSYNCHRONIZED`。评论里有人补充「直接自己维护两个 VBO」，实测动态几何占比很低所以双份内存并不肉痛。

## 关键要点

- VBO 卡住不是带宽而是同步——GPU 持锁直到 draw 完成
- VRAM 作为双缓冲几乎不可行（shadow 不一定在、DMA 阻塞、VRAM 压力、readback 复杂）
- driver 不做 region 级管理的原因：要追 pending draw 的 range，成本远高于收益
- 三种 orphan 写法：`glBufferData(NULL)`、`MAP_INVALIDATE_BUFFER_BIT`、`APPLE_flush_buffer_range`
- 应用侧「自己 alloc 两个 VBO」在动态几何占比低时是便宜又可控的方案

## 链接到的概念

- [[vbo-double-buffering-orphaning]]
- [[buffer-renaming]]
- [[glbuffersubdata-serialization]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/08/when-is-your-vbo-double-buffered.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-08-11_when-is-your-vbo-double-buffered.md`
