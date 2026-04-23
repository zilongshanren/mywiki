---
tags: [source, 游戏引擎, 内存分配, 数据导向设计, bitsquid, buddy-allocator]
date: 2026-04-19
sources: 1
---

# Allocation Adventures 2: Arrays of Arrays（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2015 年 6 月 22 日续篇，把 Part 1 遗留的"怎么高效存 `vector<vector<T>>`"压到更干净的问题：用 **TagComponent** 为例——每个 entity 一组 tag（string hash `unsigned`），要存上千 entity 的 tag 列表而**不要**为每个 entity 单独 allocate。

## 摘要

先列三类可行方案，再指向续篇要写的 [[buddy-memory-allocation|buddy allocator]]。

**Fixed size.** 如果能接受硬上限（`MAX_TAGS=8`），整组数据就是 `Array<Tags>`——一条 buffer 装下全部。适用场景包括"问题天然有界"（2D 格子最多 4 邻居）、"经验共识"（vertex 最多 4 块 bone skin）、或"按当前项目约定"。引擎写给多游戏用就难设硬上限；上限太大则浪费严重。

**Linked list.** `struct Tag { tag; Tag*; }` 看似 cache 反模式，但**把 node 放进一个 buffer 里、`next` 改成 index** 就只有一次 alloc。单字段 node 浪费一半空间在 `next` 上；做成 **block node**（`n; tags[8]; next;`）可把有效利用率推到 80%，但短列表的浪费反而更糟——`MAX_TAGS_PER_NODE` 是 cache 友好与浪费的拉锯。作者还给出一条漂亮的优化：**按 next 链把同一链条的 node 排到一起**——遍历就变成线性 access、cache miss 消失。完全排序太贵，改成 **增量式排序**——每次访问时顺手调几下，假设访问频率 > mutation 频率就能维持"大致有序"，双向 bubble sort 之类适合已近有序的算法足够。侧注：作者已从"`UINT_MAX` 作 nil"改用 **0 作 nil**——memset 清零、`if (next)` 直接判、类型切换也安全，代价是 `nodes[0]` 留作哨兵。

**Custom allocator.** 把大 buffer 切小块——前两种方案其实就是最简单的定尺寸 allocator。"是不是在重写 malloc？"作者反驳：知道了具体使用模式就能写得比通用 malloc 更简单更快（[slab allocator](https://en.wikipedia.org/wiki/Slab_allocation) 是此原则的系统软件代表）；而且集中在一处的 allocation 更好 profile 和优化。

TagComponent 的两条特性让 custom allocator 格外可行：**(1)** 所有 pointer 是内部管辖——随时可搬，不怕碎片；**(2)** `vector`-style 动态数组的 capacity **按 2 倍增长**，这是"为什么 `push_back` 是 O(1) 摊还"——`O(n)` 的 realloc 摊在 `n` 次 push 上得 O(1)。既然总 allocation 大小都是 2 的幂，**buddy allocator** 正是为这种需求而生——下一篇就讲这个。

## 关键要点

- 问题：怎么存 `vector<vector<unsigned>>` 不让每个内层 vec 独占一次 alloc
- **Fixed size**：硬上限可行时最简（2D 邻居 4、skin bone 4）
- **Linked list**：node 放进一块 buffer、next 改 index——一次 alloc
  - 单 tag node 50% 浪费；block node（8 tag）80% 有效但短列表浪费
  - **按 next 链重排 node** → 遍历变线性 access，cache miss 消失
  - 不做完整 sort，改增量 sort（访问时顺手 bubble）
  - 侧记：nil 从 `UINT_MAX` 改 0——memset 友好、类型切换安全
- **Custom allocator**：知道使用模式比 malloc 更简单更快
- TagComponent 的两条特性
  - 所有 pointer 内部管——可搬，不怕碎片
  - dynamic array capacity 按 2 倍增长——为什么 push_back 摊还 O(1)
- 2 的幂 allocation → **buddy allocator** 天然契合（下篇）
- 作者自黑：`char* buf = allocate(...); keys=(unsigned*)buf; types=(...)(keys+cap); ...` 是 bug-prone 样板，但透明、可审、可改；"hackable" 优于"完美库类"
- C++ 抽象藏太深：曾因 `vector<char>` 每次 resize 初始化 char 造成显著 perf 损失

## 链接到的概念

- [[arrays-of-arrays-allocation]]
- [[buddy-memory-allocation]]
- [[datacomponent-single-buffer-allocation]]
- [[linear-allocator]]
- [[custom-allocator-interface]]
- [[aos-vs-soa]]
- [[cache-friendliness]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/06/allocation-adventures-2-arrays-of-arrays.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-06-22_allocation-adventures-2-arrays-of-arrays.md`
