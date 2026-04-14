---
tags: [source, 数据结构, 哈希表, 性能, SIMD]
date: 2026-04-14
sources: 1
---

# Optimizing Open Addressing（Max Slater）

[[max-slater|Max Slater]] 2023 年 1 月的长 benchmark 文章，给出一条结论先行的经验法则：**你的默认哈希表应该是开放寻址 + Robin Hood 线性探测 + backward-shift 删除**；当内存宽松且要求确定性延迟时，two-way chaining 也是好选择。`std::unordered_map` 被定义成 C++ 标准库的历史失误。

## 摘要

文章用 64-bit → 64-bit 的 flat benchmark（8M entries、squirrel3 hash、2 的幂表大小、50/75/90% 装载因子），系统对比分离链式、朴素线性、带 tombstone 重建的线性、backward-shift 线性、二次探测、双哈希、Robin Hood（朴素 + backshift）、Two-Way Chaining（capacity 2/4/8）、以及 SIMD Two-Way 等 10 余种实现。每个表都报告 insert/erase/find、average/max probe、memory amplification 三组数字。总体结论是：**Robin Hood linear + backshift 在大多数场景胜出**——它的最大 probe 长度比二次探测、双哈希低一个量级，查询性能也几乎最好；two-way chaining 用更高内存换到几近常数的最大 probe。后半部分讲 CPU 级优化：unrolling 基本没用（硬件乱序已够），**软件 prefetch 把 find 从 30ns 降到 20ns**；SIMD 对 two-way chaining 真正有效，对线性探测则因平均 probe 太短而得不偿失。

## 关键要点

- **分离链式在 flat 时代过时**：所有「链式好处」都有 flat 替代方案（如 pointer-to-entry 双层实现稳定地址）。
- **Backward-shift 删除**是开放寻址的关键一环，能彻底干掉 tombstone。
- **Robin Hood 抢占**让探测长度分布极均匀——最大 probe 在 90% 装载下只有 58，朴素线性是 1604。
- **Double hashing 实测反而慢于二次探测**，因为它的探测序列跨越更多 cache line。
- **Two-way chaining**：两个 hash 分别指两桶，总取较空者；期望最大桶 $O(\log\log N)$，可以拿小常数封顶。
- **硬件已在帮你做 out-of-order execution**，手工 unrolling 不再有用；但 **software prefetching 对任何哈希表都有效**——特别是分离链式。
- **SIMD probe** 对 two-way chaining 非常合适（一桶刚好 cache line 对齐），对线性则 setup 开销吃掉收益。
- **2 的幂表**让索引用 `& (2^n - 1)` 代替 `%`，但要求 hash 函数本身质量好（不能直接扔掉高位导致退化）。

## 链接到的概念

- [[open-addressing-hashtable]]
- [[cache-friendliness]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Hashtables/
- 本地：`raw/articles/thenumb.at/2023-01-08_optimizing-open-addressing.md`
