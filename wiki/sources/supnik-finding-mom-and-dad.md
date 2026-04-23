---
tags: [source, C++, 数据结构, 模板, 侵入式链表]
date: 2026-04-19
sources: 1
---

# Finding Mom and Dad（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 11 月的一篇短文，题目是"孩子怎么找到父母"——讲的是 C++ 里一个小但真实的类型系统限制。

## 摘要

考虑一个对象 `O` 包含两个子部件 `S1` / `S2`，两个子部件各自维护一条侵入式链表；为了节约内存，两条链表共用**同一个 free-node stack**——stack 的头放在 `O` 里，`S1` / `S2` 不自带。想把"pop_front"这个操作封装到一个模板里，调用形如 `S1_head_list.pop_front()`，函数内部知道怎么去 `O` 里拿 free stack。问题在于：**`S1`、`S2` 作为对象，没有直接回到 `O` 的引用**，而 C++ 的类型系统**不允许把"从 `S1` 到 `O` 内部某字段的字节偏移"作为编译期已知信息传给模板**。可行但笨重的解法：`S1` / `S2` 各存一个 `O*` back-pointer——安全、fool-proof，但对**存储敏感**（比如 `O` 本身是海量实例的轻量对象）的场景不可接受。Supnik 给出的权宜办法：把模板版本的 `pop_front` 包在 `O` 的成员函数里，把 `S1`/`S2` 的 list pointer 设成 private，**缩小误用的面积**但治标不治本。

文章本身很短，核心价值是记录了一条**小但反复出现的 C++ 限制**：孩子想知道父亲地址，语言不给。

## 关键要点

- 侵入式数据结构里"共享池 + 多个使用者"的模式下，使用者要能反向找到池；
- 传 `O*` 回指针是最干净解，但每个 `S` 多付一个指针的开销；
- 模板无法把"字段相对偏移"作为编译期已知参数接收；
- 次优解是**把操作收进 `O` 的成员函数 + 把 list head 设 private**，缩减误用面。

## 链接到的概念

- [[parameter-nodes-intrusive-linked-list]] —— 另一侧：Bitsquid 的全局池 + 小索引方案
- [[cache-friendliness]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/finding-mom-and-dad.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-10_finding-mom-and-dad.md`
