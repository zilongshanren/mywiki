---
tags: [计算机体系结构, 缓存, allocator, 启发式, 性能]
date: 2026-04-19
sources: 1
---

# 分配顺序 ≈ 绘制顺序：一个意外赢过精心设计的 allocator 启发

Ben Supnik 2011 年写过一篇「Damn You, L2 Cache!!!」的惨败小记——他读完 Ulrich Drepper 的 *What Every Programmer Should Know About Memory*，满腔热血想让 X-Plane 的 quad-tree 剔除变得 cache 友好。结果是：**他精心改写的 allocator 让性能变差，而被他替换的那个「凑合的」老方法才是最优**。

## 出发点

X-Plane 用一个 quad-tree 做场景图剔除。性能 profile 显示**这段代码的 hot spot 全是 L2 cache miss**——CPU 不是算不过来，而是等 quad-tree 节点从主存来。

这些节点来自一个 X-Plane 自研的 [[custom-allocator-interface|定制 allocator]]（针对「一批对象生命周期一致」「不需要线程安全」这类 system allocator 不知道的局部假设）。

Supnik 的计划：改 allocator，**让 quad-tree 节点在内存里聚拢**，提升局部性，cache miss 下来，帧率上去。

## 意外结果

新 allocator 更慢。

回头分析：**被他替换的老策略是「按分配顺序让节点紧挨排列」**。而在 X-Plane 里，quad-tree 节点的分配顺序**正好近似于后来的绘制/遍历顺序**——因为 scene-graph 的构建顺序就是按空间顺序进行的。所以「分配 = 遍历顺序」这条隐式的、没人特意设计的启发，其实已经把局部性吃到很好了。

他那套「按树的拓扑聚拢小子树」的新方案看起来更「系统」，但遍历顺序不是拓扑顺序——它是被 frustum cull + LOD 决策打乱过的、跟用户装的第三方 scenery 有关的顺序。**没有办法预先算出最优布局**，只能用启发式逼近。

## 工程教训

1. **profile 的 hot spot ≠ 优化的切入点**。Cache miss 是 hot，但 allocator 不一定是能动的手柄。
2. **「明显更好」的设计可能更差**。你改的不是一个孤立决策，而是整条访问路径的对齐情况。Supnik 原话：这是又一次「人脑 0 : 复杂系统 1」。
3. **隐式启发有时胜过显式设计**。分配顺序追踪构建顺序追踪遍历顺序——一条三跳的耦合，没有人设计它，但它自洽地把 [[locality-principle|空间局部性]] 做到了位。显式规划反而切断了这条链。
4. **benchmarkable 才是真的**。Supnik 承认自己的计划「表面上对 cache 更好」，但没真跑就信了自己。结论：**想得越久不如测一次**。

## 跟 ECS / data-oriented 的对照

ECS 的「按 archetype 连续排列 component」也是一种**把分配顺序和遍历顺序对齐**的做法——差别在 ECS 把这件事显式化、用 archetype group 强制执行。X-Plane 的 allocator 是隐式偶然对齐。两者的共同前提：**遍历模式相对稳定**。如果某天 X-Plane 的剔除算法改了，这个启发可能突然失效。

## 他的下一步

文末 Supnik 说「回去喝苏格兰威士忌」。没有后续 post 反驳这个结论——说明**老方法继续留在 X-Plane 里**。

## 相关

- [[cache-friendliness]]
- [[locality-principle]]
- [[memory-latency-human-metaphor]]
- [[memory-hierarchy]]
- [[custom-allocator-interface]]
- [[linear-allocator]]
- [[aos-vs-soa]]
- [[optimization-leverage-ratio]] —— Supnik 另一篇「1% 算多吗」的 profile 判断框架
- [[ben-supnik]]

## Sources

- [[sources/supnik-damn-you-l2-cache]]
