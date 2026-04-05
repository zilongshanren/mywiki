---
tags: [source, aposd, 软件设计]
date: 2026-04-05
sources: 1
---

# APoSD Day 1 —— Introduction：一切都是关于复杂性

APoSD 学习推送系列第 1 天，对应 Ousterhout 第 1 章 Introduction。

## 摘要

引入本书的核心主题：**软件开发的最大限制不是技术，是理解系统的能力**。复杂性是软件设计的根本敌人；它会不可避免地累积，但可以被管理。对抗它有两条路——**消除**（简化代码、减少特殊情况）和**封装**（模块化设计）。软件设计是持续过程，不是一次性活动。本章还引入了「红旗」这个训练设计直觉的工具。

## 关键要点

- 最大限制是**认知**，不是技术——「The greatest limitation in writing software is our ability to understand the systems we are creating」。
- **Subtle dependencies**（微妙的依赖）是复杂性的核心形态。游戏项目特别容易产生，因为业务逻辑耦合往往不走代码调用。
- 复杂性会不可避免地增长——目标不是零复杂性，而是**放在正确位置、用正确方式封装、尽可能慢地增长**。
- 对抗复杂性的两条路：**消除复杂性**（简化、去特殊情况）与**封装复杂性**（模块化）。
- **[[continuous-design|软件设计是持续过程]]**——增量开发不是「不设计」的借口，而是「持续设计」的要求。
- **[[red-flags]]**：训练「停下来、寻找替代方案」的习惯。
- **本质复杂性 vs 不必要复杂性**：前者不可消除只能封装，后者是设计可以消除的。
- 与 Clean Code、设计模式的定位区别：APoSD 提供**框架**，不提供规则。

## 链接到的概念

- [[complexity]]
- [[continuous-design]]
- [[red-flags]]
- [[modular-design]]
- [[tactical-programming]] vs [[strategic-programming]]（埋种子）
- [[john-ousterhout]]

## 原文

- 链接到：[[raw/articles/a-philosophy-of-software-design/day1-lesson]]
