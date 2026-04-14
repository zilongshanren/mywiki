---
tags: [source, programming-languages, performance, c-sharp, data-structures, algorithms]
date: 2026-04-14
sources: 1
---

# C# List Removal Performance（Steven Sell / Vertex Fragment）

[[steven-sell]] 2021 年 10 月写的一篇短 ramble，记录他在实现 Bridson 的快速蓝噪 Poisson disk 采样时遇到的 `List<T>.RemoveAt` 性能陷阱，以及用 swap-and-pop 彻底消除这个陷阱的办法。

## 摘要

算法里要反复「随机挑一个 active point，消费后从列表里删掉」。直接调用 `List<T>.RemoveAt` 会触发整体前移（.NET 文档原话：「剩余项会被重新编号以替换被移除的项」），每次删除 `O(n)`，清空整个列表就是 `O(n²)`。作者给出的扩展方法 `RemoveUnorderedAt` 做的事只有两步：把被删位置换成 `list[Count - 1]` 的值，再 `RemoveAt(Count - 1)`——对 `List<T>` 来说末尾删除只需把 Count 减一，是 `O(1)`。他给出的基准测试从 1000 到 1,000,000 元素逐级加，百万级时 `RemoveAt` 耗 75223 ms，`RemoveUnorderedAt` 只要 9.74 ms，削减 99.987%。作者自嘲这不是什么新颖发明，Bridson curl noise 配套源码里的 `util.h` 就给了同款模板 `erase_unordered(std::vector<T>&, unsigned int)`。

## 关键要点

- `List<T>.RemoveAt` 的语义是保持顺序，代价是 `O(n)`，对随机删除场景这是白白浪费
- swap-and-pop 把问题降到 `O(1)`，百万级时差异直接变成「能跑 vs 不能跑」
- 前提是不关心顺序，也不能有外部索引指着被 swap 上来的元素
- 模式在 C++ STL 社区更常见（`erase_unordered`），C# 里反而少见
- 和 [[poisson-disk-sampling]] 的 active list 消费模式是天作之合

## 链接到的概念

- [[swap-and-pop-removal]]
- [[poisson-disk-sampling]]
- [[cache-friendliness]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/list-removal-performance/
- 本地：`raw/articles/vertexfragment.com/2021-10-18_c-list-removal-performance.md`
