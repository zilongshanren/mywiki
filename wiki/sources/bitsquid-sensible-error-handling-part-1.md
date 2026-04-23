---
tags: [source, bitsquid, error-handling, api-design, assert]
date: 2026-04-19
sources: 1
---

# Sensible Error Handling: Part 1（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2012 年 1 月《Sensible Error Handling》三部曲的第一篇，聚焦 **unexpected errors** 的处理哲学：立即崩溃。

## 摘要

先划分错误三类：unexpected（调用方没有合理手段处理的错，例如 null 指针、corrupt state、bundle 缺失）、expected（调用方必须有计划应对，如网络、存档）、warning（不严格错但可疑）。对 unexpected，Niklas 主张 **crash as soon as possible with an informative error message**。理由：如果不崩，每个调用方都要思考 API 可能怎么失败，代码被 error-handling 胶水淹没；而"打条错误消息然后 patch 好"注定失败，因为无法覆盖所有情况，且临 deadline 时没人会停下修。崩溃是不可忽视的强制函数，反而让 bug 最快被处理。他同样不推荐 C++ 异常——它抹平 expected/unexpected 的边界，引入 exception-safe 噪声，templated 代码无法声明。崩溃时要附详尽报告：错误描述（printf 风格的 XASSERT 宏）+ call stack + error context 栈。

## 关键要点

- 三分类：unexpected / expected / warning。
- Unexpected 错误立即 crash，是 API 对调用方"负全责"的表现。
- 函数契约因此更简洁：`Archive open(path)`、`double parse_json_number(s)` 都没 error code。
- 脚本边界用 `lua_error` + 冻结，不直接崩引擎。
- Call stack 翻译虽繁琐但值得：一眼诊断，不用每次挂 debugger。
- [[error-context-stack|ErrorContext]] 用 thread-local 作用域变量栈给深层 assert 加现场。

## 链接到的概念

- [[crash-on-unexpected-errors]]
- [[error-context-stack]]
- [[minimize-points-and-types-of-failure]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/01/sensible-error-handling-part-1.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-01-22_sensible-error-handling-part-1.md`
