---
tags: [source, game-development, grid, math, procedural-generation]
date: 2026-04-27
sources: 1
---

# Triangle Grids（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 5 月的文章，论证三角网格在数学简洁性和几何属性上优于六边形网格，并给出完整的参考实现。

## 摘要

文章提出三角网格（等边三角形平铺二维平面）被严重低估，认为其数学比六边形更简单，并从三点几何优势出发：三角形天然共面（适合带高度图的地形）、三点少于四点使组合情形更少、以及天然支持重心坐标插值。核心技术贡献是三坐标系统（a, b, c），将网格分解为三组平行 lane，每个格子坐标是所属 lane 的编号三元组，使邻居、距离、中心、点选等全部简化为线性运算。文章还揭示了六边形与三角网格的对偶关系，并指出 Boris 自己的工具（Sylves、Tessera）内置了对这一坐标系统的支持。

## 关键要点

- 三角坐标 (a,b,c) 满足 a+b+c∈{1,2}，第三维冗余但使运算整洁
- 邻居计算：向上三角减坐标，向下三角加坐标，无条件分支
- 距离 = 三坐标差的绝对值之和
- 三角格的 Marching Squares 类算法只需 8 种基础情形（方格需 16 种）
- 六边形网格与三角网格互为对偶，许多六边形算法可以先在三角坐标下计算再转换

## 链接到的概念

- [[game-development/triangle-grid]]
- [[game-development/tileset-classification]]
- [[game-development/wave-function-collapse]]

## 原文

- 链接：https://www.boristhebrave.com/2021/05/23/triangle-grids/
- 本地：`raw/articles/boristhebrave.com/2021-05-23_triangle-grids.md`
