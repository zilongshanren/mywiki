---
tags: [cgal, computational-geometry, arrangement, rendering]
date: 2026-04-19
sources: 1
---

# CGAL merge_edge 的方向缓存陷阱

[[ben-supnik]] 2008 年写过 X-Plane 的 CGAL arrangement 导入在 `merge_edge` 上踩过的坑：**如果两条被合并的 half-edge 方向相反，CGAL 会给你一个自相矛盾的结果**。2011-08-29 的续集是：到 CGAL 3.4，这个问题可以被绕过，只要你格外小心。

## 问题根源

CGAL 的 half-edge 数据结构**缓存**了每条 half-edge 的方向（direction），目的是加速 sweep-line 等算法。但 `merge_edge(h1, h2)` 只替换 h1 指向的底层 curve，不会主动重算方向缓存。当新 curve 的实际方向和 h1 的缓存方向不一致时，后续任何依赖这个缓存的查询都会陷入混乱。

## 解决方法

工作区在于**利用 merge_edge 的副作用次序**：调用 `merge_edge(h1, h2, curve)` 会保留 h1 及其 twin、删除 h2 及其 twin（前提是 `h1.target == h2.source`，并且这个公共顶点就是要消除的那个）。由此：

- **若 h1 方向与新 curve 一致**：直接 `merge_edge(h1, h2, curve)`。
- **若 h1 方向与 curve 相反**：由于 h1、h2 不能同向（同向 half-edge 合起来不会产生反向合成曲线），此时 h2 与 curve 同向 → h2 的 twin 与 curve **反向**同步。改调 `merge_edge(h2.twin, h1.twin, curve.reverse())`，保留的就是 h2.twin（方向正确）这一条，结果缓存一致。

## 为什么仍然脆弱

这类 bug 是典型的**隐藏状态 vs 客户契约不匹配**：CGAL 的抽象承诺「拿 half-edge 操作曲线」，但性能优化要求缓存派生状态；用户只能通过阅读源码或撞 bug 才知道这层契约。Supnik 在 [[cgal-arrangement-import-antennas]] 与 [[cgal-exact-arithmetic-mantissa-growth]] 里一再回到同一主题：**CGAL 的正确性强大但边角案例极多，工程上只能通过大量 in-tree 断言和 adapter 来把它驯化成可生产使用的工具**。

## Sources

- [[sources/supnik-merge-edge-fixed]]
