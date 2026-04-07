---
tags: [编程语言, sicp, 函数式]
date: 2026-04-05
sources: 1
---

# 高阶函数（Higher-Order Functions）

**接收或返回函数的函数**——函数作为一等公民的直接后果。

## 一等公民（First-Class Citizen）

值可以：
- 被赋值给变量
- 作为参数传递
- 作为返回值返回
- 在运行时创建

当"值"可以是函数时，就有了高阶函数。

## 从重复到抽象

SICP 的典型推演：

```scheme
; 三个重复的模式
(define (sum-cubes a b) ...)
(define (sum-integers a b) ...)
(define (pi-sum a b) ...)
```

> "The presence of such a common pattern is strong evidence that there is a useful abstraction waiting to be brought to the surface."

抽象出通用 `sum`：

```scheme
(define (sum term a next b)
  (if (> a b) 0
      (+ (term a)
         (sum term (next a) next b))))

; 调用
(sum cube a inc b)
(sum identity a inc b)
```

## 现代语言的回响

- **JavaScript**：`map` / `filter` / `reduce` + 箭头函数
- **C# LINQ**（2007）：`Where()` / `Select()` / `Sum()` + Lambda
- **Python**：函数式工具 + list comprehensions
- **Rust**：`Iterator` trait 系统
- **Unity DOTS**：`Entities.ForEach(lambda)`

## 品味结晶

> "代码重复是思维还没到位的信号——当你三次复制同一个模式，你欠这个模式一个名字。"

**规则：两次等待，三次抽象**。避免为了函数式而强行包装单函数。

## 性能注意（游戏开发）

- Lambda 捕获外部变量 → 堆分配。
- Unity DOTS Burst 专门优化 lambda，但捕获 managed object 会禁用优化。

## 相关

- [[procedural-abstraction]]
- [[lambda-calculus]]
- [[elements-of-programming]]
- [[closure]]

## Sources

- [[sources/sicp-day06]]
