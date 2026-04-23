---
tags: [软件设计, 抽象, C++, STL]
date: 2026-04-19
sources: 2
---

# STL 不是抽象，而是规定

[[ben-supnik|Ben Supnik]] 在 2010 年的一篇短文里抛出一个反直觉的论断：**STL 不是抽象，它只是 shortcut**。

他引用 Joel Spolsky 的「Leaky Abstractions」作为对照：抽象的本质是**隐藏实现**，好的抽象让你在不知道实现的情况下正确使用接口。按这个定义，STL 完全不符合——STL 不隐藏任何东西，它**精确地 prescribe**。

## vector 的「抽象」其实是什么

选择 `std::vector` 时，你实际上是在签署一份实现契约：

- 连续内存、紧凑表示；
- 随机访问极快；
- 元素拷贝构造会被触发无数次；
- `resize` 会让所有外部 iterator 失效；
- 头部和中段的插入/删除是灾难。

Supnik 的观点是：这些不是「抽象泄漏」，而是**合同的一部分**。你不是在选择一个「动态数组抽象」，你是在选择这一套性能与复数特征的组合。想要别的权衡？就换一个容器，比如 deque、list、map。

## 为什么这个「规定性」恰恰是好设计

评论区有读者补了一刀：在 C++ 里，运行时复杂度是首要关切。把 Big-O 特征**刻进接口本身**反而是正确设计——SQL 查询优化器是「抽象」（隐藏执行计划），所以它偶尔会坑你到要 DBA 去加索引；STL 则把代价提前摆在你面前。

这个立场和 [[false-abstraction]] 是同一硬币的两面：Ousterhout 警告「省略重要细节的抽象」是假抽象；Supnik 顺势说，如果接口必须暴露那些细节，那它干脆就别伪装成抽象。STL 做的正是这件事。

## 对库作者的启示

- 如果你的库里性能特征是用户做选型决策的关键，**显式把它写进接口名和文档**，而不是藏起来。
- 不要为了「通用」强行给所有容器套同一个 interface；concept / traits 层面的统一（iterator、algorithm）是值得的，但不要让用户以为选 map 还是 vector 不重要。
- 参考 [[abstraction]] 的定义：**省略不重要的细节**。对算法库而言，复杂度从来不是不重要的细节。

## Sources
- [[sources/supnik-stl-not-abstraction]]
- [[sources/supnik-more-stl-abstraction]]
