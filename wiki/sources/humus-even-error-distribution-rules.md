---
tags: [source, 图形, 软件设计, 误差分布, 设计原则, 感知]
date: 2026-04-27
sources: 1
---

# Even Error-Distribution: Rules for Designing Graphics Sub-Systems Part III（Wolfgang Engel）

[[wolfgang-engel]] 发表于 2011 年 7 月的文章，"图形子系统设计规则"系列第三部分，阐述"均匀误差分布"设计原则。

## 摘要

Engel 认为"误差"（error）是游戏视觉与真实世界体验之间的差距，它不可消除，但可以被管理。核心原则是：无论选用何种技术，都要确保误差在整个游戏中保持稳定一致，不随视角、时间或场景动态变化。他的依据是感知适应心理学：玩家能接受稳定的视觉风格化或质量降级，但对运行时的质量跳变极为敏感。文章举了跨平台开发（iOS/Android vs Windows/Xbox）的实例：在低端平台用 stencil shadow volumes、高端平台用 shadow maps，各自保持内部一致，玩家分别在各自平台上适应；但在同一平台内混用会立刻引发投诉。他特别指出：基于相机-光源夹角变化的 shadow map 质量波动、任何基于 reprojection 的技术（AO、GI、阴影的重投影）、以及混用 lightmap 与动态光照，都是违反该原则的典型案例。

## 关键要点

- "误差"不是 bug，而是一种有意的设计参数
- 均匀误差分布 = 误差恒定，而不是误差为零
- 感知适应：玩家适应稳定误差，但抗拒质量波动
- 违反案例：视角敏感的 shadow map 质量、reprojection 技术、lightmap 与动态光混用
- 该原则可作为技术选型的过滤条件：凡是产生时变质量的方案慎用

## 链接到的概念

- [[graphics-subsystem-even-error-distribution]]
- [[graphics-subsystem-no-lut]]
- [[image-quality-philosophy]]
- [[rendering-roi-philosophy]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/07/even-error-distribution-rules-for.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-07-31_even-error-distribution-rules-for-designing-graphics-sub-sys.md`
