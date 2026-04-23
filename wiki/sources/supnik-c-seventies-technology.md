---
tags: [source, C, 历史, 操作符优先级, BCPL]
date: 2026-04-19
sources: 1
---

# The Very Best Seventies Technology（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 11 月的一篇短文，半调侃半科普地解释**为什么 C 的 `&` 优先级比 `==` 低**——从 B / BCPL 一路考古到 Ritchie 的个人选择。

## 摘要

C 里 `if (value & mask == flag)` 总是错的，因为 `==` 优先级高于 `&`。直觉上 bit-wise 操作应该和算术一样优先，真实情况是历史包袱：C 的前身 B（以及 B 的前身 BCPL）只有一个 `&`——在 `if` / `while` 条件里当逻辑短路 AND 用，在其他地方当位与用。为了让 `if (ptr & ptr->value)` 这种写法安全，B 里 `&` 的优先级必须**接近 `&&`**——也就是"比比较低"。Ritchie 设计 C 时把 `&` 和 `&&` 拆成两个 token，但如果**同时把 `&` 的优先级抬到算术档**，所有 B 时代留下的代码语义都会静默改变。他选择**维持旧优先级** + **新增 `&&` token**——结果我们今天写位运算永远要记得手工加括号。Supnik 本文的"支线剧情"是他自嘲不想让自己的 C++ 看起来像 Lisp（一堆"安全"括号），于是去梳理了 C 的操作符优先级——意外发现 95% 的表达式"默认优先级就是想要的"。

## 关键要点

- B/BCPL 里 `&` 在条件上下文做短路 AND，所以优先级必须低于比较；
- Ritchie 分裂 `&` / `&&` 的同时**没有**抬高 `&` 的优先级——为了不破坏已有代码；
- `<<` / `+` 也有类似坑：`1 << 2 + 3` = `1 << 5`；
- 大部分 C 优先级按"一元→算术→比较→逻辑→赋值"分层是自然的，位操作是反例。

## 链接到的概念

- [[c-bitwise-operator-precedence-history]]
- [[avoid-unsigned-types]]
- [[floating-point-geometric-predicates]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/very-best-seventies-technology.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-11_the-very-best-seventies-technology.md`
