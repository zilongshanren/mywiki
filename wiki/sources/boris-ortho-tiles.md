---
tags: [source, game-development, tileset, autotile, procedural-generation, grid]
date: 2026-04-27
sources: 1
---

# Ortho-tiles（Boris The Brave）

[[people/boris-the-brave]] 发表于 2023 年 5 月的文章，提出将 Quarter-tile 自动切片推广到任意多边形网格的方法。

## 摘要

文章紧接 Quarter-tile 系列。Quarter-tile 将方格切为四个象限、每象限各选一张子片，实现了以约 6 张基础切片覆盖所有邻域组合的自动切片方案。Ortho-tiles 利用 Conway 的 Ortho 算子（将每个 n 边形细分为 n 个四边形"风筝格"）将同样的规则推广到六边形、三角形乃至任意不规则多边形网格。角点取值采用"共享该顶点的所有格子取最小值"统一规则，解决了非方格网格中对角邻居定义不明确的问题。文章还展示了将方格 Quarter-tile 双线性变形以适配任意四边形形状，使得同一套美术资产可直接复用于任意网格。

## 关键要点

- Ortho 算子：n 边形 → n 个四边形风筝格，统一了后续处理
- 角点取值规则：共享顶点的所有格子中取最小值（任一为空则视为空）
- 六边形自动切片仅需 6 张基础切片（带旋转），显著低于传统方案
- 方格 Quarter-tile 可直接变形复用于任意四边形网格
- 类 Townscaper 效果可用此方法以极少美术量实现

## 链接到的概念

- [[game-development/ortho-tiles]]
- [[game-development/autotile-tileset-layouts]]
- [[game-development/tileset-classification]]
- [[game-development/triangle-grid]]

## 原文

- 链接：https://www.boristhebrave.com/2023/05/31/ortho-tiles/
- 本地：`raw/articles/boristhebrave.com/2023-05-31_ortho-tiles.md`
