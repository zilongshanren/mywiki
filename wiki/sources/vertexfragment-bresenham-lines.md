---
tags: [source, rendering, rasterization, algorithms]
date: 2026-04-14
sources: 1
---

# Bresenham Lines（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 1 月的 ramble，面向“想在 tile 网格上画整数直线”的读者，重新讲清楚 Bresenham 算法的由来、原理与适用场景。

## 摘要

文章先铺陈历史背景：Bresenham 直线算法诞生于 1962 年，彼时 PC 尚无实时渲染概念，一幅图的绘制以秒/分钟计。这种只用整数加减的算法在汇编实现下极快，后来被 1992 年的 Xiaolin Wu 反走样算法部分取代，但当需求只是“整数网格上一条简单直线”时它依然是最佳选择。作者然后用起点终点、dx/dy、主次轴和 `error` 变量把核心思想讲透——每步必沿主轴走一格，次轴是否前进由 `error` 决定，直观含义是“下一个次轴格子是否已经比当前更接近理想直线”。最后他给出了自己使用它的动机：他正在开发的 roguelike 项目 Realms 需要在 tile 网格上定义“对角移动距离”“远程火球落点”这类整数路径，Bresenham 恰好提供了 Dungeon Crawl Stone Soup 等同类作品长期依赖的那种可预测整数直线。

## 关键要点

- Bresenham 是 1962 年的纯整数直线算法，靠 `error` 累积值决定何时沿次轴前进
- 每一步都沿主轴前进一格，总步数 = 主轴增量 + 1，循环体只做整数加减与一次比较
- 原始实现通过起终点 swap 把代码压缩到只需处理四个八分圆，这个优化在需要可变长度时会变成障碍
- 现代用途仍然成立：tile-grid 游戏（roguelike）中的对角移动、射线投射、视野判定
- Xiaolin Wu 1992 年的算法提供反走样直线，但更慢，不适合“整数、快速、无抗锯齿”场景
- 文章是后续 Variable Length Bresenham 一文的前置铺垫

## 链接到的概念

- [[bresenham-lines]]
- [[variable-length-bresenham]]
- [[rasterization]]
- [[steven-sell]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/bresenham-lines/
- 本地：`raw/articles/vertexfragment.com/2019-01-17_bresenham-lines.md`
- 参考：Abrash, *Graphics Programming Black Book*, ch. 35
