---
tags: [source, aposd, 软件设计]
date: 2026-04-05
sources: 1
---

# APoSD Day 4 —— 深模块：最重要的设计原则

APoSD 学习推送系列第 4 天，对应第 4 章 Modules Should Be Deep（前半部分）。

## 摘要

本章的核心概念：**深模块 = 强大功能 + 简单接口**。作者把接口理解为**成本**——调用者必须承担的认知负担——而功能是收益。经典例子 **Unix I/O**：5 个系统调用隐藏几十万行实现。**垃圾回收器**是接口为零的终极深模块。抽象是「简化视图，省略不重要细节」；省略重要细节即是**虚假抽象**。与 Clean Code、GoF 的关系：APoSD 提供判断拆分时机的原理，而不是机械规则。

## 关键要点

- **[[modular-design|模块化]]的真正目标是认知隔离**，不是单纯切分。
- **功能是收益，接口是成本**。每个方法都是负担。
- 接口有 formal（签名、类型）和 informal（行为、约束、副作用）两部分；**informal 通常更大更复杂**。
- **[[deep-modules|深模块]]**：强大功能，简单接口（高窄矩形）。
- **[[unix-io|Unix I/O]]** 5 个调用背后是几十万行实现；接口几十年不变。
- **[[garbage-collector]]**：零接口的深模块；加 GC 反而缩小了系统总接口。
- **[[abstraction|抽象]]**：简化视图，省略**不重要**细节；两种失败——不重要细节太多、重要细节被省（[[false-abstraction]]）。
- **浅模块示例**：`addNullValueForAttribute`——负数价值。
- **[[classitis|Classitis]]**：类炎症，「小类更好」的教条。Java I/O 是典型。
- **常见情况应做简单**：Unix 默认顺序+缓冲；Java 要求显式 BufferedInputStream。
- 判断深度的启发式：**文档比率**、**调用者知识**、**常见情况**、**实现变化**。

## 链接到的概念

- [[deep-modules]]
- [[shallow-modules]]
- [[classitis]]
- [[interface-vs-implementation]]
- [[abstraction]]
- [[false-abstraction]]
- [[unix-io]]
- [[garbage-collector]]
- [[modular-design]]
- [[java-io]]
- [[john-ousterhout]]

## 原文

- 链接到：[[raw/articles/a-philosophy-of-software-design/day04]]
