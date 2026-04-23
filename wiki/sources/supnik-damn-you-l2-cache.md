---
tags: [source, 计算机体系结构, 缓存, allocator, 性能, 启发式]
date: 2026-04-19
sources: 1
---

# Damn You, L2 Cache!!!（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 5 月 1 日的一篇优化惨败小记。他读完 Drepper 的 *What Every Programmer Should Know About Memory* 后想让 X-Plane quad-tree 的分配更 cache 友好，结果新 allocator 比原来的老策略更慢——被替换掉的隐式启发（allocation order ≈ draw order）其实已经把局部性吃满了。

## 摘要

X-Plane 的 quad-tree 剔除 profile 出来 hot spot 全是 L2 cache miss——CPU 不是算不动，而是等节点从主存来。Supnik 改 [[custom-allocator-interface|定制 allocator]] 让子树节点在内存里聚拢，预期提升局部性，实际更差。回头分析：老策略「按分配顺序排列」**刚好对齐了 X-Plane 的构建顺序→遍历顺序**，隐式形成了好的空间局部性；他的「按树拓扑聚拢」反而切断了这条链——因为遍历顺序被 frustum cull 和 LOD 打乱，不是拓扑序。结论：没有办法预先算最优布局，只能用启发式逼近；表面更系统的设计可能破坏意外成立的对齐。文末 Supnik 自嘲「回去喝苏格兰威士忌」——「人脑 0 : 复杂系统 1」。

## 关键要点

- cache miss 是 hot spot ≠ allocator 是对的手柄
- 隐式对齐（构建顺序 → 分配顺序 → 遍历顺序）胜过显式拓扑规划
- X-Plane 场景受第三方 scenery 影响，遍历顺序运行时才定 —— 无法预先最优
- 工程教训：**benchmarkable 才是真的，想得越久不如测一次**
- 与 ECS archetype 的对照：ECS 是把同样原理**显式化**，X-Plane 是意外收获

## 链接到的概念

- [[alloc-order-matches-draw-order]]
- [[cache-friendliness]]
- [[locality-principle]]
- [[memory-latency-human-metaphor]]
- [[custom-allocator-interface]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/damn-you-l2-cache.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-01_damn-you-l2-cache.md`
