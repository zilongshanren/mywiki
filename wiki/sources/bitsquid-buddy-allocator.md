---
tags: [source, bitsquid, allocator, 内存分配]
date: 2026-04-19
sources: 1
---

# Allocation Adventures 3: The Buddy Allocator（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2015 年 8 月 Allocation Adventures 系列的第三篇，把前两篇导出来的 buddy allocator 从概念一路压到**可实现的工程细节**——这是 [[buddy-memory-allocation|buddy 基础思路]]之后真正动手写 allocator 的人该读的那篇。

## 摘要

文章分三段。前半段是 allocator 通用语境：fragmentation 的两种形态（external 由空洞造成、internal 由 rounding 造成）、in-place linked list / preamble / postamble 三件套、`free(void*)` vs `free(void*, size_t)` 接口之争、preamble 带来的对齐和尺寸污染。中段展开 buddy 的核心算法：按 2 的幂递归切分，free 时查 buddy 是否 free，若是则递归合并。后半段是实现要点。

关键的工程压榨有几处。**Block index 公式** `(1<<level) + index_in_level - 1` 把整棵树扁平化到一维索引，便于存元数据。**合并位压到半 bit**：每对 buddy 只存 `is_A_free XOR is_B_free`，因为 free 时至少一个已知为 free，XOR 位足以推出另一个——总开销 `1 / 16 / leaf_size`。**split 位也是半 bit**：对已分配块反查 level，只要知道某个层级上的节点"被切过没有"即可倒推，配合 `free(void*)` 不要求 caller 传 size。**两张 bitmap 合起来 1 bit/block**。最后讲 metadata 本身放 buffer 头部、非 2-幂 buffer（比如 400K）用"预占前 144K"的方式适配——这些都是把 buddy 从教科书图示推到能上生产的坐标系对齐细节。

## 关键要点

- `free(void*, size_t)` 接口才是 allocator 作者的乐园，但 C/C++ 的现实是必须支持 `free(void*)`，因此需要额外 bookkeeping。
- 分配/释放的主数据只有两件：每层的**自由块 in-place linked list**、每对 buddy 的**合并 XOR bit**。
- 用 **split bitmap** 存"某层某节点被切过"代替 preamble 存 size，总开销 1 bit / block、`free(void*)` 的 size 查询只是小循环。
- **metadata 放 buffer 内部**是可行的——把前几个 leaf block 标记为 allocated 即可；注意 metadata 自身的分配要特判，避免 chicken-and-egg。
- 非 2-幂 buffer 用**"把不足的部分标为已占"** 方式适配，usable memory 从 buffer 头对齐，边界需要小心不要写到不可用内存。
- Buddy 天生适合**动态增长容器**（vector 2 倍扩容）——升级即"释放旧块 + 要更大 2 幂块"，几乎消灭 internal fragmentation。

## 链接到的概念

- [[buddy-memory-allocation]]
- [[arrays-of-arrays-allocation]]
- [[linear-allocator]]
- [[custom-allocator-interface]]
- [[a-metric-for-memory-fragmentation]]
- [[virtual-memory]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/08/allocation-adventures-3-buddy-allocator.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-08-04_allocation-adventures-3-the-buddy-allocator.md`
