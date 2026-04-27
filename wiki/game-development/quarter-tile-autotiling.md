---
tags: [tileset, autotile, procedural-generation, 2d, game-development]
date: 2026-04-27
sources: 1
---

# 四分之一格 Autotiling（Quarter-Tile）

Quarter-tile autotiling 是一种 2D 地形切片方案，将每个基础格拆分为四个半尺寸象限（quarter-cell），每个象限独立选择切片。它是[[game-development/autotile-tileset-layouts|Autotile 切片布局]]谱系中的"轻量"极端，以表达力换取更少的美术量和更简单的实现。

## 工作原理

基础格的每个象限（左上/右上/左下/右下）根据当前格及其相邻 3 个格的地形类型选片。以右下象限为例，参考的是当前格、右格、下格和右下格。总共 6 条规则覆盖所有象限的所有可能组合。若切片支持旋转复用，整套系统只需要 5 张半尺寸切片；不支持旋转时需 14-20 张。

这与 Marching Squares 的关键区别是：**地形标记在格子上**（而非顶点/双网格），实现更直观，不需要引入双网格偏移的心智模型。

## 与 Marching Squares 的比较

| | Marching Squares | Quarter-tile |
|---|---|---|
| 切片数（支持旋转） | 6 | 5（半尺寸） |
| 切片数（不支持旋转） | 16 | 14-20（半尺寸） |
| 地形数据存储 | 顶点（双网格） | 格子中心 |
| 大曲率弧线 | 支持 | 不支持 |
| 多地形过渡 | 直接支持 | 间接（叠层或专用切片） |

Quarter-tile 的本质限制来自象限尺寸：地形边界必须落在象限内部，这意味着无法绘制半径超过半格的平滑曲线，两种地形等宽分布的边界也难以表现。

## 预组合（Precomposition）

在引擎中直接处理象限切片需要额外代码支持。实践中更常见的做法是将所有象限组合预先烘焙成完整的 48 张 blob 切片，然后走标准 autotile 管线。TileGen、Tilesetter 等工具自动完成这一步骤。这也解释了为何 RPG Maker 的 autotile 系统（即此方案的工业标准实现）对外暴露 48 张切片而非象限原语。

## 多地形处理

Quarter-tile 没有原生的多地形机制，通常采用两种变通方案：

1. 每种地形独立一套 autotiling 层叠加，利用透明度过渡
2. 为每对常见地形组合专门绘制过渡切片，在象限级别判断两侧最主要的地形类型

## 3D 扩展

三维中对应的是八分之一格（Eighth-tile / Marching Cubes 的轻量替代），将体素格子拆成 8 个小块，参考 8 个相邻格。

## 相关概念

- [[game-development/autotile-tileset-layouts]] — 从 Marching Squares 到 Blob/Sub-blob 的完整谱系
- [[game-development/tileset-classification]] — Boris 对切片集类型的系统分类
- [[game-development/ortho-tiles]] — quarter-tile 向非方形网格的推广
- [[rendering/marching-squares-ambiguities]] — Marching Squares 的歧义切片问题

## Sources

- [[sources/boris-quarter-tile-autotiling]]
