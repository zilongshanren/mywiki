---
tags: [计算机体系结构, 缓存, 内存层次]
date: 2026-04-19
sources: 1
---

# 把内存延迟翻译成「人能感觉」的时间尺度

一个教学比喻：把 CPU 的一个时钟周期映射成人类的一秒，**各层存储的访问延迟就能用日常动作做类比**。Gustavo Duarte 的原文被 Ben Supnik 借来解释为什么 X-Plane 启动慢——操作系统已经拼命把磁盘伪装成快的了，但一旦让 OS 的工作变难（大量小文件 seek），就把这笔伪装的成本暴露出来。

## 比例尺

按 1 cycle = 1 second（约 3 GHz CPU）：

| 层 | 真实延迟 | 人类时间 | 动作 |
|---|---|---|---|
| L1 cache | ~0.3 ns | ~1 秒 | 东西在桌上，伸手拿 |
| L2 cache | ~1-3 ns | 几秒 | 在办公室书架上，起身走两步 |
| 主存（DRAM） | ~50-100 ns | 约一分钟 | 在楼下车库的架子上，顺便拿个零食 |
| 磁盘（机械） | ~10 ms 以上 | **走到加州再走回来** | —— |

Supnik 的脚注算过：一次 41 ms 的磁盘 seek，对一个 3 GHz CPU 相当于 **474 天**；要在这个时间里从美东走到加州来回，人每天得走 12 英里。磁盘 seek 慢得不是一个数量级的事，而是**数百个量级**。

## 为什么这个比喻有工程价值

1. **让 cache miss 的「痛」变直觉**。直接说「一次 cache miss 100 cycles」只有工程师能体会；说「起身去楼下书架拿」一听就是成本。
2. **解释 OS 的伪装边界**。操作系统通过 [[page-cache-the-affair-between-memory-and-files|page cache]]、预读、I/O 调度器把磁盘伪装成内存的延迟——但这份伪装**只在访问模式允许的前提下成立**。大量随机小文件 seek 会穿透伪装。
3. **指导存储布局策略**。X-Plane 的 scenery 包原本是「无数个小 text 文件」，DSF 提案把它们合成一个大文件，就是为了让 OS 在一次 seek 里把大块连续数据 dump 到 page cache——**一次加州之旅换几百个**。

## 跟 cache friendliness 的关系

比喻把**空间局部性**（[[locality-principle]]）的价值变得直观——连续访问不是「快一点」，而是「免去一次加州出差」。[[cache-friendliness]] 页里的 AoS vs SoA、cache line 对齐都可以用这套语言重讲：随机指针 chasing = 每个链表节点都得去一次车库。

## 它的局限

一对一的比喻掩盖了**并行**：现代 CPU 能同时发起多条 cache miss，用 [[gpu-latency-hiding|latency hiding]] 思路掩盖单条延迟。所以真实性能瓶颈不是「每次 miss 要一分钟」，而是「miss 的并发度有多高、prefetcher 能不能跟上」。比喻适合解释**为什么要关心**，但不适合直接作为优化依据。

## 相关

- [[memory-hierarchy]]
- [[locality-principle]]
- [[cache-friendliness]]
- [[alloc-order-matches-draw-order]] —— Supnik 实测：为 cache 精心设计的 allocator 反而不如「分配顺序 ≈ 绘制顺序」的老启发
- [[gpu-memory-hierarchy-latency]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-going-to-california]]
