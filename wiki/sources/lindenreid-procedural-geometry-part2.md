---
tags: [source, unity, 程序化几何, mesh]
date: 2026-04-14
sources: 1
---

# Intro to Procedural Geometry, Part 2（Linden Reid）

[[linden-reid]] 2018 年 2 月的 Unity 程序化几何教程第 2 篇。第 1 篇从平面开始，本篇进阶到 cube，把 Unity `Mesh` API 的两个核心数组——`vertices` 和 `triangles`——的填写方式讲清。

## 摘要

教程以一个 2×2×2 centered-at-origin 的 cube 为例：8 个角顶点、36 个三角形索引（6 面 × 2 三角 × 3 顶点）。作者先让读者自己推出顶点坐标——因为居中 + 对称，每个分量就是 ±1——再重点讲 Unity 的**顺时针 winding order**：三角形的顶点顺序必须从"希望可见的那一面"看过去是顺时针，否则会被背面剔除。她只完整给出了顶面的三角形索引，其他面留给读者自己画图推导。末尾提示"现在光照看起来很怪"，铺垫下一篇的法线和 UV。这篇是系列里面向初学者的"手感训练"——它不讲性能、不讲共享顶点的硬边/软边问题，只确保读者建立起"mesh = 一个顶点列表 + 一个索引列表"的基本心智模型。

## 关键要点

- `Mesh` 的最小 API：`mesh.vertices = Vector3[]`、`mesh.triangles = int[]`、`mesh.RecalculateNormals()`。
- 三角形数量 = 面数 × 2，索引数 = 三角形数 × 3。
- Unity 用**顺时针** winding order 判定正面；写错会出现"面缺了"。
- 作图比硬算快——每个面画张小图再列顶点索引。
- 文章的评论区里读者抓到两处数组长度 typo（4 应为 8、42 应为 36），作者已修正。

## 链接到的概念

- [[unity-procedural-mesh]]
- [[triangle-primitives]]
- [[culling]]
- [[rendering-pipeline]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2018/02/24/intro-to-procedural-geometry-part-2/
- 本地：`raw/articles/lindenreid.wordpress.com/2018-02-24_intro-to-procedural-geometry-part-2.md`
