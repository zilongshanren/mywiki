---
tags: [bezier, computational-geometry, rendering, graphics]
date: 2026-04-19
sources: 2
---

# Bézier 曲线没有解析解的那些事

三次 Bézier 是图形世界最常见的参数曲线，但这个选择的代价被很多人忽略：**Bézier 的许多「自然」几何查询都没有闭式解**。[[ben-supnik]] 在 2011 年 8 月的抱怨贴里列出了让他反复吃亏的几条：

- **弧长无解析解**：弧长积分 ∫ |B'(t)| dt 是一个含二次多项式开方的积分，把人算哭也没有闭式表达。想「按等长把曲线分成两段」也跟着一起挂掉——不存在把 Bézier 在 `L/2` 处切开的解析 t 值。
- **两条曲线求交没有闭式解**。Supnik 提到网上有人声称找到了（truetex 的 bezint 页），但不公开算法。实际生产里只能用 subdivision + bbox 剪枝或隐式曲线消元。
- **两条不相交曲线的最近点对**也没有解析解。

唯一真正有解析解的是 **「曲线与水平/垂直线相交」**：把已知坐标代进 `B(t)` 得一个一元三次方程，用 Cardano 的三次公式求根即可——见 `xptools` 里 `CompGeomDefs2.h` 的代码。换句话说只有「轴对齐直线切 Bézier」落在 [[cubic-equation-solver-hlsl]] 这一档里还算便宜。

## 为什么这件事重要

这几条缺口决定了任何「自适应细分」「等弧长放置路径动画」「曲线数据简化」的算法都必须走**数值而非解析**路线：要么按参数 t 均匀采样（曲率大的地方自然密，见 [[bezier-curve-triangulation]]），要么按控制多边形长度做上界估计，要么像 Supnik 在 X-Plane 里把 OSM 道路数据做 Bézier 化时那样**用暴力搜索 + 误差度量**把两段合并成一段（见 [[pn-triangle-polyline-bezier-fit]]）。

这也解释了为什么 font hinting 之外的 Bézier 应用动辄要给「max error tolerance」一个参数——这不是工程师懒，是数学决定的。

## Sources

- [[sources/supnik-joys-of-bezier-curves]]
- [[sources/supnik-bezier-curve-optimization]]
