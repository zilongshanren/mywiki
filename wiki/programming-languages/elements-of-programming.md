---
tags: [编程语言, sicp, 核心概念]
date: 2026-04-05
sources: 1
---

# 编程的三要素（Elements of Programming）

SICP 开篇提出的框架——**所有强大的编程语言都有三个基本机制**：

> "Every powerful language has three mechanisms for combining simple ideas to form more complex ideas: primitive expressions, which represent the simplest entities the language is concerned with, means of combination, by which compound elements are built from simpler ones, and means of abstraction, by which compound elements can be named and manipulated as units."

## 三要素

1. **原子表达式（Primitive Expressions）**：语言最简单的实体。数字、字符串、布尔值、内建运算符。
2. **组合手段（Means of Combination）**：把简单元素拼成复杂元素。函数调用、复合数据类型、表达式嵌套。
3. **抽象手段（Means of Abstraction）**：把复合元素命名为单元。变量、函数、类、模块。

## 品味

编程的本质不是语法，而是这三种行为的互相融合。好的编程语言在三个层面都提供强大手段并让它们彼此一致。

## 与 APoSD 的呼应

Ousterhout 的 [[deep-modules|深模块]] 和 [[information-hiding|信息隐藏]] 是"抽象手段"的具体技艺。SICP 给出 **what**（三要素），APoSD 给出 **how**（怎么抽象得好）。

## 相关

- [[substitution-model]]
- [[procedural-abstraction]]
- [[higher-order-functions]]
- [[lambda-calculus]]

## Sources

- [[sources/sicp-day01]]
