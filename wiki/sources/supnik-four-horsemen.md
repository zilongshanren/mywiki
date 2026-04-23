---
tags: [source, performance, 方法论, 架构, 复利]
date: 2026-04-19
sources: 1
---

# The Four Horsemen of the Performance Apocalypse（Ben Supnik）

[[ben-supnik]] 2015-01-31 发表，是 [[supnik-performance-by-design|上一篇立场帖]]的续篇。

## 摘要

作者承接上篇的主张——"性能是设计出来的"——在这篇里把"为什么不是"拆成四条具体机制。前置限定：不是所有代码都配得上这标准，对话框打开 30 ms 他不在乎；他关心的是核心路径——启动时间、编辑器响应、滚动平滑、游戏里能撑多大世界。四骑士分别是：**冗余工作**（大 O + 产品定义层面的浪费，如实时 shading vs 烘焙、整图铺房子 vs 只铺赛道附近）；**常数时间低效**（`std::map` / 虚函数 / `dynamic_cast` / cache-unfriendly 布局——作者指出 WED 代码库里 `std::map<string, ...>` 出现 588 次、`std::set<...>` 822 次，这不是 hot spot 是全局债）；**不必要的泛化**（用任意多边形交集算法去裁三角形、"通用 draw 任意三角形"函数、WorldEditor 因为不追脏区域所以整屏重绘——这是"简化抽象"的性能代价）；**复利**（前三条乘起来，三个 25% 的开销合起来就是 2×）。他以重新阅读 Knuth 原文作结：**Knuth 从没反对性能关注**，他要的是编译器自动反馈成本——但这不够，设计前要先估数据规模、选能在预算内跑的算法、只加付得起的抽象。

## 关键要点

- 四骑士：冗余工作 / 常数时间低效 / 不必要泛化 / 复利
- "超越大 O"的冗余——产品定义层面的浪费最贵
- `std::map<string>` 588 次 = 全局债不是 hot spot
- 复利解释了为什么 profile 救不了"uniformly slow code"
- 设计顺序：估规模 → 选算法 → 选 idiom → 加抽象（只加增值的）

## 链接到的概念

- [[four-horsemen-performance]]
- [[performance-by-design]]
- [[false-abstraction]]
- [[cheat-by-solving-less]]
- [[optimization-leverage-ratio]]
- [[stl-not-abstraction-prescription]]
- [[memory-latency-human-metaphor]]
- [[aos-vs-soa]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/01/the-four-horsemen-of-performance.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-01-31_the-four-horsemen-of-the-performance-apocalypse.md`
