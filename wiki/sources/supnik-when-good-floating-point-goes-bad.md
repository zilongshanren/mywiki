---
tags: [source, 浮点, 几何, 鲁棒性, x-plane]
date: 2026-04-19
sources: 1
---

# When Good Floating Point Goes Bad?（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2010 年 9 月的短文，总结 X-Plane 里几何谓词在浮点下的典型失效模式。

## 摘要

X-Plane 内部的线性代数/几何例程几乎都归结到点积（dot product）——它是"点在线哪一侧"、"是否共线"、"线线相交"等一系列几何判断的核心。Supnik 列出四类浮点下会出问题的模式：（1）理论上应该为 0 的点积**永远不会精确归零**，"共线"检测必须引入 ε；（2）点在直线附近时**哪一侧的判断会抖动**，因为舍入误差的方向可以翻来覆去；（3）**输入顺序不对称**——用 AB 定义直线和用 BA 定义在微小尺度上给出不同的谓词结果，破坏算法不变量；（4）**线线求交是最危险的函数**，近乎平行时分母爆炸、结果可以"飞到火星上"，但不会自动报错。他的实战做法是先用点积筛出近共线情况走另一条代码路径，主求交算法只处理夹角足够的情形。

## 关键要点

- 几何谓词的"返回三态"（负/零/正）在浮点里只能有容差版本。
- 同一条直线方向反过来定义会破坏"左/右"的一致性——需要规范化输入。
- 线线求交的误差放大取决于夹角条件数，再好的算法都要容忍它。
- 靠上游规避（用点积做共线早筛）比靠下游鲁棒化（精确算术）便宜得多。
- 但 scenery importer 这类离线工具里必须上 [[cgal-exact-arithmetic-mantissa-growth|精确算术]]。

## 链接到的概念

- [[floating-point-geometric-predicates]]
- [[cgal-exact-arithmetic-mantissa-growth]]
- [[cgal-arrangement-import-antennas]]
- [[huge-world-coordinate-precision]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/09/when-good-floating-point-goes-bad.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-09-27_when-good-floating-point-goes-bad.md`
