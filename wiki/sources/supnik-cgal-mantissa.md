---
tags: [source, computational-geometry, cgal, exact-arithmetic, floating-point]
date: 2026-04-19
sources: 1
---

# CGAL: It's All About the Mantissa（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2010 年 4 月的博客文章，用 X-Plane 的 OSM 道路网处理讲 CGAL 无限精度代数在深层构造链下崩盘的真实案例。

## 摘要

CGAL 之所以能避免浮点几何常见的「平行线交点飘到几公里外」这类灾难，是因为它用动态分配大小的数字类型配合独立分子/分母来维持符号精确，尾数可以按需长到任意长。但这种精确性有隐性代价：每一次在 CGAL 构造结果上再做一次构造，尾数长度都会累加，到了一定深度算法不会出错而是会变得「惊人地慢」。Supnik 把 OSM 原始数据合并成整体地图时，交点已经是高位尾数；再在这些长尾数点上按街区计算人行道偏移，尾数继续膨胀，整个圣地亚哥的人行道生成需要 36 分钟。修复极其直接：在第二阶段入口把每个角点 round-trip 到 IEEE float64 再转回 CGAL，强制抛掉多余精度——float64 已给出亚毫米精度，对马路而言严重溢出。新管线用 67 秒跑完，近 32 倍加速。风险是 OSM 编辑冲突可能产出 <1mm 的真小街区，此时截断会把它翻面退化；工程化时必须加 sanity check，通常小于阈值直接丢掉即可。

## 关键要点

- 符号精确算术成本随构造深度累积，不会报错只会变慢
- 周期性 round-trip 到 float 是一种简单有效的精度重置
- 精度重置只对「物理上没意义的过度精度」安全，必须配 sanity check
- 选择精度的依据来自问题域（道路 ~1mm 足够），不是算法本身

## 链接到的概念

- [[cgal-exact-arithmetic-mantissa-growth]]
- [[huge-world-coordinate-precision]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/04/cgal-its-all-about-mantissa.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-04-23_cgal-it-s-all-about-the-mantissa.md`
