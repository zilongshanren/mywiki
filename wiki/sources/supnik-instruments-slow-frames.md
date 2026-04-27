---
tags: [source, profiling, performance, instruments, apple, game-engines]
date: 2026-04-27
sources: 1
---

# Finding Slow Frames With Instruments 8.0（Ben Supnik / The Hacks of Life）

[[people/ben-supnik]] 发表于 2016 年 9 月的文章，讲解如何用 Instruments 8.0 的 Points of Interest 时间轴标记精准定位游戏帧卡顿（hitch）。

## 摘要

自适应采样 profiler 的采样概率与时间成正比，在"300 帧正常 + 1 帧慢"的场景里，慢帧仅占 1.3% 采样，任何造成 hitch 的函数都淹没在噪声里。Instruments 8.0 引入 Points of Interest track，允许开发者在代码里通过 `syscall(SYS_kdebug_trace, ...)` 向时间轴注入单点标记或区间标记，从而在时间轴上直观标出帧边界和慢帧区间。Supnik 用此技术找到 X-Plane 的 hitch 根因：在飞行途中按需编译 GLSL shader 变体（on-the-fly shader compilation），每次触发新变体时产生 45ms+ 的卡顿。文章还展示了 Instruments 8.0 新增的 CPU 核视图（橙色高亮表示调度饱和），以及一次假阳性：切换应用导致的系统级 VM 抖动，与 sim 本身无关。

## 关键要点

- 采样 profiler 天然适合"找最贵函数"，不适合"找偶发慢帧"
- Points of Interest 标记需配合 System Trace（Windowed 模式），有一定工具开销
- 区间标记可精确标出慢帧内的慢操作，快速锁定根因
- X-Plane 的实际 hitch 来源：运行时按需编译 GLSL shader 变体（driver 同步编译）
- 假阳性案例：切换前台应用导致系统所有服务短暂唤醒，与游戏逻辑无关

## 链接到的概念

- [[computer-systems/frame-hitch-profiler-markers]]
- [[rendering/glsl-compiler-optimization-reliance]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/09/finding-slow-frames-with-instruments-80.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-09-20_finding-slow-frames-with-instruments-8-0.md`
