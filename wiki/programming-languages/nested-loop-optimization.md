---
tags: [performance, optimization, benchmarking, c-sharp, dotnet, programming-folklore]
date: 2026-04-14
sources: 1
---

# 嵌套循环的性能迷思

"嵌套循环性能差所以应该拍扁成单层循环"是一条经久不衰的 code review 俗见。Sell 在这篇短文里用一个最简化的基准测试反驳了它：**同样的 N×N 次迭代，嵌套双循环往往比手动展平的单循环更快，LINQ 版本慢 6 倍。**

## 实验

三种实现，遍历一个 10000×10000 的坐标网格，执行一个极轻量的 `DoThing(x, y)`：

```csharp
// 嵌套版
for (int y = 0; y < dim; ++y)
    for (int x = 0; x < dim; ++x)
        operation(x, y);

// 单层版：用除法/取模还原坐标
int total = dim * dim;
for (int i = 0; i < total; ++i)
    operation(i % dim, i / dim);

// LINQ 版
var coords = from y in Enumerable.Range(0, dim)
             from x in Enumerable.Range(0, dim)
             select new { x, y };
foreach (var c in coords) operation(c.x, c.y);
```

在 .NET Core 3.1 下跑 10 次取均值（`iterations=10000`）：

| 方案 | 平均 ticks | 相对最快 |
|---|---|---|
| Nested | 4,153,902 | 100% |
| Single | 6,703,180 | 161% |
| LINQ | 26,875,268 | 647% |

嵌套循环**反而最快**。为什么？单层版每次循环都要做一次整数除法和取模来还原 `(x, y)`，而现代 CPU 上整数除法是最昂贵的整型指令之一（数十个 cycle）。嵌套版里内层的 `x` 只是 `++x` 递增，外层的 `y` 递增频率被 JIT/硬件完美隐藏在 branch prediction + loop pipelining 里，几乎零开销。LINQ 版则除了循环本身还要分配匿名对象、构造迭代器、走虚调用——慢到离谱是意料之中。

## 一般化的教训

文章的真正重点不是这三组数字，而是一句写给所有 code reviewer 的话：**先按可读性和可维护性写，等基准测试证明性能问题再优化**。"嵌套循环 = 慢"是一个把 Big-O 误当成常数因子的误传。两个嵌套循环的渐进复杂度是 O(N²)，手动展平后**仍然是 O(N²)**——渐进级没有变化，变化的只是常数项。把 code review 的论据建立在「因为它长得像 O(N²)」上是错的。

几条更一般的推论：

- **Big-O 和常数因子是两件事**：渐进相同时，哪个更快完全取决于现代硬件上的常数项：分支预测、缓存、指令延迟、寄存器压力，统统要让位于实测。
- **JIT/编译器很可能已经比你聪明**：直白的嵌套循环是编译器最容易 pattern match 的形态，loop unrolling、vectorization、bound check elimination 都依赖于"结构干净"。手动展平反而**破坏**了这些优化机会——这一点和 [[cache-friendliness|缓存亲和]]、[[latency-vs-throughput|延迟与吞吐]] 相关：几乎所有现代优化都默认输入是规范嵌套结构。
- **LINQ 不是免费的**：声明式 API 的抽象开销在热循环里会被放大百倍。在性能敏感路径用 `for` 而不是 LINQ，是一个很稳的经验法则。
- **凭直觉做优化就是凭直觉**：Sell 把大部分"嵌套循环罪犯论"归结为 cargo cult——说的人没做过基准，甚至没想清楚渐进复杂度是什么。

## 这不是说所有嵌套循环都无辜

文章一开头就声明这不是为所有嵌套循环辩护：**真正的性能问题**——比如内层循环里反复分配内存、访问不连续的 cache line、或者本可以通过算法改造降到 O(N log N) 的——该修还是要修。反驳的只是"因为是嵌套循环所以必须拆"这种**形式主义**的评审。正确的流程是：profile → 定位热点 → 确认代价 → 再决定如何改。

## 相关

- [[cache-friendliness]] —— 真正影响循环性能的那些东西
- [[latency-vs-throughput]] —— 常数因子到底怎么算
- [[order-of-growth]] —— Big-O 究竟描述什么，又没描述什么

## Sources

- [[sources/vertexfragment-demonizing-nested-loops]]
