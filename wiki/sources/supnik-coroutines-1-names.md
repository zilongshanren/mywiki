---
tags: [source, c++20, 协程, promise_type]
date: 2026-04-27
sources: 1
---

# C++ Coroutines - Getting Past the Names（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 6 月的 C++20 协程系列第一篇，批评 `promise_type` 的命名并厘清其真实职责。

## 摘要

作者对 C++20 协程语言特性总体正面，但对 `promise_type` 这个名称表示不满——它与 C++11 的 promise/future 几乎无关，更准确的名称应该是"traits"或"control block"。`promise_type` 真正控制三件事：协程的生命周期起止策略（`initial_suspend` / `final_suspend`）、生命周期节点的 CPU 控制流（awaitables 允许在此时跳转到任意协程）、以及调用方拿到的 handle 类型。文章作为系列入口，为后续四篇奠定术语基础。

## 关键要点

- `promise_type` 是 control block，不是异步承诺
- `initial_suspend`：决定协程创建后是否立即跑还是先挂起
- `final_suspend`：决定协程结束后是否自毁还是等待外部清理
- promise_type 内嵌于返回类型（如 `task<T>::promise_type`）是表达关联关系的惯用法
- 野西部时代：标准库尚无统一的协程辅助库，作者选择自己实现

## 链接到的概念

- [[cpp-coroutine-promise-type]]
- [[coroutine-awaitable-pattern]]
- [[stackless-vs-stackful-coroutines]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2021/06/c-coroutines-getting-past-names.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-06-17_c-coroutines-getting-past-the-names.md`
