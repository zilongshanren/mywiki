---
tags: [SIMD, 性能, 缓存, 带宽, bottleneck]
date: 2026-04-19
sources: 1
---

# SIMD 优化被内存带宽吃掉的场景

SIMD 不是免费午餐——**CPU 挨饿时多宽的执行单元也没用**。[[ben-supnik|Supnik]] 2011 年在 X-Plane 上把网格索引矩阵变换从标量改 SSE，第一版「简单 SSE」获得 15% 吞吐，第二版「避免 unaligned load 的更复杂 SSE」把收益**打回原形**。Shark profile 显示更复杂的版本已经**撞到内存带宽墙**，执行单元在等数据。

## 判别信号

- 简单 SIMD 有小收益 → 说明还有 ALU headroom。
- 复杂 SIMD 的 L1/L2 miss 升高而总吞吐不升 → 工作负载进入 **memory-bound** 区段，更多指令只是在内存子系统后面排队。
- L2 profile 的热点与时间 profile 的热点**不重叠**时，通常还在 compute-bound；**重叠**时才是内存带宽问题。Supnik 在 [[supnik-damn-you-l2-cache|L2 cache 那次惨败]] 和 [[optimization-leverage-ratio|«1% 算多吗»]] 里都用过这条判据。

## 为什么「避免 unaligned load」的更聪明版本反而更差

unaligned load 在现代 x86（Nehalem 之后）已经很便宜——省下的那点周期不敌新增的 shuffle / 重拼数据带来的寄存器压力和 load/store 调度冲突。更重要的：**更多 load/store 引擎运转的代码反而让 memory port 更拥挤**，于是内存带宽先饱和。

## 工程结论

- 在 memory-bound 区域，**换数据布局**（[[aos-vs-soa|SoA]]、预取、合批）比**换更宽的指令**收益大得多。
- 决定是否继续向 SIMD 要性能之前，先看 L2/LLC miss rate——如果已经贴顶，下一步应该是 [[cache-friendliness|cache 优化]] 而不是 intrinsics。
- 这是 [[bottleneck-analysis|瓶颈分析]]「先识别瓶颈再动手」原则的反面教材：SSE 改完才测，白改了一版。

## 相关

- [[bottleneck-analysis]]
- [[memory-hierarchy]]
- [[cache-friendliness]]
- [[aos-vs-soa]]
- [[sse-tricks]]
- [[optimization-leverage-ratio]]
- [[alloc-order-matches-draw-order]] —— Supnik 另一次把 allocator 改 cache 友好反而更差
- [[ben-supnik]]

## Sources

- [[sources/supnik-sse-its-the-memory]]
