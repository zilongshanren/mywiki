---
tags: [source, sicp, 编程语言]
date: 2026-04-05
sources: 1
---

# SICP Day 1 —— 编程的三要素

SICP 学习推送第 1 天，对应 Chapter 1 Building Abstractions with Procedures。

## 摘要

介绍编程语言的三个基本机制：**原子表达式**、**组合手段**、**抽象手段**。强调 SICP 不是教你 Scheme，而是教你怎么思考编程。引入了环境、代换模型、应用序与正则序、代码即数据等核心观念。

## 关键要点

- **编程语言的三要素**：primitive expressions、means of combination、means of abstraction——"Every powerful language has three mechanisms..."
- **环境（Environment）**：保存名字-值对的内存结构，是理解闭包和作用域的基础。
- **代换模型（Substitution Model）**：β-归约；理解纯函数求值的思维工具。
- **应用序 vs 正则序**：求值时机的设计选择；大多数语言是应用序，惰性求值基于正则序。
- **代码即数据（Homoiconicity）**：Lisp 的设计特性，程序本身就是可被操作的数据结构。
- 品味：编程的本质不是语法，而是这三种行为的互相融合。

## 链接到的概念

- [[elements-of-programming]]
- [[substitution-model]]
- [[applicative-vs-normal-order]]
- [[environment]]

## 原文

- 链接到：[[raw/articles/sicp/day1]]
