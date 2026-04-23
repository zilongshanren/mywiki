---
tags: [performance, 方法论, 架构, knuth, premature-optimization]
date: 2026-04-19
sources: 1
---

# 高性能是设计出来的，不是优化出来的

[[ben-supnik|Ben Supnik]] 2015 年初的立场帖。他原本准备写一篇"不要拿 Knuth 当借口糊弄代码然后靠 profile 去局部修修补补"的长文，但发现 Joshua Barczak 已经先写了一篇同题博客，于是自己改写成一句浓缩的口号：

> **High performance software is always high performance by design.**

## 核心论点

1. **Knuth 的原句不只被误引，在今天还是错的**。"premature optimization is the root of all evil" 常被当作"别管性能，先写完再说"的许可证。Supnik 的反命题是：*Premature design without analyzing the performance characteristics of the problem is the root of all evil.*
2. **性能的结构性因素在设计阶段就定死了**。X-Plane 里他自己引以为傲的每一个子系统，性能都是**从第一天就写在架构里**，不是后期调出来的。后期调的只是叶子。
3. **"profile 后再优化"不是错的——但只是必要条件不是充分条件**。评论里他自己澄清：没有 profile 的代码你甚至不知道它工作不工作；但光 profile 不足以拯救一个错误架构的系统。

## 与其它方法论的定位

和 [[strategic-programming]] 是同一立场：**前期投资换长期价值**，反对把性能当 tactical 补丁。在 [[pragmatic-performance-philosophy]] 里 Niklas Frykholm 提的"数量级驱动设计"（1 / 100 / 1000 / 10000 次/帧决定数据结构层级）是这个主张的具体操作化。

[[four-horsemen-performance]] 是 Supnik 自己紧接着这篇之后的续篇——把"为什么后期救不回来"拆成四个具体机制：**冗余工作、常数时间低效、不必要的泛化、复利叠加**。

## 手工调优也是必需的

评论区讨论澄清了一个误解：Supnik 并不是说"设计完就别 profile 了"。"Hand tuning"有两种含义——**按 profile 数据改内存布局**，以及**用更劳动密集的手段重写热点**（把热循环写成汇编）。两种都是正当的、也都是必要的。他反对的是"用 hand tuning 代替设计"，而不是"hand tuning 本身"。

## 相关

- [[four-horsemen-performance]]
- [[pragmatic-performance-philosophy]]
- [[strategic-programming]]
- [[tactical-programming]]
- [[optimization-leverage-ratio]]
- [[cheat-by-solving-less]]
- [[false-abstraction]]

## Sources

- [[sources/supnik-performance-by-design]]
