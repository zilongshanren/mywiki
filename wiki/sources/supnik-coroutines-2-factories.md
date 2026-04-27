---
tags: [source, c++20, 协程, 工厂模式, 异步]
date: 2026-04-27
sources: 1
---

# Coroutines Look Like Factories（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 6 月的 C++20 协程系列第二篇，揭示协程的工厂调用语义。

## 摘要

理解 C++20 协程的关键直觉：你把协程**写**成函数，但调用者把它当作**工厂**使用——每次调用产生一个新的协程实例 handle。文章以最简的 fire-and-forget 类型 `async` 为例：`initial_suspend` 和 `final_suspend` 均为 `suspend_never`，协程自动开始并自动销毁，返回的 handle 无实际意义。调用方可以在循环中多次调用，每次产生一个独立协程并发执行。这与 callback 式 API 等价，但代码可以写成顺序风格。文章也坦承 fire-and-forget 的局限：调用方无法得知操作是否成功，纯发射即忘——适合把旧 callback 代码包装改造，不适合需要错误处理的场景。

## 关键要点

- 协程调用 = 工厂调用：每次返回新的协程 handle
- `suspend_never` × 2 = fire-and-forget，handle 无用
- 调用方循环创建多个协程 → 并发 IO 天然展开
- 协程跑到第一个 `co_await` 即返回控制权给调用方，IO 系统异步推进
- 局限：无法在 fire-and-forget 里传递结果或错误给调用方

## 链接到的概念

- [[cpp-coroutine-promise-type]]
- [[coroutine-awaitable-pattern]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2021/06/coroutines-look-like-factories.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-06-18_coroutines-look-like-factories.md`
