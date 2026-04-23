---
tags: [source, bezier, computational-geometry, graphics]
date: 2026-04-19
sources: 1
---

# The Joys of Bezier Curves [NOT]（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 8 月 22 日的短文，一句抱怨开场：「能不能有人提醒我，为什么计算机图形里 Bézier 曲线是这么常见的参数曲线选择？」正文是他列出的 Bézier 不讨喜特性清单。

## 摘要

三次 Bézier 在图形学里广泛使用，但**大多数自然几何查询都没有闭式解**：弧长积分无解析解、两曲线求交无闭式（truetex 的 bezint 声称有但不公开）、两曲线最近点也没有、按弧长等分切一条 Bézier 的 t 值不可解析求。唯一算得上便宜的是「与水平/垂直直线求交」——代入已知坐标后解一元三次方程，用 Cardano 公式即可，X-Plane 的 `xptools` 里 `CompGeomDefs2.h` 就是这么干的。Supnik 的潜台词是：所有 Bézier 上层算法都只能走数值而非解析路线，这一点被很多讨论遗忘。

## 关键要点

- Bézier 弧长积分含二次多项式开方，无解析解
- 按弧长分段（等长切一半）也随之无解析解
- Bézier-Bézier 相交、最近点对都只能数值求解
- Bézier-水平/垂直线：代入后是三次方程，可用 Cardano 解析解
- xptools `CompGeomDefs2.h` 包含该三次求根代码
- 实际工程后果：见 [[pn-triangle-polyline-bezier-fit]] 为什么要用暴力搜索

## 链接到的概念

- [[bezier-analytic-limitations]]
- [[cubic-equation-solver-hlsl]]
- [[bezier-curve-triangulation]]
- [[pn-triangle-polyline-bezier-fit]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/08/joys-of-bezier-curves-not.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-08-22_the-joys-of-bezier-curves-not.md`
