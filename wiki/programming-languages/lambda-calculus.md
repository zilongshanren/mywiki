---
tags: [编程语言, 理论基础]
date: 2026-04-05
sources: 1
---

# λ 演算（Lambda Calculus）

**计算的通用数学模型**——1930 年代由 Alonzo Church 提出，先于现代计算机。

## 核心元素

只需三种构造：
1. **变量**：`x`
2. **抽象**：`λx.M`（定义接收参数 x 的函数）
3. **应用**：`(M N)`（函数 M 作用于参数 N）

**就这三样**。整个计算理论可以用这三样推导出来。

## 与 Turing Machine 的等价

Church-Turing 假说：lambda 演算和图灵机计算能力等价——**任何可计算的东西都可以用 lambda 演算表达**。

## 核心操作：β-归约

```
(λx.M) N → M[x := N]
```

把函数应用到参数 = 把参数代换进函数体。这就是 [[substitution-model|代换模型]]的数学基础。

## 对编程语言的影响

- **函数式编程**（Lisp、Haskell、ML）直接以 lambda 演算为理论基础。
- **现代语言**的 lambda 表达式、匿名函数、闭包——都是 lambda 演算概念的工程化。
- **类型论**（System F、Hindley-Milner 推断）扩展了 lambda 演算。

## 游戏开发的直接联系

- C# 的 lambda 表达式 `x => x * 2`
- LINQ 查询
- Unity ECS 的 `ForEach(lambda)`

**每次你写 lambda 表达式，都在使用 1930 年代的数学发现**。

## 相关

- [[higher-order-functions]]
- [[substitution-model]]
- [[procedural-abstraction]]

## Sources

- [[sources/sicp-day06]]
