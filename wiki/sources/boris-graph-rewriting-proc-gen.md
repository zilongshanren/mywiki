---
tags: [source, procedural-generation, graph-rewriting, level-generation]
date: 2026-04-27
sources: 1
---

# Graph Rewriting for Procedural Level Generation（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 4 月的文章，系统介绍图改写（Graph Rewriting）技术及其在游戏关卡生成中的应用。

## 摘要

本文是 Boris 针对游戏 Unexplored 关卡生成技术的深度拆解系列的第一篇。文章首先介绍图（Graph）这一基础数据结构——节点与边的集合，适用于表达关系网络。随后解释**图改写（Graph Rewriting）**的核心思想：类比文本查找替换，定义一组"左侧模式"与"右侧替换"规则，在更大图的局部匹配并替换，从而迭代生长出复杂结构。这一机制能生成链状、分叉、环形等多样拓扑。文章还横向比较了 L-System（也基于替换但针对线性字符串）和多款游戏/工具（Enter the Gungeon、Dungeon Architect）对图改写的有限使用，并介绍了 Joris Dormans 长期研究该方向的成果——PhantomGrammar 与 Ludoscope 工具。

## 关键要点

- 图改写 = 图上的查找替换，左侧模式匹配子图，右侧指定替换结构
- 能生成 L-System 无法表达的循环/非线性拓扑
- Dormans 等人的研究表明其在任务/空间生成中有很强表达力
- 实际游戏中使用仍属罕见，多以简化形式出现
- 是理解 Unexplored 的 PhantomGrammar 生成系统的前置知识

## 链接到的概念

- [[game-development/graph-rewriting-proc-gen]]
- [[game-development/procedural-dungeon-generation]]
- [[game-development/mission-graph]]

## 原文

- 链接：https://www.boristhebrave.com/2021/04/02/graph-rewriting/
- 本地：`raw/articles/boristhebrave.com/2021-04-02_graph-rewriting-for-procedural-level-generation.md`
