---
tags: [source, sicp, 编程语言]
date: 2026-04-05
sources: 1
---

# SICP Day 2 —— 过程即黑盒抽象

SICP 学习推送第 2 天。

## 摘要

论述过程抽象作为信息隐藏的基本形态。引入绑定变量、自由变量、块结构、词法作用域、闭包等概念。提到 Scheme 1975 选择词法作用域的历史意义。

## 关键要点

- 过程抽象屏障：使用者不需要知道实现细节。
- **绑定变量（Bound Variables）**：过程内部参数，作用域局限。
- **自由变量（Free Variables）**：来自外部环境，是隐式耦合来源。
- **块结构（Block Structure）**：函数内部定义辅助函数，隐藏实现细节。
- **词法作用域（Lexical Scoping）**：Scheme 的关键决策，变量作用域由代码静态结构决定，打破当时 Lisp 的动态作用域惯例。
- **闭包（Closure）**：函数 + 其定义环境。
- 与 APoSD 的 [[information-hiding]] 直接呼应。

## 链接到的概念

- [[procedural-abstraction]]
- [[lexical-scoping]]
- [[closure]]
- [[information-hiding]]

## 原文

- 链接到：[[raw/articles/sicp/day2]]
