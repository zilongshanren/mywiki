---
tags: [source, aposd, 软件设计]
date: 2026-04-05
sources: 1
---

# APoSD Day 2 —— 复杂性的定义与症状

APoSD 学习推送系列第 2 天，对应第 2 章 The Nature of Complexity。

## 摘要

给出复杂性的精确定义：**任何使系统难以理解和修改的东西**。强调复杂性是读者视角的判断，不是写者的。提出衡量公式 `C = Σ(cp × tp)`——隔离到少触之地等于消除。复杂性有三种症状：**变更放大**、**认知负荷**、**未知的未知**。有两大根源：**依赖**和**模糊性**。复杂性是渐进累积的，没有灾难性时刻。

## 关键要点

- 复杂性的定义：**Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system.**
- 复杂性更对读者显而易见：「Complexity is more apparent to readers than writers」。
- 公式 **C = Σ(cp × tp)**——把复杂隔离到罕有接触的地方，约等于消除。
- 三症状：
  - [[change-amplification]]——改动需要触及多处
  - [[cognitive-load]]——需要知道太多
  - [[unknown-unknowns]]——不知道自己不知道（最危险）
- 两根源：[[dependencies]]、[[obscurity]]
- 文档是补丁，不是解药：**需要大量文档的地方通常是设计不太对的红旗**。
- 复杂性渐进累积——没人主动搞乱系统，小妥协累积成灾难。
- 认知负荷 ≠ 代码行数。有时更长的代码更简单。

## 链接到的概念

- [[complexity]]
- [[change-amplification]]
- [[cognitive-load]]
- [[unknown-unknowns]]
- [[dependencies]]
- [[obscurity]]
- [[john-ousterhout]]

## 原文

- 链接到：[[raw/articles/a-philosophy-of-software-design/day2-lesson]]
