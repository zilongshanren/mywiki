---
tags: [游戏引擎, 内存分配, 数据导向设计, bitsquid, cache]
date: 2026-04-19
sources: 1
---

# Arrays of Arrays：N 个动态容器共用一块大 buffer

N 个 entity 各挂一个**动态变长**的数据结构（如一组 tag、一段 buff 列表）——怎么把它们塞进**少数几块 buffer**而不是 N 次独立 `malloc`？[[niklas-frykholm|Niklas Frykholm]] 2015 年《Allocation Adventures 2》给出三条路线及优缺点，并预告续篇的 [[buddy-memory-allocation|buddy allocator]]——因为 `vector` 容量按 2 倍增长，buddy 天然契合。

## 问题

举例 `TagComponent`：每 entity 一组 `unsigned` tag（字符串 hash），需要存上千 entity 的 tag 列表。朴素实现 `std::vector<std::vector<unsigned>>` 每个内层 vector 自带一次独立 alloc——N entity 就 N 次 alloc，cache 散落、profile 难做。

## 路线 1：Fixed size 硬上限

`struct Tags { unsigned n; unsigned tags[MAX_TAGS]; }; Array<Tags>` 一条 buffer 装下全部。适用于：

- **问题天然有界**：2D 格子最多 4 邻居、skin mesh 每 vertex 最多 4 bone 权重；
- **当前项目的业务约定**：这游戏的 entity 最多 4 tag 够用；
- **引擎写给多游戏**则难：上限难设，设大了每 entity 浪费严重。

## 路线 2：Linked list + index 而非 pointer

`Array<Node> nodes`，`Node { tag; next; }`——所有 node 放进**一条 buffer**，`next` 改成 index。一次 alloc 搞定。

但单字段 node **50% 空间浪费**在 `next` 上。改成 **block node**：

```c
enum { MAX_TAGS_PER_NODE = 8 };
struct Node { unsigned n; unsigned tags[MAX_TAGS_PER_NODE]; unsigned next; };
```

node 满时**有效利用 80%**；但**短列表的浪费反而更糟**（3 tag 塞进 8 tag node = 30%）——`MAX_TAGS_PER_NODE` 是 cache 与浪费的拉锯参数。

### 按链排序让遍历线性化

单 buffer 里 `next` 仍可能跳到 buffer 任意位置——大 buffer 时 cache miss 再起。**技巧：把同一 next 链的 node 按顺序排到一起**：

```
--------------------------------------------------
| A1 --|--> A2 --|--> A3 | B | C1 --|--> C2 |
--------------------------------------------------
```

遍历链 = 线性访问，cache miss 消失。完整 `O(n log n)` sort 太贵，改成**增量 sort**——每次访问时顺手调几下；假设 access 频率 > mutation 频率，就能维持"大致有序"。作者建议 **two-way bubble sort**——对已近有序数据表现好。

### 侧注：nil 用 0 还是 UINT_MAX

作者从"`UINT_MAX` 作 nil"改到 **"0 作 nil"**——`memset(buffer, 0, ...)` 重置、`if (next)` 直接判、`unsigned → uint16_t` 类型切换仍安全。代价是 `nodes[0]` 留作哨兵、不能用。这个 idiom 后来在 ECS / handle table 设计里越来越常见。

## 路线 3：Custom allocator

把大 buffer 自己切块——前两种方案其实就是极简的定尺寸 allocator。"是不是在重写 malloc？"

作者反驳：**malloc 为通用而生**——处理未知大小、未知寿命、未知线程模式、未知碎片化行为，注定不能为任一场景做到最优。知道具体使用模式的 custom allocator 可以**更简单也更快**（[slab allocator](https://en.wikipedia.org/wiki/Slab_allocation) 是系统软件的经典代表）；而且集中在一处的 allocation 更好 profile 和优化。

TagComponent 的两条特性让 custom allocator 格外可行：

- **所有 pointer 内部管辖**——没有外部指针指向它的内存块，**可任意搬、不怕碎片**；
- **`vector` 容量按 2 倍增长**——这就是 `push_back` 摊还 O(1) 的原因：`O(n)` 的 realloc 摊在 `n` 次 push 上得 O(1)。**既然所有 allocation 都是 2 的幂，[[buddy-memory-allocation|buddy allocator]] 天然契合。**

## 话外：C++ 抽象与"hackable 代码"

作者自黑第一轮 SoA 代码：

```c
char *buf = allocate(cap * (sizeof(unsigned) + sizeof(DataType) + sizeof(Value)));
keys = (unsigned *)buf;
types = (DataType *)(keys + cap);
values = (Value *)(types + cap);
```

评论者指出：样板代码到处抄、对齐处理麻烦、不如封装成模板 `multivector`。作者承认是样板 bug-prone，**但透明、可审、可改**——"今天要跳过初始化，明天要 serialize，后天要复用 slot..."，宁可保留 "hackable"。他梦想的语言是 **"C + 小而简单的模板引擎"**——C++ 的 template 对他太复杂。还举了 `std::vector<char>` 每次 resize 初始化 char 造成显著 perf 损失的真实故事——**抽象太深以至于要读汇编才敢相信编译器做对了**。

## 相关

- [[datacomponent-single-buffer-allocation]] — Part 1：单 component 的八步压缩
- [[buddy-memory-allocation]] — 路线 3 的续篇给出的 allocator 选型
- [[linear-allocator]]
- [[custom-allocator-interface]] — Bitsquid Allocator 抽象接口
- [[aos-vs-soa]] — SoA 在 memory-bound 下的经验优势
- [[cache-friendliness]]
- [[bitsquid-data-oriented-entity-system]] — component manager 内部布局
- [[handle-based-resource-manager]] — 同类"内部管指针、对外发 handle"原则

## Sources

- [[sources/bitsquid-allocation-adventures-2-arrays]]
