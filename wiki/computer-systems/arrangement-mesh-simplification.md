---
tags: [计算几何, 网格简化, cgal, arrangement, delaunay, squatters]
date: 2026-04-19
sources: 1
---

# Arrangement 网格简化与 Squatter 搜索

把一张 2D arrangement（平面曲线排列，比如 X-Plane 地图里的道路 / 河流 / 海岸线段网络）简化掉冗余顶点，最自然的迭代就是：找一个度数为 2 的顶点 `q`，把与它相邻的两条边 `pq`、`qr` 合成一条 `pr`；按引入误差排优先级，贪心剥。真正的难点不是决定「要不要删 q」的误差度量，而是**正确判断 pr 是否会破坏拓扑**——三角形 `pqr` 内部或边界上有没有别的顶点、线段、岛屿挡路。[[ben-supnik|Supnik]] 在 2011 年 5 月的三篇系列里，把这个「squatter 搜索」问题从两套数据结构（arrangement 本身、constrained Delaunay triangulation）两个角度各写了一次。

## 简化条件与 squatter

给定 `pq`、`qr` 两条线段，可以合成 `pr` 的前提：

- `q` 的度数为 2（除了 `pq`、`qr` 没别的边）
- `pr` 不是 arrangement 里既有的边
- 若 `p, q, r` 不共线，则三角形 `pqr` 的内部（含 `p-r` 连线之间，但不含 `pq` / `qr` 上的点，按定义就没有）没有其他顶点 / 线段 / 孤立点

最后这条是「squatter 不能挡路」——任何蹲在 `pqr` 里的顶点或穿过的线段都会阻止合并。外加两种失败：有孤岛几何在 `pqr` 简化后会落到错误一侧；或者封闭的外部几何在 `pr` 处被切穿。

## 路径 A：放弃 zone 计算

Supnik 最早的实现是用 **arrangement zone 计算**——把 `pr` 当作一条候选边，让 CGAL 求它穿过的所有 face / edge / vertex。问题有两个：

1. **复杂度爆炸**。一个有 X 条边的简单多边形，最坏情况要做 O(X) 次 zone 计算，每次 zone 都要遍历多边形边界 → **O(N²)**。X-Plane 的数据恰好是「大量长多边形、边很小」，最糟糕的象限。
2. **结果不够**。zone 只告诉你 `pr` 会不会撞到现有几何；它**不会报告 `pqr` 内部的 hole**（孤岛 face），要另外单独迭代 hole。

## 路径 B：Delaunay 作空间索引

替代方案是把所有 arrangement 顶点塞进一个 **Delaunay 三角剖分**当空间索引（灵感来自 CGAL 的 `point_set_2`）。检查 squatter 时：

- 取三角形 `pqr` 的最小外接圆
- 在 Delaunay 里查圆内的点

Supnik 没直接用 CGAL 的 `point_set_2`——它的点查询是**栈式深搜**，数据量一大就爆栈。他自己写了一套等价的点集，迭代式实现。

实现另外几条细节：

- 他**不把之前被判定「阻塞」的顶点重新排队**。理论上应该加，但当前索引结构不好改。
- 他利用 CGAL 的 `merge_edge` 做合并——该 API 本意是合并共线曲线，但 Supnik 自己先保证了安全性。好处是**不拆不建 face**，face 上挂的数据保持稳定，省掉 hole-in-face 重定位的几何测试。
- 代价：`merge_edge` 要求两条 halfedge 方向可合成一条 x-单调曲线；方向反向的对就不能合，所以有些可简化的细节漏过。

## 路径 C：让 triangulation 自己当索引

第三篇把观察推到更干净的形态：如果已经有一个 **constrained Delaunay triangulation**——原 arrangement 的边被当成 triangulation 约束、没有自由顶点（所有三角化顶点都至少落在一条约束上），那么 squatter 搜索甚至不需要圆查询：

> 若三角形 `pqr` 内部或边上存在任一顶点 `X`，那么 `X` 必定是 `q` 在 triangulation 里的邻居（并且位于 `pq` 和 `pr` 之间的锐角侧）。

**搜索 q 的一圈邻居就够了**。理由：假设存在 `pqr` 内部的 `X` 不和 `q` 相邻——那么三角化过程一定会给 `X` 接一条边，否则只能是另一个更近的点 `Y` 夹在中间；而 `Y` 若存在，我们在 `Y` 这关就已经失败。即 triangulation 的邻接本身就是 squatter 的充分表达。

顺带好处：**删掉一个 squatter `X` 时，重新评估 `X` 的邻居很自然**——因为 `X` 阻塞的就是和它连边的 `q`，「解锁」关系天然在邻接里。

## 实现上的反向链接难题

如果 triangulation 的顶点和 arrangement 的顶点是**多对多**（triangulation 里有地形采样带进来的额外顶点、原 arrangement 有被简化掉的顶点），还要能从一个约束三角形的边反查到原 arrangement 的 halfedge。Supnik 的折中：**每条 poly-line（原边段序列）里至少保留一个度数 2 的中间顶点**。不留就可能出现「两顶点之间两条不同路径」这种多边对应，反向查询没法唯一。实际上大多数 poly-line 也不会全简化到两端点（那就塌成零长度了），所以这条约束成本不高。

## 为什么值得留一笔

Supnik 三篇串起来的教训不是「algorithm for mesh simplification」——教科书里 Garland–Heckbert QEM、Hoppe progressive mesh 更出名——而是**「用什么索引」这件事被正确选择后，正确性证明会自然落地**：

- zone 计算：拓扑查询 / O(N²) / 还漏 hole
- Delaunay 外置索引：圆查询 / O(log N) 但要维护第二份结构 / merge_edge 兜缺陷
- **Constrained triangulation 作索引**：邻居圈 / 证明自然 / 删除后的重新评估也是邻居圈

这是一条「把问题向数据结构投影」的典型路径——和 [[cgal-arrangement-import-antennas|CGAL arrangement 导入的 antenna 陷阱]] 是同一家 X-Plane 地图管线里的兄弟。

## 相关
- [[cgal-arrangement-import-antennas]]
- [[cgal-exact-arithmetic-mantissa-growth]]
- [[floating-point-geometric-predicates]]
- [[ben-supnik]]
- [[pn-triangle-polyline-bezier-fit]] —— 同样的「误差度量 + 优先队列贪婪合并」骨架，用在折线 → Bezier 化

## Sources

- [[sources/supnik-mesh-simplification-trilogy]]
