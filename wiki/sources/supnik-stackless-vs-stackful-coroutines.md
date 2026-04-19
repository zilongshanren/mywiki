---
tags: [source, c++20, 协程, x-plane]
date: 2026-04-19
sources: 1
---

# We Never Needed Stackfull Coroutines（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 6 月的 C++20 协程系列第四篇，主题是：为什么从 Fibers / ucontext 习惯过来的人不必怀念「整栈保存」。

## 摘要

作者用自己早年写 MacOS Thread Manager 的经验开场——那时候 fibers 是"有栈协程"，yield 时要保存整个物理栈。C++20 协程改走 stackless 路线：挂起点只能在协程函数体内、编译器把协程改写成状态机，只保留跨挂起点的变量。他最初以为会怀念整栈保存，然后发现根本不需要：(1) 协程调用普通函数不会要求挂起；(2) 协程"调用"协程实际是 `co_await`，子协程启动时把父 `coroutine_handle` 存进自己的 promise，结束时 `final_suspend` 把父 handle 交还——等价于一次 `ret` 弹栈，完全不需要物理栈的参与。于是 stackless 把"栈"的职责交给了 await 链 + heap，换来了更低的单协程内存开销与更好的编译器可见性。

## 关键要点

- stackful（Fibers、Boost.Fiber、`ucontext`）每个协程持有整条栈，挂起时整体保存；stackless 只保存跨挂起变量。
- C++20 的约束"只能在协程体内挂起"在实践中不痛，因为调用链被折叠成 await 链。
- `final_suspend` 把父 handle 返回 / `resume` 就实现了返回跳转。
- Supnik 的结论：从 Fiber 迁 C++20 协程不会丢能力，反而得到更好的并发密度。

## 链接到的概念

- [[stackless-vs-stackful-coroutines]]
- [[coroutine-awaitable-pattern]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2021/06/we-never-needed-stackfull-coroutines.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-06-20_we-never-needed-stackfull-coroutines.md`
