---
tags: [source, sicp, 编程语言]
date: 2026-04-05
sources: 1
---

# SICP Day 3 —— 递归的两张面孔

SICP 学习推送第 3 天。

## 摘要

区分**递归语法（syntactically recursive procedure）**和**递归过程（recursive process）**：前者是代码写法，后者是计算行为。迭代过程用固定状态变量表达，递归过程靠延迟操作链（deferred operations）。讨论尾调用优化（TCO）的语言设计分歧。

## 关键要点

- **递归过程**：展开-收缩，存在延迟操作链，空间随规模增长。
- **迭代过程**：固定数量的状态变量，空间 O(1)。
- **尾调用优化（TCO）**：Scheme 强制要求；C/C++ 可选；Java 不支持（保护 stack trace）；Python Guido 反对；ES6 标准要求。
- 树形递归不是坏事——处理树形数据时很自然，关键是识别冗余计算。

## 链接到的概念

- [[recursive-vs-iterative-process]]
- [[tail-call-optimization]]

## 原文

- 链接到：[[raw/articles/sicp/day3]]
