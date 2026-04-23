---
tags: [source, bitsquid, spatial-query, data-structure]
date: 2026-04-19
sources: 1
---

# Finding nearby stuff（Niklas Frykholm / Bitsquid, 2013-08-16）

[[niklas-frykholm]] 2013 年 8 月的博客，给出 Bitsquid 在"找附近点"问题上的默认工程方案：grid coord → HashMap → 扁平数组内嵌链表。

## 摘要

作者因合并 nav mesh 时需要找所有"足够近"的重复顶点而整理出这套思路。朴素双重循环 O(n²) 不可用；加速结构用**均匀网格**：把世界按 `cell_size` 切格，查询时只检查点所在 cell。最多需要看 2D 4 个、3D 8 个 cell（查询半径无论多小都有这个下界，除非加插入期复制到相邻 cell 的写多读少优化）。若查询半径固定，`cell_size = search_diameter` 让检查数稳定在 4。传统矩阵网格有范围/稀疏/越界三个痛点，换成 `HashMap<GridCoord, CellData>` 一次解决：按需分配、O(1)、无边界。cell 内容用 `Vector<T>` 会因大量微小集合堆分配 + cache miss 把性能打回去；作者的通用 C++ 规则是"不要在集合里放集合"，应当改成一个扁平 `Array<CellData>`，`CellData = {id, next}`，哈希表只存每个 cell 链表的头索引，用 `next == UINT_MAX` 终结。更复杂的场景（volume 查询、动态结构）再升级到 BVH、k-d、octree（可配 Morton + RLE）。

## 关键要点

- 均匀网格 + `cell_size = 查询直径` → 查询固定看 4 个 cell（2D）
- `HashMap<GridCoord, CellData>` 替代二维矩阵：稀疏友好、无范围假设
- cell 存**扁平数组内嵌链表**，不用 `Vector<T>`——省堆分配，locality 好
- 插入时写进 4 邻 cell 可让查询只看 1 个 cell，但代价 4× 插入/内存，仅在读多写少时划算
- 通用规则："高性能 C++ 避免 collection inside collection"

## 链接到的概念

- [[spatial-hash-grid-linked-list]]

## 原文

- 链接：https://bitsquid.blogspot.com/2013/08/finding-nearby-stuff.html
- 本地：`raw/articles/bitsquid.blogspot.com/2013-08-16_finding-nearby-stuff.md`
