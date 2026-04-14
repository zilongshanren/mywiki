---
tags: [data-structures, performance, algorithms, c-sharp, cpp]
date: 2026-04-14
sources: 1
---

# Swap-and-pop 无序删除

「从数组中间删一个元素」这条操作在大多数语言的标准容器里代价是 `O(n)`，因为语义要求保留剩余元素的相对顺序——被删索引之后的所有元素必须整体前移一格。`List<T>.RemoveAt` 的 MSDN 文档原话很直白：「剩余项会被重新编号以替换被移除的项」。对于不关心顺序的场景，这个代价完全是白付的。

替代做法只有两行：把被删位置换成数组末尾的值，再把末尾 pop 掉。C# 扩展方法：

```csharp
public static void RemoveUnorderedAt<T>(this List<T> list, int index)
{
    list[index] = list[list.Count - 1];
    list.RemoveAt(list.Count - 1);
}
```

末尾删除是 `O(1)`（只是把 `Count--`），于是整体从 `O(n)` 降到 `O(1)`。Steven Sell 在写基于 [Fast Poisson Disk Sampling in Arbitrary Dimensions] 的蓝噪采样器时栽进这个坑：蓝噪生成过程正是「随机选一个活动点，消费后移除」，对一百万元素的列表跑一遍彻底清空：

| 列表大小 | `List.RemoveAt` | `RemoveUnorderedAt` |
|---|---|---|
| 1,000 | 0.03 ms | 0.008 ms |
| 10,000 | 1.57 ms | 0.08 ms |
| 100,000 | 240 ms | 0.64 ms |
| 1,000,000 | 75,223 ms | 9.74 ms |

百万级别是 99.987% 的运行时削减。这不是微优化——`O(n²)` 和 `O(n)` 的渐近差在这里直接把一分多钟变成十毫秒，甚至会决定某种算法「能不能跑」。

同样的 idiom 在 C++ 里更常见，`erase_unordered` 的标准写法：

```cpp
template<class T>
void erase_unordered(std::vector<T>& a, unsigned int index) {
    a[index] = a.back();
    a.pop_back();
}
```

Robert Bridson 的 curl noise 源码和很多模拟代码里都能看到这个套路。语义上，代价是**失去稳定性**——被删点之后有一次额外的元素位置变动，如果外部还有索引指向被 swap 过来的那个元素，它们会指错。因此它只适用于「索引不跨操作持有」的场景，比如遍历待处理集合、随机挑一个处理掉的那类算法。和 [[poisson-disk-sampling]] 这种「active list 随机消费」的模式是天作之合，和需要保持顺序的 UI 列表、时序队列则是正交的。

更一般地，这体现了一种常见的「语义-性能 tradeoff」：数据结构提供的保证越强（顺序稳定、迭代器有效、O(log n) 查找），越贵；放弃你用不上的那部分保证通常能一下把代价削掉一个数量级。这和 [[cache-friendliness]]、[[aos-vs-soa]] 是同一条思路——对齐使用模式和数据布局。

## Sources

- [[sources/vertexfragment-list-removal]]
