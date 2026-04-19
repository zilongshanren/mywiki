---
tags: [source, 软件设计, 性能, 分配器]
date: 2026-04-19
sources: 1
---

# This One Weird Trick Let's You Beat the Experts（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 标题党式博文，一句话教你写比 `malloc` 更快的分配器。

## 摘要

文章用 StackOverflow 上的典型问答开场——新人问"怎么写比系统分配器还快的 allocator"，资深玩家讽刺式地劝退："你写不过黑胡子大神。"然后作者给出答案：**作弊**。贴出一段"世界上最烂的 allocator"——静态 1K buffer、忽略 free——这段代码确实比 `malloc` 快，只要你不要求它做 `malloc` 做的那些事（任意大小、任意顺序、可 free、跨线程）。下一步升级到 **bump allocator**（[[linear-allocator|线性分配器]]）：一块大 buffer + 一个 offset 指针，帧末整体 reset；这是游戏引擎里"每帧一个 arena"的常见做法，单次分配是一条加法，free 是 no-op，没有锁。作者抽象出三条判断准则：(1) 你需要更好性能；(2) 你的抽象需求比通用情形更简单或更特别；(3) 能用这些特殊要求写出更快的实现。三条全中，自己动手；否则用标准实现。这个方法论同样适用于网络协议（游戏自研 UDP over TCP）、哈希表、字符串处理等领域。

## 关键要点

- **通用实现 = 通用代价**：系统 `malloc` 覆盖所有情况，代价是对任何单一情况都不是最优。
- 三问：need better perf? requirements simpler/more peculiar? can exploit that?
- 典型例：bump/linear allocator、UDP 私有协议、perfect hash、SIMD numeric parsing。
- 写库的人没有这个选项——他们必须承担通用性的代价。
- 风格：标题党 + 贯穿笑点（黑胡子大神、Zilog Z-80、Heisenberg 分配器）。

## 链接到的概念

- [[cheat-by-solving-less]]
- [[linear-allocator]]
- [[future-proofing-tests]]
- [[graphics-programmer-constraints]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/06/beating-experts.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-10-29_this-one-weird-trick-let-s-you-beat-the-experts.md`
