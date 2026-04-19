---
tags: [c++20, 协程, 运行时, 内存]
date: 2026-04-19
sources: 1
---

# Stackless vs Stackful 协程：为什么我们从来不需要整栈保存

协程（coroutine）的核心是「函数中途挂起、以后再恢复」。实现层有两种完全不同的姿势：

- **Stackful**（有栈协程）：每个协程独占一整条调用栈；挂起时把当前栈指针、寄存器、通常还有完整栈帧保存下来，恢复时换回去。Windows Fibers、Boost.Fiber、Linux `ucontext`、古代 MacOS Thread Manager 都属于这一类——本质就是「用户态线程」。好处是**可以在任何调用深度挂起**，哪怕挂起点在第十层普通函数内部。代价是：每个协程必须为可能的最大栈深度预留内存（MB 级别 guard page，或至少几十 KB），N 个并发协程带来 N × stack 的常驻内存；上下文切换要搬一批寄存器；编译器无法看穿栈上的状态做优化。
- **Stackless**（无栈协程）：C++20 选择的路线。编译器把 `co_await` / `co_yield` 所在的函数改写成一个状态机对象，**只保存跨挂起点需要活着的局部变量**（那些在 `co_await` 两侧都被用到的）。挂起发生时不需要搬栈——因为此刻函数的「栈帧」其实就是堆上那个状态机对象的字段。

Stackless 的限制听起来很严苛：**只能在协程自己的函数体里挂起**。普通函数调用链上一个 C 风格函数没法替协程喊「我要 yield」——它没有挂起所需的状态机改写。

## Supnik 的反驳：这个限制其实不痛

Ben Supnik 指出，这个限制在实际工程里并不是问题，因为它形成了一个干净的分层：

1. **协程调用普通函数**：普通函数没有挂起点，根本不会要求保存栈——问题自动消失。
2. **协程调用协程**：语法上不是 `call`，而是 `co_await child()`。子协程一旦挂起，父协程早就因为 `co_await` 自己挂在那里了，根本不在「栈」上。

关键机制是 [[coroutine-awaitable-pattern|awaitable 做返回地址跳板]]：子协程在启动时拿到父协程的 `coroutine_handle` 存在自己的 promise 里，子协程真正跑完时，它的 `final_suspend` 返回这个父 handle，于是执行流跳回父协程——等价于一次 `ret` 弹栈。

> 「stackless 不是缺失整栈的残废版，而是把栈的职责交给了 await 链和 heap。整个调用关系被拍成一组 promise 对象串在堆上，而不是一条物理栈。」

## 代价对比

| 维度 | Stackful | Stackless (C++20) |
|---|---|---|
| 单协程内存 | 整个栈（>= 几 KB 到 MB） | 只存真正跨挂起点的变量，通常几十到几百字节 |
| 并发数 | 受总内存限制，几千量级 | 几十万到百万协程可行（典型 async 服务器） |
| 挂起位置 | 任意调用深度 | 只能在 `co_await` 所在函数 |
| 上下文切换 | 保存/恢复寄存器和栈指针 | 零切换——本质是状态机方法调用 |
| 与编译器优化 | 黑盒：栈内容不可见 | 透明：状态机内所有变量都是常规字段，正常 inline / const-fold |
| 跨线程调度 | 天然支持 | 也支持，但要在 awaitable 里处理 |

## 什么时候真的需要 Stackful

- 需要劫持**已经写好的同步库**（例如阻塞 I/O 的第三方 API）而又不改源码——Fiber 可以在任何位置硬 yield。
- 把**已有的深度递归 DFS** 改成可挂起的搜索器——把算法拆成状态机太痛苦。
- 用作**用户态抢占式调度器**的基础（Go 的 goroutine 走的是这条路，但 Go 有 runtime 栈可增长不需要预留）。

如果你的代码本来就能写成 `async/await` 风格的协程——I/O、任务调度、生成器、异步流——**Stackless 是碾压性的选择**。Supnik 在 X-Plane 的 async 层里就是这个判断。

## 相关

- [[coroutine-awaitable-pattern]] — stackless 挂起/恢复的实际机制
- [[closure]] — 状态机本质也是一次自动闭包化
- [[go-goroutine-channels]] — Go 的 goroutine 采用可增长栈的另一路径
- [[ltask-scheduler]] — Lua 侧基于 stackful coroutine 的任务调度
- [[ben-supnik]]

## Sources

- [[sources/supnik-stackless-vs-stackful-coroutines]]
