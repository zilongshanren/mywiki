---
tags: [source, c++, 团队规范, 代码评审, 工程文化]
date: 2026-04-19
sources: 1
---

# Survive C++ / Collaborative Guidelines Experiment（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 1 月的一篇**预告式短文**：宣布将在 etherpad 上发起一次「C++ 视觉编码指南」的众包实验——以「code flashcards」的形式，列出「见到这种写法 → 该警觉什么」的规则，辅助代码评审。

## 摘要

Pesce 过去写过多篇反 C++ / 反 OOP / 反 design patterns 的博文，但他承认：做实时渲染的工程师仍然被 C++ 绑着——那就必须**想办法活下来**。所以他换一种正向姿态：发起一个类似 2010 年 [[sources/c0de517e-collaborative-engine-design|collaborative engine design]] 实验的**协作 etherpad**，让大家一起收集 C++ 写法「陷阱 → 应对」的闪卡，形式力求**视觉化**，便于代码评审时快速比对。

文章本身没给出具体条款，只是公告与约请——等 etherpad 沉淀稳定后他会把结果搬回博客。

评论区有读者质疑「为什么要避开 boost」，另一读者回答这是**游戏引擎语境**下的建议：游戏引擎架构和普通应用不同，大部分 design pattern 在这里并不合算（Singleton / Composite / Flyweight 是少数例外）。Pesce 确认了这点：「是，是关于游戏。」

## 关键要点

- **本文只是公告**：实质内容（那份「视觉编码指南」）不在本文，本文价值在**确立文体与问题**——C++ 在游戏引擎语境下的最小可行子集是什么？
- **延续 [[cpp-multi-paradigm-discipline|C++ 多范式纪律]] 的思路**：既然 C++ 是语言联邦，就必须在团队 / 子群体层面**先定义子集再开工**；Pesce 希望用众包的方式沉淀游戏圈的那个子集。
- **Flashcard 形式**是对代码评审的自觉优化——把抽象原则压缩成可视化、可快速模式匹配的反射，这和他在 [[code-tourism-practice|code tourism]] 中提议的「精彩片段陈列馆」是**同一套问题的两面**：陈列值得学的 vs 陈列值得警觉的。
- **反 boost** 仅限游戏引擎语境——boost 在通用 C++ 开发中仍被广泛认可；在游戏引擎里被回避的原因更多是编译成本、二进制体积、异常 / RTTI 依赖、调试难度等工业约束。
- **和 [[c0de517e-collaborative-engine-design|collaborative engine design experiment]] 是同系列**：都是「把个人笔记做成众包文档」的尝试，反映 Pesce 对「**思考应当公开协作**」的一贯信念。

## 链接到的概念

- [[cpp-multi-paradigm-discipline]]
- [[code-tourism-practice]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/01/survive-c-collaborative-guidelines.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-01-06_survive-c-collaborative-guidelines-experiment.md`

## 备注

- `2011-01-06_survive-c-collaborative-guidelines-experiment-2.md` 是同一篇的归档重抓（URL 只差 http/https），视作重复。
