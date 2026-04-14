---
tags: [编程语言, sicp]
date: 2026-04-05
sources: 1
---

# 闭包（Closure）

**函数 + 其定义时的环境**——函数"记住"了出生时看到的变量，即使被传到别处调用依然能访问。

## 经典例子

```scheme
(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

(define c (make-counter))
(c) ; 1
(c) ; 2
(c) ; 3
```

`make-counter` 返回的 lambda 捕获了 `count`——即使 `make-counter` 早已返回，返回的函数依然能修改并读取 `count`。

## 实现原理

闭包 = **函数指针 + 环境指针**。它记住一条 [[environment|环境链]]，而不是拷贝值。

参见 [[lua-design-philosophy]]：Lua 的 `for` 循环之所以能做成通用且紧凑的形式，正是因为闭包能保留生成器函数在循环之间的内部状态。

## 游戏开发应用

- **事件回调**：按钮 callback 捕获 UI 状态。
- **协程**：Unity 的 IEnumerator 捕获外部状态。
- **延迟执行**：Tween 完成回调、promise 链。

## 陷阱

- **意外捕获**：for 循环里的 lambda 捕获循环变量的**引用**，导致所有 lambda 看到同一值（JavaScript `var` 的经典坑，ES6 `let` 才修复）。
- **内存泄漏**：闭包持有的引用让对象无法 GC——Unity 里的 coroutine 常因 GameObject 被销毁后协程仍持有引用而泄漏。

## 相关

- [[environment]]
- [[lexical-scoping]]
- [[higher-order-functions]]

## Sources

- [[sources/sicp-day02]]
