---
tags: [source, game-development, procedural-generation, graph-rewriting, level-generation]
date: 2026-04-27
sources: 1
---

# PhantomGrammar and Ludoscope（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 4 月的文章，介绍 Joris Dormans 围绕图改写构建的完整生成工具套件 PhantomGrammar 及其图形化 IDE Ludoscope。

## 摘要

PhantomGrammar 是 Dormans 多年开发积累的图改写引擎，驱动了 Unexplored 等游戏的内容生成。它在基础图改写之上增加了扩展图（节点/边带任意属性）、条件匹配、随机选择替换、以及三种迭代模式（Normal / LSystem / Cellular）。规则被组织进"菜谱（Recipe）"——顺序执行的指令序列，控制哪批规则在何时以何种模式运行。Unexplored 有超过 5000 条规则，通过菜谱分模块管理。该工具的局限在于难以表达传统算法（如图布局），且缺乏高级抽象，简单操作也需分解为多步规则。

## 关键要点

- PhantomGrammar 在图改写基础上支持扩展图、条件模式匹配、代码钩子
- 三种迭代模式——Normal（随机单次）、LSystem（扫描序替换全部匹配）、Cellular（找到所有匹配后批量替换）——对应不同生成语义
- 菜谱（Recipe）机制解耦"生成什么"与"何时执行"，是管理 5000+ 规则的关键
- 工具支持字符串、切片地图等非图对象，可直接实现 L-System 和元胞自动机
- 主要局限：无法做图布局算法、缺乏抽象导致重复编码几何操作

## 链接到的概念

- [[game-development/graph-rewriting-proc-gen]]
- [[game-development/phantomgrammar-ludoscope]]
- [[game-development/dungeon-generation-algorithm]]
- [[game-development/mission-graph]]

## 原文

- 链接：https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/
- 本地：`raw/articles/boristhebrave.com/2021-04-02_phantomgrammar-and-ludoscope.md`
