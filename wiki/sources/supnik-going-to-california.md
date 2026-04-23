---
tags: [source, 计算机体系结构, 缓存, 内存层次, 文件系统]
date: 2026-04-19
sources: 1
---

# Going to California (with an Aching in My Heart)（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 4 月 25 日的一篇短文，借 Gustavo Duarte 的「把一个 cycle 映射成人类一秒」比喻，把存储层次的延迟翻译成日常可感时间，并把它直接绑到 X-Plane 场景包文件打包的工程决策上。

## 摘要

1 cycle = 1 秒 的尺度下：L1 = 桌上、L2 = 书架、主存 = 楼下车库、磁盘 = **走到加州再走回来**。3 GHz CPU 上一次 41 ms 磁盘 seek 等于 474 人类天——即使你每天走 12 英里也来回不完。Supnik 的应用：X-Plane 的 scenery 包用一堆小 text 文件储存，**每个小文件都是一次加州之旅**；DSF RFC 提案把它们合成一个大文件，让 OS 能一次 seek 把大块连续数据 dump 进 page cache。操作系统已经拼命伪装磁盘是快的，但你要配合它——不给它大量随机小 I/O。

## 关键要点

- 把延迟差距变直觉：L1→L2→DRAM→Disk 不是阶梯，是鸿沟
- 一次磁盘 seek ≈ 474 CPU 天 = 美东走加州一圈
- OS 的 page cache / readahead / elevator 伪装得好，但**需要 I/O pattern 配合**
- X-Plane 的 scenery 重构：合并小文件 = 一次 seek 换数百次
- 脚注幽默：如果你住加州，「就假装自己是 SSD」

## 链接到的概念

- [[memory-latency-human-metaphor]]
- [[memory-hierarchy]]
- [[locality-principle]]
- [[cache-friendliness]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/04/going-to-california-with-aching-in-my.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-04-25_going-to-california-with-an-aching-in-my-heart.md`
