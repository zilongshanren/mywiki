---
tags: [编程语言, sicp]
date: 2026-04-05
sources: 1
---

# 代换模型（Substitution Model）

SICP 用来解释函数求值的**思维工具**：把参数代入函数体、逐步化简，像手工解方程。

## 使用方式

```
(square 5)
→ (* 5 5)      ; 把 x 代换为 5
→ 25           ; 应用 primitive *
```

## 局限

代换模型只适用于**纯函数**——没有副作用、没有可变状态。一旦涉及 `set!`、I/O、引用，就要升级到**环境模型**。

## 应用序 vs 正则序

- **应用序**：先求值参数，再代换。大多数语言用这个。
- **正则序**：直接把参数表达式代换进函数体，用到时才求值——**惰性求值**的基础（Haskell）。

## 与 β-归约

代换模型本质上是 λ 演算中的 β-归约的工程化版本。理解它能帮助你在脑子里模拟纯函数代码的执行。

## 相关

- [[elements-of-programming]]
- [[applicative-vs-normal-order]]
- [[lambda-calculus]]
- [[environment]]

## Sources

- [[sources/sicp-day01]]
