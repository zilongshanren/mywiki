---
tags: [source, 软件设计, C++, STL]
date: 2026-04-19
sources: 1
---

# The STL Is Not An Abstraction（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 2 月的一篇短文，反驳「STL 是个有时会泄漏的抽象」，主张它根本就不是抽象。

## 摘要

Supnik 用 Joel Spolsky「Leaky Abstractions」做参照系：真正的抽象**隐藏实现**。而 STL 不隐藏任何东西，它是**开放的规定**——你选 `vector` 等于签下一份合同：连续内存、拷贝构造调用无数次、中段插入昂贵、resize 会让 iterator 失效。所以 STL 不算抽象失败，它是一个「shortcut」：帮你省下从零写数据结构的功夫，前提是你懂每个容器的取舍。评论区延伸出 C++ 的特殊处境：在运行复杂度是头等关切的语言里，**把 Big-O 刻进接口**才是正确设计；隐藏它（比如 SQL 优化器）偶尔会坑死用户。

## 关键要点

- 抽象 = 隐藏细节；STL 不隐藏任何东西，精确 prescribe 实现。
- 选 `vector` 等于同时选择了它的 5 条性能特征。
- 把复杂度写进接口是 C++ 在 performance-critical 场景下的正确设计选择。
- 和 SQL 查询优化器作对比：后者是真正的（漏水）抽象，前者不是。
- Scott Meyers Effective STL item 2：「Beware the illusion of container-independent code」。
- C++0x 原本计划用 concepts 让接口约束显式化，但被搁置；C++20 最终补上。

## 链接到的概念

- [[stl-not-abstraction-prescription]]
- [[abstraction]]
- [[false-abstraction]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/02/stl-is-not-abstraction.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-03_the-stl-is-not-an-abstraction.md`
