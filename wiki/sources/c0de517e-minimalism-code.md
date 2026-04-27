---
tags: [source, 软件设计, 简洁性, 复杂性, 抽象]
date: 2026-04-27
sources: 1
---

# Notes on Minimalism in code（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2014 年 8 月的文章，受极简主义演讲启发，探讨如何把「有意识地做选择」的哲学带入编程实践。

## 摘要

Pesce 从现实生活的极简主义（Joshua Fields Millburn & Ryan Nicodemus 的演讲）中提炼出三条对编程直接适用的洞察。第一，**无用的复杂度往往不是程序员故意制造的，而是组织激励结构扭曲的结果**：写三个函数的 A 与搭建「框架」的 B，后者在缺乏技术判断力的团队里更容易获得晋升，复杂度因此自我繁殖。第二，**简洁不等于「尽量少」**，而是「审慎且有意义地选择」——每一次加入类、模板、抽象，都需要问「它为我省去的代码量，是否超过我为实现它所写的代码量，以及所有人为理解它所付出的代价」。第三，**删除代码是良性的**，引申出「打包派对」的代码版本：用覆盖率工具找到从未被执行的代码行，毫不犹豫地删除它们。

## 关键要点

- 过早泛化比过早优化更危险：泛化付出的代价不只是当下的编写成本，还有无限期的理解与维护成本
- 「压缩比喻」的逆面：抽象是代码压缩，但压缩本身不是目标；若解压器比原始数据还大，该抽象就不成立
- 每个决策都是 OR 问题（运筹学）：在模糊数量上做多目标权衡，没有通用公式，只有意识
- 「高使用量」和「表面简单」可以共存于内部极为复杂的东西（如 Mathematica），但游戏代码不应依赖这种黑盒
- 对代码度量的两条实用启发式：① 代码量 / 有效计算量（signal-to-noise）；② 引入省力 / 引入理解成本（ROI of abstraction）

## 链接到的概念

- [[negative-space-in-programming]]
- [[complexity]]
- [[abstraction]]
- [[cognitive-load]]
- [[tactical-programming]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/08/minimalism.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-08-23_notes-on-minimalism-in-code.md`
