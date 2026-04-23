---
tags: [source, 渲染, 坐标, 引擎架构]
date: 2026-04-19
sources: 1
---

# How To Scroll the OpenGL World（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 2 月的文章，讨论 X-Plane 这类跨地球尺度的引擎如何在 32-bit float 下维持坐标精度。

## 摘要

观察者远离 origin 后，单精度浮点在顶点上开始丢位，需要**周期性重置坐标系**。Supnik 列三种方案：(1) 停世界整体 transform——X-Plane 当时用的，问题是 mesh 大量驻 GPU，要从 VRAM 拖回 CPU，被 PCIe 带宽掐死；(2) 世界双缓冲——切换零成本但内存翻倍，2010 年消费机吃不下；(3) 每个 tile 自带局部坐标系，只改层级矩阵。方案 3 的难点是相邻 tile 的接缝处经过不同矩阵变换后可能产生像素级 crack。Supnik 在后续评论里给出「3a」优化：每顶点记所属坐标系编号，边界三角形的边顶点统一用邻 tile master 侧的 transform。评论区补充了 Dungeon Siege「无世界空间」、Tom Forsyth 整数位置、CPU 双精度 × 单精度转换、24 字节顶点编码等多条工业界做法。

## 关键要点

- 32-bit float 世界空间在公里/星球尺度必然丢精度。
- 三种应对：整体 transform / 世界双缓冲 / 局部坐标系。
- 局部坐标系的接缝 crack 可以用「顶点带坐标系编号 + 边界用 master 侧 transform」解决。
- Dungeon Siege 的「no world space」是经典参考。
- Scene graph 用 double、draw 时转 float 是简单可行的务实方案。
- 24 字节顶点位置模拟 double precision 是另一条路。

## 链接到的概念

- [[huge-world-coordinate-precision]]
- [[coordinate-spaces]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/02/how-to-scroll-opengl-world.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-04_how-to-scroll-the-opengl-world.md`
