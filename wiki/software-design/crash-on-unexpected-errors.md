---
tags: [error-handling, api-design, assert, bitsquid]
date: 2026-04-19
sources: 1
---

# Crash fast：对 unexpected error 采用崩溃策略

[[niklas-frykholm]] 在 2012 年《Sensible Error Handling》第 1 篇里把错误分成三类：**unexpected**（调用方无合理办法处理的错，如 null 指针、内存越界、核心资源缺失）、**expected**（调用方必须有计划应对的错，如网络、存档）、**warnings**。对 unexpected 错误，他的结论简短而激进：**立即以尽可能详尽的错误消息崩溃**。

## 为什么崩溃比「优雅降级」更负责

反直觉的一点是：崩溃其实是 API 在对调用方「负全责」。如果不崩，每个调用方都必须额外思考「这个 API 可能怎样失败」，代码被 error-handling 胶水淹没（典型的 `if (err == E_xxx) goto exit` 模式），而且永远覆盖不全——毕竟这些错本来就是「没预期到的」。让 API 在 `file_does_not_exist`、`malformed json`、`invalid arg` 时直接崩，调用方代码才能保持干净：

```cpp
bool exists(const char *path);
Archive open(const char *path);          // 找不到就崩
double parse_json_number(const char *s); // 格式不对就崩
bool is_valid_json_number(const char *s);// 真正可疑的场景再调这个
```

Niklas 反驳另一常见方案——「打一条严厉的错误消息然后假装填好空数据」：程序员花力气去 patch 一个已经错乱的状态，基本是白费，后续还会引发更隐蔽的崩溃；而且任何非强制的错误提示**一定**会被忽略——临 deadline 的时候没人会停下来看。崩溃是不可忽视的，因此 bug 会被优先修。这和 [[zero-tolerance]] 的思路一致：不留缓冲区，就能让问题必须当场解决。

## 异常不是银弹

Niklas 明确反对用 C++ 异常来实现这套：异常抹平了 unexpected 和 expected 的区别，让调用方不得不假设每一行都可能跳走，整个代码库被迫写成 exception-safe；模板里你根本不知道可能抛什么；throw 声明一旦缺失，API 契约就崩坏。崩溃模型的哲学优势是：**代码要么 work，要么根本不跑**——这是一种二元、可预测的约束。

脚本边界是个例外：暴露给 Lua 的接口用 `lua_error()` + 内部冻结替代硬崩，避免脚本能把引擎干掉。

## 崩的时候要给出信息

崩溃本身容易，难的是给出可诊断的错误报告。Bitsquid 的模板：**描述 + 调用栈 + [[error-context-stack|error context]]**。`XASSERT(test, msg, ...)` 宏用 C99 可变参数 macro 包装 printf 风格消息；Windows 上 `StackWalk64` + `Sym*` 拿 call stack；符号翻译虽然麻烦但值得——很多 bug 一眼就能从 stack 诊出，不用每次都挂调试器。

## 相关

- [[error-context-stack]]
- [[minimize-points-and-types-of-failure]]
- [[warnings-as-errors-strategy]]
- [[zero-tolerance]]
- [[automated-test-philosophy]]

## Sources

- [[sources/bitsquid-sensible-error-handling-part-1]]
- [[sources/bitsquid-sensible-error-handling-part-2]]
