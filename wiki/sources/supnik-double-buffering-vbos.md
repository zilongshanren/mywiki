---
tags: [source, 渲染, opengl, vbo, 驱动]
date: 2026-04-19
sources: 1
---

# Double-Buffering VBOs（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 2 月的 OpenGL VBO 流式更新笔记——从「为什么朴素更新那么慢」出发，对照 D3D 的 `D3DLOCK_DISCARD` 推出 OpenGL 的 orphaning 写法。

## 摘要

朴素每帧重写 VBO：`glMapBuffer → 写 → Unmap → Draw`。PCIe 带宽并不短缺，但性能很差，因为 `glMapBuffer` 等同于等一把被 GPU 从 issue 到 draw 完成全程持有的锁。锁的原因是 VBO 要么在 AGP 里只有一份物理内存、要么是 VRAM + system RAM 两份镜像、任何一种都要保证 GPU 读和 CPU 写不撞。D3D 的解法是 `D3DLOCK_DISCARD`——驱动发你一块新内存填，旧那块挂在老 draw 上退休（典型 [[buffer-renaming]]）。OpenGL 里等价写法有两条：`glBufferData(NULL)` 显式 orphan（VBO 扩展 spec 承认的 `DiscardAndMapBuffer` 语义），或 `GL_MAP_INVALIDATE_BUFFER_BIT`（GL 3.0 / `ARB_map_buffer_range`）。文末讨论 MacOS 10.4.7 起就提供的 `APPLE_flush_buffer_range`——可关 map 阻塞、可 partial flush，PowerPC 收益大。评论里 map-buffer-range 合著者 Rob Barris 补充：X-Plane 放弃驱动自动 system-memory 镜像策略，宁可自己多 RAM 一份副本、明确告诉 GL「数据放 VRAM，别管了」。

## 关键要点

- 慢的不是带宽，是 map 等锁。
- 锁存在因为 VBO 的物理内存只有一份「活」拷贝。
- D3D `DISCARD` = GL `glBufferData(NULL)` / `INVALIDATE_BUFFER_BIT`——都是 orphan。
- 整块 orphan 适合每帧完全重写；局部改写需要 `UNSYNCHRONIZED` + 客户端同步。
- 驱动的 client 镜像策略在不同实现差异极大，依赖它是陷阱。

## 链接到的概念

- [[vbo-double-buffering-orphaning]]
- [[buffer-renaming]]
- [[agp-vs-vram-streaming]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/02/double-buffering-vbos.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-24_double-buffering-vbos.md`
