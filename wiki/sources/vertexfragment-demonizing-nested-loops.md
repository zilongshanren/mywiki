---
tags: [source, performance, benchmarking, c-sharp, dotnet, programming-folklore]
date: 2026-04-14
sources: 1
---

# Demonizing Nested Loops（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 12 月的短评，反驳"嵌套循环总是拖慢性能所以必须拍扁"这一 code review 俗见。

## 摘要

作者多次目睹开发者——尤其是在面试里——下意识把双层 `for` 循环视为需要修复的"性能问题"，并抛出"Big O 复杂度"作为理由。Sell 用一个最朴素的基准反驳：同样遍历一个 10000×10000 的坐标网格，**嵌套双循环比手动拍平到单循环快 1.6 倍**，LINQ 版本则慢近 7 倍。单循环版慢的原因是每次迭代都要做整数除法和取模来还原 `(x, y)`——而现代 CPU 的整除相对昂贵。嵌套版让 JIT 和 branch predictor 都能顺利发挥，是"结构最干净"的形态。LINQ 版则叠加了匿名对象分配、迭代器构造和虚调用的额外常数。文章的真正要点是一句工程原则："**先按可读性/可维护性写，等实测证明需要优化再优化**"——把嵌套循环当成性能罪过是把 Big-O 的渐进复杂度和常数因子混为一谈。

## 关键要点

- **实测结果**（.NET Core 3.1，`iterations=10000`，10 次平均）：Nested 4.15M ticks；Single 6.70M ticks (161%)；LINQ 26.88M ticks (647%)。
- 单循环版的瓶颈是**整数除法/取模**，不是"少一层循环"带来的好处——反而是坏处。
- **渐进复杂度和常数因子是两件事**：两个版本都是 O(N²)，形式变化不改变渐进阶。
- **JIT/编译器偏好规整的嵌套结构**：手动展平可能反而阻止了 loop unrolling、bounds-check elimination 等优化。
- **LINQ 的抽象代价**在热循环里被放大到百倍量级，不适合性能敏感路径。
- 工程层面的总结：**先可读后性能**，基准测试驱动优化决定，避免基于直觉的 cargo cult 评审。
- 作者没有为所有嵌套循环辩护——真正的性能问题（内层分配、cache 不友好、可算法改造的）该修还是要修；反对的只是**形式主义的**"只要是嵌套就拆"这种评审逻辑。

## 链接到的概念

- [[nested-loop-optimization]]
- [[cache-friendliness]]
- [[order-of-growth]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/demonizing-nested-loops/
- 本地：`raw/articles/vertexfragment.com/2019-12-13_demonizing-nested-loops.md`
