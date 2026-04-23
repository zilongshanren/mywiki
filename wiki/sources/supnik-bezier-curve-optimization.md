---
tags: [source, bezier, polyline, pn-triangles, x-plane, osm, graphics]
date: 2026-04-19
sources: 1
---

# Bezier Curve Optimization（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 9 月 3 日的长文，讲 X-Plane 10 把 OpenStreetMap 折线道路转成分段 Bézier 曲线的完整流水线。代码在 `xptools`：`NetPlacement.cpp`、`BezierApprox.cpp`。

## 摘要

X-Plane 10 的道路表示是「tagged points」的分段 Bézier（端点 + 最多两连控制点 = 线段/二次/三次）。OSM 输入是点密度极高的折线。问题分两步：**折线 → 分段 Bézier（先用 PN-Triangle 估切线）+ Bézier 简化（自底向上合并）**。第一步借鉴 ATI PN-Triangles：对每个顶点用入/出线段方向取平均得切线，控制点沿切线放置、距离决定凸出程度；为避免 bulge，Supnik 按「两边是否弯/直」分五种拐角情形单独处理。第二步跳过 Douglas-Peucker（忽略曲率），改用**邻两段 Bézier 合一**的二维标量搜索（两控制柄长度）+ 折线化方差误差度量（类 Hausdorff 但可排序），整条路按「误差最小先合并」的优先队列全局贪婪推进；合并误差始终对照最原始的多段 Bézier 计算，而非已合并结果。

## 关键要点

- 道路 Bézier = 线段 / 二次 / 三次 + tagged-point 表示
- PN-Triangles 切线估计从网格降维到一维折线
- 五种拐角处理：锐角保留、钝角保直、两弯、一弯一直、两直圆角
- 「直」判定靠「若全当圆弧其半径是否超阈值」
- 简化用自底向上合并 + 暴力搜索两控制柄长度
- 误差 = 折线化后的距离方差（非 Hausdorff 最大值）
- 始终对照原始 Bézier 算误差，防止多次合并漂移
- 不用 Douglas-Peucker——曲率信息在它那里丢失

## 链接到的概念

- [[pn-triangle-polyline-bezier-fit]]
- [[bezier-analytic-limitations]]
- [[bezier-curve-triangulation]]
- [[arrangement-mesh-simplification]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/09/bezier-curve-optimization.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-09-03_bezier-curve-optimization.md`
