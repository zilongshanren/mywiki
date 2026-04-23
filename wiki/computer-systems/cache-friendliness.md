---
tags: [计算机体系结构, 缓存, 性能]
date: 2026-04-05
sources: 2
---

# 缓存友好性（Cache Friendliness）

让代码的数据访问模式**和 CPU 缓存层次对齐**——是性能优化最容易被忽视的维度。

## 核心实践

1. **连续访问**：尽可能按连续内存地址访问。
2. **小热路径**：频繁运行的代码应该尽量紧凑，fit in L1。
3. **对齐**：结构体尺寸是 cache line（64 字节）的整数倍更好。
4. **分离冷热字段**：经常访问的字段放前面，少访问的放后面。
5. **SoA 布局**：按字段访问而非按对象。

## 反面例子

- 链表（或其他指针密集数据结构）的随机跳转。
- HashMap 在低局部性热路径上的使用。
- 多层嵌套 OOP 类（每次方法调用可能带着几次 cache miss）。

## 工具

- **perf** / **Intel VTune**：测量 cache miss 率。
- **Unity Profiler**：查找 managed heap 分配热点。
- **Data-oriented design 工具**：Burst 等。

## 与增长阶的关系

增长阶（[[order-of-growth]]）分析完全忽略 cache。在小 n 区间或 cache 友好的情况下，O(n) 可能胜过 O(log n)。**profiler 是真理**。

## 相关
- [[memory-hierarchy]]
- [[locality-principle]]
- [[aos-vs-soa]]
- [[order-of-growth]]
- [[texture-swizzle-nested-tiling]] —— GPU 纹理通过嵌套分块把空间相邻映射到地址相邻
- [[animation-stream-cache-layout]] — Bitsquid 动画流的 hot/cold 分离 + active 数组
- [[parameter-nodes-intrusive-linked-list]] — 池化数组 + intrusive 链表的 cache 友好变长结构
- [[memory-latency-human-metaphor]] —— 让 cache miss 的代价变直觉
- [[alloc-order-matches-draw-order]] —— Supnik 实测：精心规划的 cache 友好布局不一定赢

## Sources

- [[sources/caqa-day02]]
- [[sources/csapp-day01]]
