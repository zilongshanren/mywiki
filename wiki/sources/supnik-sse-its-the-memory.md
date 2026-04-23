---
tags: [source, SIMD, SSE, 内存带宽, 性能, X-Plane]
date: 2026-04-19
sources: 1
---

# SSE? It's the Memory, Stupid（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2011 年 5 月 17 日的一条短札记：把 X-Plane 里基于网格索引的矩阵变换改成简单 SSE，吞吐涨 15%；改成更复杂、「避免 unaligned load」的版本，**加速消失**。

## 摘要

Shark profile 一看就知道第二版撞到了内存带宽墙——CPU 被数据喂不上，再多指令也只是在 load/store port 后面排队。标题点题：**SSE 的限制经常不是 SSE 本身，而是喂不上它的存储子系统**。这一条与 Supnik 同月 [[sources/supnik-damn-you-l2-cache|Damn You L2 Cache]] 互为印证——改 allocator 让 cache miss 更少、改 SIMD 让 load 指令更少，是两个方向的同一个问题：CPU 是否在等数据。遇到「更聪明的 SIMD 反而更慢」时第一反应应当是看 LLC miss 与 memory port 占用，而不是继续 tune 指令。

## 关键要点

- 简单 SSE 吃 compute-bound headroom，有 15% 收益
- 复杂 SSE 把 memory port 压饱 → 收益归零
- 判据：时间 profile 热点与 L2 miss profile 热点重叠 = memory-bound
- 解法方向：换数据布局 / 预取 / SoA，而不是再 tune intrinsics
- 与 [[alloc-order-matches-draw-order]] 互补：都在问「CPU 是不是在等数据」

## 链接到的概念

- [[simd-memory-bandwidth-bound]]
- [[bottleneck-analysis]]
- [[memory-hierarchy]]
- [[sse-tricks]]
- [[cache-friendliness]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/sse-its-memory-stupid.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-17_sse-it-s-the-memory-stupid.md`
