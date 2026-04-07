---
tags: [source, sicp, 编程语言]
date: 2026-04-05
sources: 1
---

# SICP Day 6 —— 高阶函数

SICP 学习推送第 6 天。

## 摘要

**高阶函数（Higher-Order Procedures）**作为函数式编程的核心——接收或返回函数的函数。**函数作为一等公民**。从通用求和模式开始，看到「等待被浮现出来的有用抽象」。与 Lambda 演算的历史渊源。

## 关键要点

- 识别重复模式并抽象为高阶函数：「代码重复是思维还没到位的信号」。
- **一等公民**：可赋值、传参、返回、运行时创建。
- Lambda 演算（1930s，Alonzo Church）是计算的通用基础。
- 通用 `sum` 模式：`(sum term a next b)`。
- 现代语言回响：JS map/filter/reduce、C# LINQ、Python/Rust Iterator、Unity ECS `ForEach(lambda)`。
- 游戏应用：Tween 缓动参数化、AI 行为查询链、DOTS 的 ForEach。
- **规则**：两次等待，三次抽象；避免为了函数式而函数式。

## 链接到的概念

- [[higher-order-functions]]
- [[lambda-calculus]]
- [[procedural-abstraction]]

## 原文

- 链接到：[[raw/articles/sicp/day06]]
