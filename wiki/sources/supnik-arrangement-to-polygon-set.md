---
tags: [source, cgal, 计算几何, arrangement, polygon-set]
date: 2026-04-19
sources: 1
---

# How to Jam an Arrangement_2 into a General_polygon_set_2（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2013-03-14 的短文，记一次为 X-Plane 地图管线硬塞 `Arrangement_2` 给 `General_polygon_set_2`（GPS）时重复踩坑的过程。更气的是：他三年前自己写过同一个答案，今天搜出来才想起来。

## 摘要

标准 CGAL 流程是给 GPS 喂多边形、它内部自建 arrangement。但 Supnik 场景里 arrangement 已经由更上游几何管线生成且非常大，让 GPS 重建会丢拓扑 + 重跑几何测试，性能无法接受。他 sub-class GPS 拿直接访问口，代价是 arrangement 要预先带上 face 上的 containment 标记。直接塞会得到多边形含重复点——根因是 GPS 假设两个不变量：(1) 没有 antenna（CCB 上零宽尖刺），用 CGAL 自带的清理函数；(2) 每条 CCB 上所有 halfedge 的 underlying curve 方向一致。修 (2) 的策略：遍历所有 halfedge，只在"curve 方向与 halfedge 相反 **并且** halfedge 贴在内部 face 侧"时，翻转 curve 方向。删去 antenna 后这套规则能在所有 CCB 上一致成立。这是 CGAL 抽象与实现契约不匹配的又一个例子。

## 关键要点

- 保留 arrangement 的理由是性能：大 map 重建拓扑代价很大
- Sub-class GPS 要求 arrangement face 上附 containment 标记
- 两个不变量：无 antenna + CCB curve 方向一致
- 修方向的条件：(curve 与 halfedge 方向不符) AND (halfedge 在内部 face 侧) → 翻 curve
- CGAL 这条契约在文档里没明讲，只能通过 bug 发现
- Supnik 三年前已经解决过一次没记下来——自己的博客成了未来的答案书

## 链接到的概念

- [[cgal-arrangement-to-polygon-set-conversion]]
- [[cgal-arrangement-import-antennas]]
- [[cgal-halfedge-direction-cache-pitfall]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2013/03/how-to-jam-arrangement2-into.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-03-14_how-to-jam-an-arrangement-2-into-a-general-polygon-set-2.md`
