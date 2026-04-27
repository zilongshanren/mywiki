---
tags: [source, software-design, 特化, 抽象]
date: 2026-04-27
sources: 1
---

# Solve Less General Problems（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2018 年 8 月发表的文章，以亲身经历的"硬件抽象层教训"为起点，系统阐述为什么"解更小的问题"是更成熟的工程判断，而非偷懒。

## 摘要

Supnik 刚出校门时在 Avid 被分配做 DV/1394 支持，年轻时的本能是设计一套通用 HAL（硬件抽象层）支持任意视频输入。HAL 做完了，DV 也跑起来了，然后产品被取消了，HAL 永远再没被用过。这个故事让他意识到：HAL 的"通用性"既浪费了开发资源，也从未获得任何回报，而"直接 special-case DV"本可以以极小代价完成需求。文章随后将这个教训抽象为一条普遍原理：通用解决方案天然携带通用代价；当你能确认需求不需要通用性时，选一个恰好够用的特化方案，弱点恰好落在你不需要的那部分。文章引用了 Fedor Pikus 在 lock-free 领域的观点（全通用的无锁设计往往根本不可行，特化方案才能真正落地）和 Mike Acton 的 Data-Oriented Design（"了解你的数据"，针对你实际的数据而非想象中的任意数据写代码）。最后用一个比喻收尾：宁要一个特化但不泄漏的方案，也不要一个通用但到处漏风的抽象。

## 关键要点

- YAGNI 的实践形式：不为从未出现的需求预留通用性
- 每个方案都有弱点；选特化方案，让弱点落在你不需要的地方
- 通用性本身是设计和维护成本，在需求不确定时是纯开销
- lock-free 编程的全通用设计可能根本无法实现，特化才能落地
- Data-Oriented Design 的"知道你的数据"就是同一思想的另一表述

## 链接到的概念

- [[cheat-by-solving-less]]
- [[abstraction]]
- [[false-abstraction]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2018/08/solve-less-general-problems.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2018-08-11_solve-less-general-problems.md`
