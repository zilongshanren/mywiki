---
tags: [bezier, polyline, pn-triangles, road, x-plane, rendering]
date: 2026-04-19
sources: 1
---

# OSM 折线到分段 Bézier 的 PN-Triangle 化 + 自底向上合并

[[ben-supnik]] 在 X-Plane 10 里需要把 OpenStreetMap 的道路（原始为折线 polyline，每几米一个节点）转成**分段 Bézier 曲线**——X-Plane 的道路表示是「tagged points」：端点（非控制点）+ 最多两个连续控制点，对应线段、二次或三次 Bézier。核心代码在 `xptools` 的 `NetPlacement.cpp` 与 `BezierApprox.cpp`。

整个流水线分两步：**折线 → 分段 Bézier（点数未减）** + **Bézier 优化（减点）**。

## 第一步：PN-Triangle 启发式生成切线

借鉴 ATI 的 [PN-Triangles](http://alex.vlachos.com/graphics/CurvedPNTriangles.pdf)：网格顶点的切线可以由相邻线段方向做平均估计出来。对一维折线这个思路更简单——每个顶点的「平均方向」由入边、出边两条线段方向求平均，得到切线；Bézier 的控制点必须沿切线方向摆放（因为 Bézier 在端点处的切线方向就指向相邻控制点），然后控制点离端点的**距离**决定「凸出程度」。

但 PN-Triangle 风格会让曲线向凸包外**膨胀**（bulge）——在匝道上这是好事，在直道上会变成「道路向外拱起」。Supnik 为此引入**五种拐角情形**：

1. 极锐角：保持尖角，相信数据里的锐角就是真锐角。
2. 极钝角：保持直线，即使角度很小也不值得为了凑圆润而移动端点。
3. 两边都「弯」：正常 PN-triangle 切线。
4. 一边弯一边直：切线取自**直的那条**，消除直道端点的 bulge。
5. 两边都直但非共线：保留原点作为二次 Bézier 的控制点，在角内做圆角。

「直」的判定是：如果把这条线段当作某圆弧的一段，半径会大于一个常量阈值（各类道路不同），就认为它是直道加一个小拐弯，而不是大圆弧的一部分。

## 第二步：自底向上 Bézier 合并（不用 Douglas-Peucker）

第一步结束后，每个原始顶点附近都多出了 1-2 个控制点，点数比原始折线还多。需要**简化**，但 [[ramer-douglas-peucker|Douglas-Peucker]] 行不通——它丢弃的是「离直线近的点」，不考虑 Bézier 曲率信息。

Supnik 的解法是**两曲线合一**的暴力搜索：

- **参数化观察**：要用一段 Bézier 近似相邻两段 Bézier 的合并，新曲线两端的切线方向必须与原曲线一致 → 两个新控制点只能在原切线方向上「伸缩」。于是整个近似问题**只剩两个标量参数**：起点控制柄长、终点控制柄长。两步搜索（粗扫 + 在最小误差附近细化）就能找到近似最优。
- **误差度量**：把近似 Bézier 和两段原始 Bézier 都细分为折线（N 段），用一条折线上每点到另一条折线的最近距离的**方差**作为误差。和 [Hausdorff 距离](https://en.wikipedia.org/wiki/Hausdorff_distance) 的两个区别：(1) 方差不是最小值，不能像 min-dist 那样用 bbox 剪枝 → 需要设一个「超过此距离不看」的上限；(2) 方差依赖所有点，能给出较细粒度的排序，便于在多候选里挑最佳。
- **全路简化**：对折线上每个非端点节点都算一次「与两个邻居合并」的误差，按误差入优先队列；不断 pop 误差最小的合并、替换两段为一段、重算该位置左右两个新邻居的误差。**注意**：误差必须始终对照**最原始**的若干段 Bézier 算——合并的合并的合并必须记住自己代表的是 8 段原始曲线而不是 2 段已合并曲线。

这种**全局贪婪**的次序保证了误差最小的合并先发生，比 Douglas-Peucker 那种单侧阈值裁剪在 Bézier 世界里更合理。

## 沿用到的想法

这篇把 **PN-Triangles 的切线估计** 从三角网格降维到一维折线，再接到 **[[bezier-analytic-limitations]]** 的现实里——正因为 Bézier 的误差度量/弧长/交点都没有解析解，每一步都只能靠细分 + 数值搜索。对 X-Plane 这种「全球道路数据一次烘焙」的离线管线，CPU 暴力搜索不敏感；换到实时场景就得换策略。参考 [[bezier-curve-triangulation]] 看另一种用切线重建曲线的生产代码。

## Sources

- [[sources/supnik-bezier-curve-optimization]]
