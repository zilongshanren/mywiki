---
tags: [c++20, 协程, 异步, 抽象]
date: 2026-04-19
sources: 1
---

# Coroutine 与 Awaitable 的关系

C++20 协程里最容易绕晕的是 `awaitable`、`coroutine`、`promise_type`、`coroutine_handle` 这一堆角色的职责划分。Ben Supnik 的总结把问题简化到两句话：

- **Awaitable** 是一个名词——「**可以等待的东西**」：mutex、I/O 子系统、一个下载对象、一个定时器。Awaitable 本质是**事件源**，事件就是「等待结束」。
- **Coroutine** 是一个动词——「**做等待这件事的代码**」。你需要一段代码来触发 `co_await`，等待完成后继续执行；这段代码必须是能被挂起/恢复的协程。

两者的交互规则：`co_await <awaitable>` 把当前协程挂起，awaitable 负责在恰当的时刻把当前协程的 `coroutine_handle` 再 `resume()` 回来。

## 协程本身也能是 Awaitable

关键转折：**协程只要有终点（不是 infinite loop），它的"结束"就是一个可等待的事件**。于是你可以对一个协程写 `co_await some_task()`，让调用者在子任务完成后继续。

要把协程做成 awaitable，只需两步：

1. **提供 `co_await` 运算符**（在协程类型或其 promise 上实现 `operator co_await()`，或直接实现 `await_ready / await_suspend / await_resume`）。这告诉编译器：拿到这个对象后该构造什么 awaitable 来协调挂起。
2. **给调用者一个被唤醒的理由**：在自己的 `final_suspend` 里，把之前存起来的父 `coroutine_handle` 返回/`resume()`——这样子协程结束时，控制权自动飞回父协程。

典型实现：

- Task 构造时 `initial_suspend` 返回 `suspend_always`，所以 task 创建后不立刻跑，而是等被人 `co_await`。
- 父协程执行 `co_await task` 时，awaitable 的 `await_suspend(h)` 把父 handle `h` 存进 task 的 promise，然后 `resume` task 开始执行。
- task 跑到尽头，`final_suspend` 返回一个自定义 awaitable，它在 `await_suspend` 里返回之前存好的父 handle——编译器的 symmetric transfer 规则让父协程接管 CPU，没有 stack 递归。

这个跳板机制解释了 [[stackless-vs-stackful-coroutines|stackless 协程为什么不需要保存完整栈]]：调用链被折叠成一串堆上 promise 的 handle 传递，物理栈只是临时的指令游标。

## 不是所有协程都必须 awaitable

Supnik 在 X-Plane 里还写过**「fire and forget」** 风格的协程：顶层从同步代码启动，跑完自动销毁，不打算让任何调用者 `co_await` 它。这类协程的 `final_suspend` 通常返回 `suspend_never`，让协程帧在结束时自毁。结果的回传靠调用普通回调、往队列投消息等非协程机制完成。

结论：**协程 → awaitable 是能力不是义务**。设计一个协程类型时要问清楚：调用方会不会 `co_await` 我？如果不会，省掉 awaitable 的机器；如果会，就得实现上面那两步。

## 与其他异步抽象的对比

| 抽象 | 事件源（awaitable） | 执行载体（coroutine） |
|---|---|---|
| C++20 | 任意实现 `operator co_await` 的对象 | `co_await/co_yield/co_return` 函数 |
| JavaScript | `Promise` | `async function` |
| Rust | `Future` trait | `async fn` / `.await` |
| Go | 隐式（channel/select） | goroutine |

四种语言里除了 Go（走 [[go-goroutine-channels|CSP + runtime 调度]]）外，本质都是同一组分工：**有个被动的"事件对象"描述等待条件，有个主动的"协程函数"在等待结束时推进状态**。理解这一划分后，阅读任何异步代码都会顺畅很多。

## 相关

- [[stackless-vs-stackful-coroutines]]
- [[closure]]
- [[go-goroutine-channels]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-coroutine-as-awaitable]]
