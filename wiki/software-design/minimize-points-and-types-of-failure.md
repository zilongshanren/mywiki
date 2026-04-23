---
tags: [error-handling, api-design, bitsquid]
date: 2026-04-19
sources: 1
---

# 最小化失败点与失败类型：expected error 的 API 设计

对 [[crash-on-unexpected-errors|unexpected 错误]] 可以一崩了之，但网络、存档、可插拔硬件这些场景里，错误是业务的一部分，**调用方必须有计划**——这就是 [[niklas-frykholm]] 所说的 *expected error*。Bitsquid 的原则只有一句：

> **Minimize the points and types of failures.**

API 抽象 functionality 时是把低层调用合成高层概念；处理 expected error 也应当对称——把底层一堆杂乱的 failure state 抽成少数几个定义清晰的高层 failure。

## Points：让能失败的函数尽量少

反例是 `enumerate() / open() / read() / close()` 每个都返回一个 error code——调用方要在四处检查，各种路径分支爆炸。Bitsquid 的 save system 只有 `load_result(id)` 这一个函数可能返回失败：

```cpp
enum LoadResult { IN_PROGRESS, COMPLETED, FAILED };
unsigned num_saved_games();
LoadId start_loading_game(unsigned i);
LoadResult load_result(LoadId id);
Data loaded_data(LoadId id);
void free_data(LoadId id);
```

其余所有函数要么不会失败（不会失败的路径直接走 [[crash-on-unexpected-errors|crash]]），要么将错误收敛到唯一的查询点。这样调用方只在一处写错误处理。

## Types：失败形态要少且具体

别返回能取 40 亿种值、语义又模糊的通用 `int` error code——`EWOULDBLOCK` 和 `EAGAIN` 到底什么区别？`GetOverlappedResult` 的全家桶更是灾难。Niklas 的替代方案：多数情况 `true/false` + 日志足够；需要区分失败原因时，**每个函数定义一个自己的小 enum**：

```cpp
enum LoadResult {
    IN_PROGRESS, COMPLETED,
    FILE_NOT_FOUND, FILE_COULD_NOT_BE_READ, FILE_CORRUPTED
};
```

调用方一眼就能验证自己是否 cover 了所有分支。

## 别抗拒多返回值

C 程序员有时对「返回一个 struct」过敏，习惯把第二个返回值塞进 out-parameter：`const char *loaded_data(unsigned &len)`。这属于历史惯性——现代 ABI 把 8 字节结构直接放寄存器返回，几乎零成本。正确写法是：

```cpp
struct SaveResult {
    enum { NO_ERROR, DISK_FULL, WRITE_ERROR } error;
    unsigned saved_bytes;
};
SaveResult save_result(SaveId id);
```

把错误码和业务数据作为**一个值**返回，代码干净、语义清楚。

## 与异常的对比

Niklas 不用 C++ 异常处理 expected error，主要反对意见有三点：异常不在类型签名里，API 契约不完整；加上 `throw()` 声明后，templated 代码几乎没法用；异常在**每一行**都可能发生，要求你写 exception-safe 代码，成本太高。错误码虽然古老，但配合「少失败点 + 函数级 enum + struct 返回」三条规则，恰恰是**显式、可审计、可读**的——这就是 Bitsquid 回到错误码的理由。

## 相关

- [[crash-on-unexpected-errors]]
- [[error-context-stack]]
- [[warnings-as-errors-strategy]]
- [[interface-vs-implementation]]

## Sources

- [[sources/bitsquid-sensible-error-handling-part-2]]
