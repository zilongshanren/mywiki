---
tags: [source, graphics, opengl, instancing, benchmark]
date: 2026-04-19
sources: 1
---

# Instancing Limits（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 5 月 24 日的续篇，给 [[sources/supnik-instancing-numbers|同年 3 月的 instancing 吞吐数字]] 加了两条新边界：上限与下限。

## 摘要

继续压 X-Plane 的 OpenGL GPU instancing 后，在一台搭 ATI 显卡的 Mac 上发现**上限约 100k 个 instanced batch**——再往上吞吐就挡住。与此同时存在一个**下限**：单个 instanced batch 里 instance 数量过少时，走普通 immediate mode 多次 draw 反而更快；Supnik 推测这个切换点**很低，大约 2–3 个 instance**。另附一条踩坑：OS X 10.6.x 上，如果 instance 数据放在系统内存（client array）而不是 VBO，走的是**非加速路径**，性能直接塌掉。正文还点出中层工程权衡——**大 clump（少 driver 调用，但屏外部分不能 cull 多画了）vs 小 clump（多 driver 调用，但 cull 得彻底）** 的 trade-off 还在调。

## 关键要点

- 上限：ATI Mac 上约 **100k instanced batch**
- 下限：instance 数 ≤ 2–3 时，immediate mode 多次 draw 更快
- client array 走 instancing 在 OS X 10.6.x 非加速，**必须放 VBO**
- 另一个未定的甜点：clump 粒度 vs cull 效率的 trade-off

## 链接到的概念

- [[xplane-instancing-2011-numbers]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/instancing-limits.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-24_instancing-limits.md`
