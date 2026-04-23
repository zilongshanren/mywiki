---
tags: [source, 计算几何, 网格简化, cgal, arrangement, delaunay]
date: 2026-04-19
sources: 1
---

# Mesh Simplification 三部曲（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 5 月 26 日连发的三篇短文（Part I/II/III），讲 X-Plane 地图生成管线里怎么把一个 arrangement（平面曲线排列）迭代简化掉冗余顶点——核心是「squatter 搜索」怎么做最省。

## 摘要

给一张 arrangement，要把度数为 2 的顶点 `q` 配合它的两条邻边 `pq`、`qr` 合并成 `pr`，合法性的难点不在误差度量而在「squatter」——三角形 `pqr` 内部有没有别的顶点 / 线段 / 孤立点挡路。Supnik 先否掉基于 arrangement zone 计算的老实现（O(N²) 且漏 hole），换成把所有顶点塞进一个 **Delaunay 三角剖分**当空间索引，查三角形 `pqr` 外接圆内的点来判断 squatter。实现细节上他弃用 CGAL 的 `point_set_2`（栈式 DFS 爆栈）、用 `merge_edge` 替代 insert/remove 保持 face 稳定、但付出「方向反向的曲线对不能合」的限制。第三篇推进到更干净的形式：**如果已经有一个 constrained Delaunay triangulation**（原 arrangement 的边作为约束、没有自由顶点），那么 `pqr` 内的任意 squatter 必定是 `q` 在 triangulation 里的邻居——搜索只需圈一圈 `q` 的邻居，证明短且自然。额外工程约束：为了能从 triangulation 反查到原 arrangement 的 halfedge，poly-line 内部至少要保留一个中间顶点。

## 关键要点

- 核心问题不是「选哪个顶点删」而是「怎么快而正确地检查 squatter」
- 放弃 arrangement zone 计算：**O(N²) + 漏 hole**
- Delaunay 外置索引：三角形外接圆查询，自建点集替代 CGAL `point_set_2`（后者栈爆）
- `merge_edge` 替代 insert/remove：保 face 数据稳定，代价是 x-单调性约束导致反向曲线对合不了
- Constrained triangulation 作索引：**squatter 必为 `q` 邻居**，拓扑邻接就是索引
- 反查原 arrangement halfedge 需要保留 poly-line 中间顶点，以避免多路径歧义

## 链接到的概念

- [[arrangement-mesh-simplification]]
- [[cgal-arrangement-import-antennas]]
- [[ben-supnik]]

## 原文

- 链接（Part I）：http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-i-its-all.html
- 链接（Part II）：http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-i-arrangement.html
- 链接（Part III）：http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-iii.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-26_mesh-simplification-part-i-it-s-all-about-squatters.md`
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-26_mesh-simplification-part-ii-arrangement-simplification.md`
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-26_mesh-simplification-part-iii-simplifying-a-triangulation.md`
