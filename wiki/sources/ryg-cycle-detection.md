---
tags: [source, 算法, 调试, ryg]
date: 2026-04-14
sources: 1
---

# Cycle detection algorithms are handy to know（ryg / The ryg blog）

[[fabian-giesen]] 在 2010 年 10 月发表的短文，承接他上一篇关于 [[data-structure-invariants]] 的讨论：单链表最容易悄悄坏掉的方式之一是自身成环，这时候你需要一种不额外占内存、不需要写入「visited 位」就能工作的环检测算法。

## 摘要

文章建议记住两种经典的环检测算法——**Floyd 龟兔**和 **Brent 的倍增变体**。作者强调 Brent 算法常被忽视，但它其实是**迭代加深**在链表检测上的一个实例：每一轮都从头重跑，但因为深度指数增长，重复代价仍在最优解的常数倍以内。文章顺带抛出一个相关小谜题：双向无限铁轨上找同伴的最优搜索策略是「指数来回」，和 Brent 算法共享同一个「指数加深保证常数竞争比」的思想骨架。篇幅不长，更多是提醒而非教学；真正的算法细节 ryg 直接把读者指向 Wikipedia。

## 关键要点

- 单链表成环最常见的触发点：把同一个节点第二次插入链表
- 「加 visited 位」看似简单，但清理位本身要遍历可能坏掉的链表
- Floyd 算法（慢走 1 步，快走 2 步）最经典；Brent 算法（慢指针周期性跳到快指针位置，快指针按 2、4、8、16… 步长推进）实测通常更快
- Brent 算法是**迭代加深**的一个实例——重做代价是指数增长的，总代价落在最优解的常数因子内
- 「铁轨找人」小谜题：指数来回扫描可在最优距离的常数倍内找到同伴

## 链接到的概念

- [[cycle-detection-floyd-brent]]
- [[data-structure-invariants]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/08/cycle-detection-algorithms-are-handy-to-know/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-08_cycle-detection-algorithms-are-handy-to-know.md`
