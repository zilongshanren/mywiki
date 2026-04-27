---
tags: [source, c++20, 协程, co_await, 异步, continuation]
date: 2026-04-27
sources: 1
---

# co_await is the .then of Coroutines（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 6 月的 C++20 协程系列第三篇，将 `co_await` 类比为 continuation 系统中的 `.then`。

## 摘要

Supnik 用一段对比代码把 `co_await` 的语义一句话讲清楚：在 future/callback 系统里，`.then(lambda)` 表达"在前置操作完成**之后**执行"；`co_await` 做完全相同的事，只是 continuation 被写成直线代码而非嵌套 lambda。两段代码在执行语义上等价——起点都在调用方线程，IO 绑定后让出，IO 完成后在 IO 系统提供的线程上继续。这一对等关系的推论是：任何有"完成后回调"接口的系统都可以包装成 awaitable，包括线程池调度、非阻塞 IO、按需加载对象、串行执行队列（充当非阻塞互斥锁）。文章还提到 `await_suspend` 可拿到调用协程的 `coroutine_handle`，允许把它存入 FIFO 实现调度。

## 关键要点

- `co_await X` = `X.then(rest_of_coroutine)`，语义等价，写法不同
- 凡有 completion callback 的接口均可包装为 awaitable
- 典型 awaitable 类型：线程池、非阻塞 IO、懒加载对象、串行队列
- `await_suspend` 收到调用方的 handle → 可存入 FIFO 实现优先级调度
- 执行线程由 awaitable 的实现决定，协程本身不关心

## 链接到的概念

- [[cpp-coroutine-promise-type]]
- [[coroutine-awaitable-pattern]]
- [[closure]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2021/06/coawait-is-then-of-coroutines.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-06-19_co-await-is-the-then-of-coroutines.md`
