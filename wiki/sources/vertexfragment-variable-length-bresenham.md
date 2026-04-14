---
tags: [source, rendering, rasterization, algorithms]
date: 2026-04-14
sources: 1
---

# Variable Length Bresenham Lines（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 2 月的后续 ramble，解决标准 [[bresenham-lines]] 在需要“从起点沿方向走固定距离”时的失效问题。

## 摘要

作者指出，标准 Bresenham 为了节省代码量使用了一个聪明的优化：通过起终点 swap，把所有方向的直线翻转成“自底向上”的四种八分圆之一再绘制。这在只关心最终像素集合时毫无问题，但在需要沿方向延伸可变距离的场景（射线投射、视野、roguelike 投射物）中会失败——swap 后绘制顺序可能从终点开始，`range` 参数一加上去，直线就会朝反方向延伸、越过起点跑向错误的一侧。解决方法很直接：去掉入口 swap，改为显式处理全部八个八分圆，让水平和垂直两个分支在主轴上迭代 `range` 步。令人意外的是，这个展开版本代码**反而更短**，因为现在只需对 `dx`/`dy` 取绝对值判断主轴，不必处理 swap 边界。更令人意外的是性能：在 Chrome v72 上 jsperf 实测，“反优化”的可变长度版本（48.7M ops/sec）比原始四八分圆版本（47.4M ops/sec）还略快——现代 CPU 的分支预测和乱序执行有时会奖励均匀、直白的代码结构。

## 关键要点

- 标准 Bresenham 的 swap 优化使直线有时从起点、有时从终点开始绘制
- 想要“从起点开始、沿方向走 `range` 步”必须先解除这个优化
- 显式处理 8 个八分圆后代码反而更短，因为取 `abs(dx/dy)` 就能判主轴
- `range = 0` 时退化为原本的“画到终点”行为，是标准实现的超集
- jsperf 结果：可变长度版本略快于原版，现代 CPU 不再奖赏当年那种手工压缩
- 这是现代工程实践中一个典型的“反优化胜出”案例

## 链接到的概念

- [[variable-length-bresenham]]
- [[bresenham-lines]]
- [[rasterization]]
- [[steven-sell]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/variable-length-bresenham-lines/
- 本地：`raw/articles/vertexfragment.com/2019-02-19_variable-length-bresenham-lines.md`
