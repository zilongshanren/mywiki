---
tags: [计算机系统, 内存分配, allocator, 数据结构]
date: 2026-04-19
sources: 1
---

# Buddy Memory Allocation

**Buddy allocator** 在动态变长数据按 2 的幂增长时几乎是最契合的 allocator 设计——分配复杂度 O(log n)、释放时可**合并相邻 buddy**防碎片，内部分裂/合并逻辑简单到可徒手实现。[[niklas-frykholm|Niklas Frykholm]] 在[[arrays-of-arrays-allocation|《Allocation Adventures 2》]] 结尾把 `vector` 容量按 2 倍增长的事实和 buddy 对接——"既然所有 allocation 都是 2 的幂，这个 allocator 就是为此而生"。续篇原本要展开的是这个。

## 基本思路

把一整块大 buffer 视作大小 $2^N$ 的根节点，每次请求大小 $2^k$ 的块时：

1. 找一个未被使用的、大小 $\ge 2^k$ 的最小节点；
2. 若该节点大小 $> 2^k$，**递归对半切**直到大小 $= 2^k$——切出来的每一对就是"buddy"；
3. 返回其中一半；另一半留给未来分配。

释放时把块标为 free，**如果它的 buddy 也 free**，就合并回父节点；父节点也可能再与它的 buddy 合并，递归上去。于是 buddy allocator **天然避免碎片**——释放即合并。

## 为什么对"2 倍增长容器"特别合适

`std::vector`、Bitsquid `Array<T>` 等动态数组的实现默认按 2 倍扩容——这保证 `push_back` 摊还 O(1)（$O(n)$ 的 realloc 摊在 $n$ 次 push 上）。一个 `vector` 的整生命期里需要的 allocation 大小永远是 $2^0, 2^1, 2^2, \ldots$——buddy allocator 要给出的正是这种尺寸序列的高效管理。

一个由 N 个独立 dynamic vector 构成的 **"arrays of arrays"** 场景，用 buddy 管底层共享大 buffer 后，每个 vector 扩容基本就是 "还旧的 2 的幂块、要个更大的 2 的幂块"。相邻释放还能合并回连续空间——比通用 malloc 简单数量级。

## 和其他方案的关系

- [[linear-allocator]] / bump allocator：O(1) 分配，零合并——适合**同寿命批量释放**的场景（一帧的 scratch 内存）；
- slab allocator：为**固定大小对象**而生，分配 O(1) 不浪费；对变长不适用；
- 通用 `malloc`：要兼顾所有尺寸、所有寿命，必然在任一专门场景上次优；
- buddy：**专对"2 的幂尺寸、寿命自由"** 最优，分配 O(log n)、合并 O(log n)。

## 系统软件里的应用

Linux kernel 的 page allocator 就是 buddy——页大小都是 2 的幂的倍数。许多嵌入式和游戏 runtime 也用 buddy 做中等粒度的 subsystem allocator，配合上层 slab（固定尺寸小对象）和 linear（short-lived 大块）形成**三层 allocator**。

## 在 Bitsquid 语境里

Bitsquid 的 [[custom-allocator-interface|Allocator 抽象接口]] 允许每个子系统选自己的 allocator。按 Niklas 的行文，[[datacomponent-single-buffer-allocation|DataComponent]] 的内部 value buffer 用 bump + defrag 够用；更大范围的 **"多个 component 共享 buffer"** 才把 buddy 推上台面——续篇《Allocation Adventures 3》会展开（本 wave 未收录）。

## 相关

- [[arrays-of-arrays-allocation]] — 导出 buddy 的具体问题域
- [[linear-allocator]]
- [[bump-allocator-wasm-guest]]
- [[custom-allocator-interface]]
- [[page-granular-system-allocator]]
- [[a-metric-for-memory-fragmentation]]

## Sources

- [[sources/bitsquid-allocation-adventures-2-arrays]]
