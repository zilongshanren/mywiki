---
tags: [编程语言, sicp, 性能]
date: 2026-04-05
sources: 1
---

# 尾调用优化（Tail Call Optimization，TCO）

**当递归调用是函数的最后一个操作时，复用当前栈帧而不创建新帧**——让递归语法在 O(1) 空间下执行。

## 尾调用条件

```scheme
; 这是尾调用——没有延迟操作
(define (loop n)
  (if (= n 0) 'done
      (loop (- n 1))))

; 这不是尾调用——乘法延迟
(define (fact n)
  (if (= n 0) 1
      (* n (fact (- n 1)))))   ; * 是最后操作，不是 fact
```

## 语言支持

| 语言 | TCO 支持 |
|---|---|
| Scheme | **强制**（R5RS 标准） |
| Haskell | 有（惰性求值下） |
| OCaml / F# | 有 |
| Rust | 无（tail-call attr 是提示） |
| C/C++ | 编译器可选（-O2 通常会做） |
| Java | **不支持**——保护 stack trace |
| Python | **不支持**——Guido 反对 |
| JavaScript | ES6 标准要求，浏览器实现不一 |
| Swift | 支持 |
| Kotlin | `tailrec` 关键字显式开启 |

## Java 为什么拒绝

Java 认为 stack trace 对诊断 bug 至关重要，TCO 会让递归调用"消失"，破坏调试。这是语言哲学选择，不是技术限制。

## 工程影响

如果语言**不支持** TCO，所有靠尾递归表达的迭代过程都会 StackOverflow。**Java/Python 代码要用 while 循环替代尾递归**。

## 相关

- [[recursive-vs-iterative-process]]
- [[order-of-growth]]

## Sources

- [[sources/sicp-day03]]
