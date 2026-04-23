---
tags: [source, cgal, arrangement, computational-geometry, half-edge]
date: 2026-04-19
sources: 1
---

# merge_edge - Fixed, Sort of.（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 8 月 29 日的 CGAL 后续贴。2008 年他写过 [X-Plane 在 CGAL 上的 merge_edge 坑](http://hacksoflife.blogspot.com/2008/10/cgla-abusing-mergeedge.html)——两条 half-edge 方向相反时合并会搞砸。2011 的更新是：CGAL 3.4 之后这个坑可以绕过，只要你格外小心。

## 摘要

CGAL 的 arrangement half-edge 结构**缓存了每条 half-edge 的方向**以加速 sweep-line 等算法。调用 `merge_edge(h1, h2, new_curve)` 只替换 curve 不刷新方向缓存。当新 curve 的实际方向和保留下来的 h1 缓存方向不一致时，后续查询就会错乱。Supnik 给出的绕法是**利用 merge_edge 保留 h1 / 删除 h2 这个固定副作用**：若 h1 方向与 new_curve 一致，直接合并；若反向，则合并 `h2.twin, h1.twin, curve.reverse()`，因为 h2 与 curve 必然反向同步，其 twin 与 curve 相反方向同步，把 twin 当主角合并就能让保留的 half-edge 方向缓存与 curve 一致。

## 关键要点

- CGAL half-edge 缓存方向信息
- `merge_edge` 不刷新该缓存
- merge_edge(h1, h2) 固定保留 h1/twin、删除 h2/twin（前提 h1.target == h2.source）
- 方向一致：直接合并 h1, h2
- 方向相反：合并 h2.twin, h1.twin, curve.reverse()
- 这是「绕过 CGAL 隐藏缓存」的典型 workaround，上下文是 X-Plane OSM import

## 链接到的概念

- [[cgal-halfedge-direction-cache-pitfall]]
- [[cgal-arrangement-import-antennas]]
- [[cgal-exact-arithmetic-mantissa-growth]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/08/mergeedge-fixed-sort-of.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-08-29_merge-edge-fixed-sort-of.md`
