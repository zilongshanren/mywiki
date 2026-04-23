---
tags: [source, bitsquid, error-handling, api-design]
date: 2026-04-19
sources: 1
---

# Sensible Error Handling: Part 2（Niklas Frykholm / Bitsquid）

三部曲第 2 篇，专论 **expected errors**——调用方必须有计划应对的错。

## 摘要

核心原则一句：**minimize the points and types of failures**。API 抽象 functionality 时要把低层操作合成高层概念，处理失败也要对称——把一堆低层 failure state 收敛成少数几个清晰的 high-level failure。Points 层面：别让 `enumerate()/open()/read()/close()` 每个都能失败；示例 SaveSystem 把失败点收敛到唯一的 `load_result(id)` 查询函数，调用方只在一处处理。Types 层面：别用能取 40 亿值、语义重叠的通用 `int` error code（吐槽 `EWOULDBLOCK` vs `EAGAIN`、`GetOverlappedResult`），多数场景 `true/false` + 日志够用；需要区分时每个函数定义自己的小 enum。Niklas 不用异常处理 expected error——契约不在签名里、`throw()` 让 templated 代码难用、每行都可能跳走导致 exception-safe 噪声。错误码被误解的三条理由他都给了反驳：用少失败点压住噪声；用函数级 enum 压住通用性；用 struct 多返回值替代 out-parameter（现代 ABI 把小结构放寄存器返回，成本可忽略）。

## 关键要点

- SaveSystem 示例：一个 failure 查询点 + enum `{IN_PROGRESS, COMPLETED, FAILED}`。
- 结构化返回值是新时代的 error code：`struct SaveResult { enum error; unsigned saved_bytes; }`。
- C 的 out-parameter 惯例在现代 ABI 已无性能理由。
- Java checked / unchecked 的争议其实源自"没区分 expected vs unexpected"。
- 评论里讨论了 NSError 的 domain/code/localized 组合，Niklas 认为人类可读消息应该进日志，而非返回对象。

## 链接到的概念

- [[minimize-points-and-types-of-failure]]
- [[crash-on-unexpected-errors]]
- [[interface-vs-implementation]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/02/sensible-error-handling-part-2.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-02-05_sensible-error-handling-part-2.md`
