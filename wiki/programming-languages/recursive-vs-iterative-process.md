---
tags: [编程语言, sicp, 算法]
date: 2026-04-05
sources: 1
---

# 递归过程 vs 迭代过程

SICP 的关键区分：**递归语法（recursive procedure）** 和 **递归过程（recursive process）**不是同一件事。

## 定义

- **递归语法**：过程在定义中调用自己——**代码层面**的特征。
- **递归过程**：运行时有**展开-收缩**行为，存在**延迟操作链（deferred operations）**——**计算行为**的特征。
- **迭代过程**：状态由**固定数量的状态变量**描述，不依赖调用栈——空间 O(1)。

> "In contrasting iteration and recursion, we must be careful not to confuse the notion of a recursive process with the notion of a recursive procedure."

## 例子

```scheme
; 递归语法 + 递归过程
(define (fact n)
  (if (= n 0) 1
      (* n (fact (- n 1)))))   ; 乘法延迟到递归返回后

; 递归语法 + 迭代过程
(define (fact-iter n)
  (define (loop acc i)
    (if (> i n) acc
        (loop (* acc i) (+ i 1))))  ; 尾调用，无延迟操作
  (loop 1 1))
```

两者都是递归语法。但前者 O(n) 栈空间，后者**如果语言支持 TCO**则 O(1) 栈空间。

## 与 TCO 的关系

递归语法能否表现为迭代过程，取决于语言是否做 [[tail-call-optimization|尾调用优化]]：
- Scheme：标准保证 TCO。
- C/C++：编译器可选。
- Java：**不支持**（保护 stack trace）。

## 相关

- [[tail-call-optimization]]
- [[order-of-growth]]
- [[elements-of-programming]]

## Sources

- [[sources/sicp-day03]]
