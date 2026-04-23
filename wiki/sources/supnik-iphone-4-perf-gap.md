---
tags: [source, graphics, opengl-es, mobile, iphone-4, x-plane]
date: 2026-04-19
sources: 1
---

# OpenGL ES Performance: The iPhone 4 Performance Gap（Ben Supnik）

[[ben-supnik]] 2014-12-26 发表于 *The Hacks of Life*，X-Plane 10 Mobile 已经发货、且刻意把最低机型抬到 iOS 8（剔除 iPhone 4）之后的性能复盘。

## 摘要

文章的起点是一条观察：iPhone 4 不是"比 4S 慢 20%"这种均匀退化，而是"代码在新机跑得好，一到 4 就像要把自己撞死"的断崖。作者承认没能彻底搞清楚根因——但留下了三条可复用的观察：iPhone 4 唯一会在顶点阶段卡死（tiler utilization 95%+）；varying 数量**和 varying 如何打包**对性能都极敏感，把 fog + emissive 塞进一个 `vec2` 显著加速；VBO 的 orphan / respecify 路径在老驱动里代价不可忽略，但同样的代码在新设备上只占 < 1%。评论区 Mihai 补充了一条工程细节：UV 在 fragment shader 里解包会变成 dependent texture lookup，在 SGX543 上比直接当 varying 传慢得多。文末抛出"规范说 API 做什么，不说多快"的观点，直接导向三个月后对 [[vulkan-explicit-performance|Vulkan 显式性能]] 的评价。

## 关键要点

- iPhone 4 在顶点阶段瓶颈：95%+ tiler / < 30% renderer，修 fragment shader 没用
- varying 的**数量**和**打包方式**都对性能敏感，`vec2` 打包 fog+emissive 比两个 scalar 快
- 但 UV varying 必须放 `XY`，否则 fragment shader 里的 UV 解包触发 dependent texture lookup
- VBO orphan 池回收在 iPhone 4 上可观察，新设备上几乎看不见
- 规范定义 API 行为但不定义性能——Metal / Vulkan 的卖点之一是**确定性性能**

## 链接到的概念

- [[iphone-4-opengl-es-perf-gap]]
- [[vulkan-explicit-performance]]
- [[vbo-double-buffering-orphaning]]
- [[tbdr-vs-imr]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2014/12/opengl-es-performance-iphone-4.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2014-12-26_opengl-es-performance-the-iphone-4-performance-gap.md`
