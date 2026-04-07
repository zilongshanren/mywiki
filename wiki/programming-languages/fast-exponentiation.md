---
tags: [算法, sicp, 分治]
date: 2026-04-05
sources: 2
---

# 快速幂（Fast Exponentiation）

**分治思想的经典例证**：求 `b^n` 从朴素 O(n) 降到 O(log n)。

## 核心观察

```
b^(2n) = (b^n)^2
b^(2n+1) = b × b^(2n)
```

每次把指数减半，对数复杂度自然浮现。

## 实现

```scheme
(define (fast-expt b n)
  (cond ((= n 0) 1)
        ((even? n) (square (fast-expt b (/ n 2))))
        (else      (* b (fast-expt b (- n 1))))))
```

## SICP 的直觉

> "Computing b^(2n) using fast-expt requires only one more multiplication than computing b^n. The size of the exponent we can compute therefore doubles (approximately) with every new multiplication we are allowed."

**每多一次乘法，可处理的指数大约翻倍**——这就是 O(log n) 的直观含义。

## 矩阵快速幂

把 b 换成矩阵，操作换成矩阵乘法：可以 O(log n) 计算：
- Fibonacci 数列（通项公式的迭代形式）
- 骨骼动画的程序化姿态
- 线性递推关系

## 模幂运算（modular exponentiation）

```
expmod: b^n mod m in O(log n)
```

**RSA 加密的核心运算**、[[probabilistic-algorithms|Fermat 素性测试]]的核心运算。

## 相关

- [[order-of-growth]]
- [[probabilistic-algorithms]]
- [[recursive-vs-iterative-process]]

## Sources

- [[sources/sicp-day04]]
- [[sources/sicp-day05]]
