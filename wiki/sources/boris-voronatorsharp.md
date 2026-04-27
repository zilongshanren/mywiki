---
tags: [source, 程序化生成, 几何算法, voronoi, delaunay, csharp]
date: 2026-04-27
sources: 1
---

# VoronatorSharp（Boris The Brave）

[[boris-the-brave]] 发表于 2022 年 9 月的工具发布公告，介绍其开源 C# 库 **VoronatorSharp**，用于计算 Voronoi 图与 Delaunay 三角剖分，支持 Unity 集成。

## 摘要

VoronatorSharp 是 Boris 将 JavaScript 库 [Delaunator](https://github.com/mapbox/delaunator) 移植到 C# 的成果。核心能力包括：根据一组点集计算 Voronoi 多边形（每个多边形包含平面上距离该点最近的区域），以及对应的 Delaunay 三角剖分（Voronoi 的对偶图）。

技术亮点方面，库采用 `n log(n)` 的 sweephull 算法，并主动减少内存分配（适合游戏运行时使用）；使用 [RobustGeometry.NET](https://github.com/govert/RobustGeometry.NET) 的鲁棒方向判断代码，处理退化情况（共线点、仅 1-2 个点）不会崩溃；Voronoi 多边形可裁剪到矩形区域，便于有界场景使用。

## 关键要点

- Voronoi 图将平面划分为「距某点最近的区域」——经典程序化地图生成基础结构。
- Delaunay 三角剖分是 Voronoi 的对偶图，同一个库同时提供两者。
- sweephull 算法：O(n log n) 增量构建，适合大点集。
- 主动减少内存分配：游戏运行时友好。
- 支持 Unity standalone，可直接用于程序化地图生成流水线。

## 链接到的概念

- [[rendering/voronoi-lava-shader]]
- [[rendering/worley-voronoi-noise]]
- [[rendering/cellular-texture-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2022/09/10/voronator-sharp/
- 本地：`raw/articles/boristhebrave.com/2022-09-10_voronatorsharp.md`
