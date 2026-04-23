---
tags: [性能, 优化, profiler, X-Plane]
date: 2026-04-19
sources: 1
---

# 优化杠杆率（Leverage Ratio）

[[ben-supnik|Supnik]] 用一个朴素的名字封装了 [[amdahls-law|Amdahl 定律]]在工程实操里最直接的意义：**每段代码的「杠杆率」就是它占总时间的比例**。一段占帧时间 20% 的代码，哪怕你把它优化到 0，全局只省下 20%；一段占 2% 的代码，全部消灭也只省 2%。

## 1% 何时算多

1% 本身不重要，**1% × 杠杆率**才重要。Supnik 给了两类判断：

1. **高杠杆情况下 1% 值得追**。X-Plane 9.62 的 Shark profile 里，`glDrawElements` 占 35.6%，那是一个已经被 Shark 砸过多年的成熟应用里的「鲸鱼级」杠杆。这种地方 1% 的改进会立刻在整帧 FPS 上体现出来。
2. **低杠杆情况下，只有可复制的优化才值得追**。`glBegin` 在那份 profile 里占 2%，散落在遍地遗留代码里——一次 99% 的优化也只换来不到 2% 的帧率，而且要改动量巨大。但如果一类优化可以**在几十处反复套用**，累积起来也可能达到高杠杆结构性改动的级别（比如每次 shader 优化 1%，十个 shader 就是 10%）。

## 从 profile 读杠杆率

Shark 这类 adaptive sampling profiler 的价值不是「告诉你哪里慢」，而是**把代码按杠杆率排序**。Supnik 推荐两个具体手法：

- **Timed Profile（All Thread States）**：必须把 blocking 时间算进来，否则你会漏掉 `glMapBufferARB` 这种「明明在等」的调用。对主线程受限 FPS 的应用，这是唯一正确模式。
- **同时看 L2 miss profile**：如果一个热点同时在时间和 L2 miss 榜上出现，说明它慢是因为等内存。X-Plane 的 quad-tree 占 12.9% 时间，L2 miss 榜也上榜——对应的优化方向就不是算法，而是布局（改分配模式 / 节点结构，提升局部性）。

另一个实用技巧：用 profiler 的 **data mining** 折叠掉 OpenGL 驱动的内部细节，先看「自己代码 vs 驱动」大盘；确定要追哪个驱动调用时再展开。

## 出乎意料的热点往往是 bug

X-Plane 的那份 profile 里，有一个「检查 3D mesh 是否需要处理」的例程排到第三（7.6%）——Supnik 当场说这几乎肯定是 bug。**优化的第二重意义：profiler 也是 bug 探测器**。一个不应该上榜的函数上榜了，意味着有非预期的调用路径——这比优化它本身更重要，因为你能同时省时间和修逻辑错误。

## 工程结论

不要问「这段代码能不能被优化」；要问「乘上杠杆率以后值不值得花这个小时」。这条原则跟 [[amdahls-law|Amdahl]] 的另一半——**make the common case fast**——是同一回事，只是把抽象公式换成了可以从 profile 直接读出来的数字。

## 相关

- [[amdahls-law]]
- [[cpu-performance-formula]]
- [[bottleneck-analysis]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-is-1-a-lot]]
