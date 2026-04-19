---
tags: [source, c++20, 协程, 异步]
date: 2026-04-19
sources: 1
---

# A Coroutine Can Be An Awaitable（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 6 月的 C++20 协程系列第五篇（也是收尾篇）。

## 摘要

作者把 awaitable 和 coroutine 的关系拆成最简单的一句话：awaitable 是**名词**（一个"可以等待"的事件源）、coroutine 是**动词**（做等待这件事的可挂起代码）。协程有终点，所以"协程结束"本身就是一个 awaitable 事件——这意味着**协程可以当作 awaitable 被另一个协程等**。把协程做成 awaitable 需要两步：给它实现 `co_await` 运算符，让编译器知道如何构造协调挂起的 awaitable；并在 `final_suspend` 里归还父 handle，让父协程在子协程完成后自动恢复。作者同时指出并非所有协程都必须 awaitable——他在 X-Plane 里写过 "fire and forget" 顶层协程：跑完自毁，不给任何调用者等待的机会，结果通过其他回调机制回传。

## 关键要点

- awaitable 是"事件源"，协程是"执行载体"，两者并不相等但可相互组合。
- 协程成为 awaitable 的两个条件：`operator co_await` 和 "唤醒调用方的机制"。
- Task 类型典型模式：`initial_suspend` 挂起、`final_suspend` `resume` 存好的父 handle。
- 不需要被等的协程可直接 `suspend_never` 加自毁。

## 链接到的概念

- [[coroutine-awaitable-pattern]]
- [[stackless-vs-stackful-coroutines]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2021/06/a-coroutine-can-be-awaitable.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-06-21_a-coroutine-can-be-awaitable.md`
