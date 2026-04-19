---
tags: [source, 数据结构, C, 分配器]
date: 2026-04-19
sources: 1
---

# A Fast, Growable Array With Stable Pointers in C（Daniel Hooper）

[[daniel-chase-hooper]] 2025 年 8 月的文章，讲一个被多人独立发现、叫法各异的容器（[[segment-array|Segment Array]] / Segmented List / levelwise-allocated pile），同时做到常数时间随机访问、追加指针稳定、对 arena 友好，并给出 120 行单头文件实现与 10 条 x86 指令的 `sa_get`。

## 摘要

Segment Array 的结构是一个固定长度的指针数组，指向若干**按 2 的幂递增**的段。新增元素时按需分配下一段，已有数据永不搬迁，因此指针始终稳定；又因段大小是 2 的幂，`__builtin_clzll` 即可把「索引 → 段号 + 段内偏移」压成三五条指令，整个 `sa_get` 在 `-O3` 下是 10 条 x86-64。作者推导出 26 段的合理值（来自 48 位虚拟地址、uint32 索引、去掉最小的 6 段开销），容量接近 UINT32_MAX。对比固定数组 / 动态数组 / 分块链表 / 虚拟内存数组 / 混合方案等六种常见选择，Segment Array 的最大卖点是「追加期间指针稳定」× 「能塞进 arena 不留洞」——作者自己在构建可视化工具 *What The Fork* 里用它存数量未知的事件流。

## 关键要点

- 结构：`u8 *segments[26]` + `count` + `used_segments`；指针数组内嵌减少 cache miss
- 段数推导：48 位指针 → uint32 索引 → 去掉 6 个最小段 → 26 段 ≈ 4.29e9 items
- `log2i` = `8*sizeof(u64) - __builtin_clzll(x) - 1`，`sa_get` = 10 条 x86-64 指令
- 追加不搬迁意味着**指针稳定** + **arena 不留洞**，这是对 [[linear-allocator|arena 分配器]] 的关键价值
- Header 216 字节 vs 动态数组 24 字节——只适合全局中心容器，不适合小集合
- 变体：前两段同大小 → 总容量永远是 2 的幂，适合做 [[open-addressing-hashtable|open-addressing 哈希表]] 的后备
- 泛型：`union { SegmentArrayInternal internal; T *payload; }` + `typeof()` 宏，类型安全

## 链接到的概念

- [[segment-array]]
- [[linear-allocator]]
- [[open-addressing-hashtable]]
- [[data-structure-invariants]]

## 原文

- 链接：<https://danielchasehooper.com/posts/segment_array/>
- 本地：`raw/articles/danielchasehooper.com/2025-08-05_a-fast-growable-array-with-stable-pointers-in-c.md`
