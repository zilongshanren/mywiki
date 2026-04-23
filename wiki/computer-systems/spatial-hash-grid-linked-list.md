---
tags: [spatial-query, hash-map, data-structure, linked-list, game-programming]
date: 2026-04-19
sources: 1
---

# 空间哈希网格 + 内嵌链表

"找附近的东西"是游戏编程高频需求：合并导航网格时要找所有距离 <ε 的重复顶点、找玩家附近的敌人、找哥布林附近的宝箱。朴素的双重循环是 O(n²)，量大时直接不可用。[[niklas-frykholm]] 在 *Finding nearby stuff* 里给出他的"标配"方案：**网格坐标 → 哈希表 → 数组内嵌链表**。

**网格坐标**。把空间按 `cell_size` 切格，查询时只看点所在的 cell。二维情形里最多需要看 4 个 cell、三维里 8 个——靠近网格交点时无论查询半径多小都逃不掉这个下界。若查询半径固定（比如顶点合并时），把 `cell_size` 取成**查询直径的 1.0 倍**，检查数就稳定在 4 个 cell。如果数据很稀疏，可以把 cell 取更大，平均查询 cell 数缓慢下降（1.5× → 2.78 个、3× → 1.78 个、10× → 1.21 个），但每个 cell 的面积和其中平均点数按平方增长——只在确认稀疏时才值得这么调。

还有一个加速技巧：**在插入时就把点写进相邻 4 个 cell**，这样查询只查 1 个 cell。代价是插入 4×、内存 4×。只在查询/插入比很高的场景划算；顶点合并这种"插一次查一次"显然不划算。

**哈希表而非矩阵**。传统二维矩阵必须预先知道范围、担心对角稀疏浪费空间、边界越界。把 `(int, int)` grid coord 做 key、cell 内容做 value 放进 `HashMap`，上述三个问题一次性消失：只给有数据的 cell 花内存，O(1) 查询，不用管范围边界。

**cell 内容不要用 `Vector<T>`**。`Vector<VertexId>` 在 cell 大多数只装几个元素时是严重浪费——每 cell 一次堆分配、pointer chasing、cache miss、集合嵌集合式的隐式拷贝。作者给出的通用规则："高性能 C++ 里避免把集合放进另一个集合。" 替代方案是一个扁平 `Array<CellData>`，`CellData = { id, next_index }`，哈希表里只存每个 cell 链表的**头节点**，通过 `next == UINT_MAX` 标记链表终结——本质是**把链表节点存进一块连续数组**（唯一理智的 linked list 实现）。这比 `Vector` 省堆分配、节点连续、cache 行为远好；代价是删除得扫一遍链表。

这个"grid coord → HashMap → 扁平 array 里的 linked list"三段式是作者的默认答案；更复杂的场景（体积交查点、体积交体积）才升级到 BVH、k-d tree、octree（配 [[morton-code|Morton code]] 与 RLE）。

## Sources

- [[sources/bitsquid-finding-nearby-stuff]]
