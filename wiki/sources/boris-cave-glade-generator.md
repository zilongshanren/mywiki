---
tags: [source, game-development, procedural-generation, dungeon-generation, algorithm]
date: 2026-04-27
sources: 1
---

# How Does Cave/Glade Generator Work（Boris The Brave）

[[people/boris-the-brave]] 发表于 2023 年 11 月的技术逆向分析文章，通过阅读 Watabou 导出的 JavaScript 源码，完整拆解其洞穴/林间空地地图生成器的工作原理。

## 摘要

Watabou 的 Cave Generator 以极具风格的手绘质感著称，其核心管线比外表复杂得多。Boris 发现生成过程全程在六边形网格（内部以 DCEL 数据结构表示）上运行，主要分为：种子扩张（随机洪水填充式区域生长）、区域连通（最小生成树或受限环路策略）、走廊收缩（反复删格并验证连通性）、以及多步几何后处理（细分、偏移、Chaikin 曲线平滑、Dyson 阴影线）。水面效果来自独立的柏林噪声。地图名称使用 Tracery 语法生成，标签系统统一控制参数预设与算法切换。Boris 总结的核心经验：优秀程序化结果来自简单规则的有效组合，而非复杂算法。

## 关键要点

- 底层是六边形网格 + DCEL，上层后处理完全隐藏了网格结构
- 种子扩张（seed growth）是核心生成算法，通过 gamma 参数控制形状从圆润到珊瑚状
- 标签系统（tags）同时承担算法切换和参数预设两种职责
- 区域连通支持：生成树（无环）、减少三角环路、全连通三种模式
- 洞穴模式与林间空地模式共享同一管线，仅边界绘制方式不同
- 简单规则有效组合 > 单一复杂算法

## 链接到的概念

- [[game-development/seed-growth-algorithm]]
- [[game-development/dungeon-generation-algorithm]]
- [[game-development/procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2023/11/19/how-does-cave-glade-generator-work/
- 本地：`raw/articles/boristhebrave.com/2023-11-19_how-does-cave-glade-generator-work.md`
