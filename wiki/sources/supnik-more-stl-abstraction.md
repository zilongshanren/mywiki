---
tags: [source, C++, STL, 性能]
date: 2026-04-19
sources: 1
---

# More STL Abstraction（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 11 月的续写文章，回应了早先《STL Is Not An Abstraction》的评论，承认自己的用词不精确，并补上若干「规格允许、但实现之间差异可观」的具体例子。

## 摘要

Supnik 指出 STL 并不是规格不清，而是**在规格允许的范围内，实现依然存在性能差异**。他举了两个例子：`vector` 的区间 insert 可以选「一边走一边扩容（多次 reallocation）」或「先测距离再一次分配」，后者对无随机访问的迭代器要付出二次遍历代价；`list::size()` 在 SGI 规范里允许 O(N) 或 O(1)，旧 gcc STL 曾是线性，新版本缓存了大小。因此在容器选型的边界情况，跨实现的差异可能刚好压过 vector↔list 的决策线。他自己的做法是：真出性能问题就上 Shark profile；常见结局反而是彻底扔掉 STL 换成手写容器，profile 本身会同时暴露 STL 实现间的差异。评论区补充一句点醒：STL 属于**泛型编程**的范畴，不是 OOP，其目标从来不是隐藏细节，而是解耦算法与容器；这让 Supnik 重新整理了自己的用词。

## 关键要点

- STL 的「未明说的弹性」：规格允许但实现可以差很多——`vector` 区间 insert、`list::size()` 都是例子。
- 性能敏感场景里，容器间的抉择可能被实现差异盖过：vector 只能单次分配还是 list 能 O(1) size，决定选型。
- 实际工程解药不是背下规格，是跑 profiler；Shark 同时能暴露 STL 实现问题。
- 一部分团队（包括 X-Plane）最后选择**彻底替换 STL**——既然要 profile，就把替换 STL 的工作也纳入进来。
- Stepanov 原意：STL 是 generic programming 的产物，不追求隐藏细节，追求算法跨容器复用。

## 链接到的概念

- [[stl-not-abstraction-prescription]]
- [[rpp-stl-replacement]] —— 类似「干脆重写一套 STL」的现代回响
- [[optimization-leverage-ratio]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/more-stl-abstraction.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-26_more-stl-abstraction.md`
