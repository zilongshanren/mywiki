---
tags: [source, procedural-generation, wfc, tileset, game-development]
date: 2026-04-27
sources: 1
---

# Wave Function Collapse Tips and Tricks（Boris The Brave / BorisTheBrave.Com）

[[people/boris-the-brave]] 发表于 2020 年 2 月的实践指南，聚焦如何把 WFC 用于实际可玩关卡。

## 摘要

文章开门见山：WFC 容易出结果，但难以输出有实际游戏价值的关卡——根本原因是 WFC 只施加局部约束，缺乏大尺度结构。针对这个痛点，文章分三大板块提供解法。**瓦片设计**：以 Marching Cubes 思路设计确保始终能"接上"的瓦片集，并通过"地基约束"（底部比顶部宽的瓦片）让 WFC 自然生成有支撑的建筑；递归细分近似、Big Tiles 等进一步丰富输出形状。**约束扩展**：固定瓦片（Fixed Tiles）让特定位置可预设内容；作者自创的**路径约束**（Path Constraint）作为全局补丁强制连通性，解决 WFC 最常见的"孤立区域"问题。**多样性**：按关卡选 Biome 禁用部分瓦片、按地图区域细分并用不同配置各跑一遍 WFC（Caves of Qud 的方案）。

## 关键要点

- Marching Cubes 式瓦片设计是最可靠的接缝保证策略
- 路径约束（全局连通）是对 WFC 纯局部特性的最重要补充
- 固定瓦片可做入口/出口/前置手工内容的锚点
- 分区运行不同 WFC 模板是解决单调感的有效手段（Caves of Qud）
- Bad North 的实例展示了 Big Tiles + Biome 过滤的组合威力

## 链接到的概念

- [[wave-function-collapse]]
- [[autotile-tileset-layouts]]

## 原文

- 链接：https://www.boristhebrave.com/2020/02/08/wave-function-collapse-tips-and-tricks/
- 本地：`raw/articles/boristhebrave.com/2020-02-08_wave-function-collapse-tips-and-tricks.md`
