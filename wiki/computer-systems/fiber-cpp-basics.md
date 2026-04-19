---
tags: [计算机系统, 多任务, 并发, C++, 游戏引擎, 协程, 调度]
date: 2026-04-19
sources: 1
---

# C++ Fiber：从 preemptive 到 cooperative 的一跳

Fiber 相比 coroutine 更冷门，但在 AAA 游戏 job system 里扮演关键角色——最著名的公开案例是 Naughty Dog 引擎（Christian Gyrling, GDC 2015）。[[graphics-guy-notes|Jiayin Cao]] 写了一篇基础教程 "Fiber in C++: Understanding the Basics"，把 fiber 的**动机、与 thread/coroutine 的差异、x64 上的最小实现**一次讲完。本页是要点摘录。

## 动机：preemptive multitasking 在游戏里的尴尬

主流 OS 的抢占式多任务（时间片轮转 + 内核调度）在游戏开发里有几处痛：

- **context switch 频率不可控**：要进内核态，代价不低，大量切换是被动的。
- **调度器对游戏无知**：线程优先级之外，程序员几乎管不了下一个谁上。
- **等待 I/O 或依赖 job 结果时没有"体面"的让出机制**：
  - 给线程池排更多线程、让 OS 调度 → OS 不知道输入何时 ready，会反复唤醒白费资源；若池里全部在等，易死锁。
  - Job nesting（在当前调用栈上跑别的 job）→ 栈层层嵌套，底下的 job 先完成不了。
  - 把 job 从等待点一切为二 → 等待点变多时不可扩展。

根源是：**preemptive 模式不允许任务主动 yield 而不付大代价**。

## Cooperative multitasking 的另一条路

让程序员接管调度，任务之间互相信任：只要我在合理的点 yield，就不需要 OS 来打断我。`coroutine` 是这条路上最常见的武器，`fiber` 是另一条。

- **Subroutine**（函数）：被调、返回。
- **Coroutine**：除 subroutine 的能力外，可在执行中挂起并把控制交还调用者，之后在另一个线程上从挂起点续跑。
- **Fiber**：可以视为**有栈协程**（stackful coroutine）的一种 OS/assembly 级实现。C++ 语言层从 C++20 开始支持**无栈协程**，而 fiber 通常靠 OS API 或自己写汇编。

## Fiber vs Thread

| 维度 | Thread | Fiber |
|---|---|---|
| 调度方 | OS（抢占） | 程序员（协作） |
| 运行在 | 物理核 | 线程之上 |
| 切换代价 | 内核态切换 | 仅仅几十条寄存器保存/恢复 |
| 栈内存 | OS 管 | 程序员自己分配 |
| TLS 安全 | 是 | 不一定（恢复到别的线程就废） |
| OS 同步原语 | 可用 | 不一定安全（跨线程恢复后 mutex 归属问题） |

## Fiber vs C++20 Coroutine

关键的"致命差异"有两条：

1. **对称 vs 非对称**：C++20 coroutine 是非对称的，yield 只能回到 caller；fiber 是对称的，可以 yield 给任意另一个 fiber。job system 里想做"当前 job 等 A、直接切到 job B"就需要对称。
2. **stackful vs stackless**：C++ coroutine 是 stackless，只能在 coroutine 函数自身里 yield；fiber 可在**任意深度的调用栈里** yield。后者对于 job system 的自然编程风格（"我在业务函数第 5 层发现需要等，就挂起"）几乎是必需的。

其他差异：coroutine 可以 return 值、生命周期结束会析构局部变量；fiber 没有返回值的概念，局部变量不会自动销毁（**容易泄漏**，尤其是 smart pointer 持有的堆内存，因为 fiber 被杀时栈并未正常退出）；coroutine 内存布局由编译器管，fiber 的栈需程序员自行分配。

## 最小 fiber 实现的关键

作者以 x64 + System V ABI 为例给出实现思路：

- x64 有 16 个 64 位通用寄存器（`RAX..R15`）+ `RIP`；SSE2/AVX/AVX-512 分别带来 `XMM/YMM/ZMM` 寄存器组。
- fiber 的 "switch" 本质：把当前 CPU 的寄存器集保存到旧 fiber 的 context，把新 fiber 的 context 载回寄存器（包括 `RSP` 与 `RIP`），CPU 自动从新栈 / 新指令继续。
- ABI 会指定哪些是 callee-saved、哪些是 caller-saved——fiber switch 只需保存 callee-saved 即可（与正常函数调用约定一致）。
- fiber 入口函数没有"正常返回地址"，所以不能靠 return 结束，需要约定一个显式的终止机制。
- 栈内存由程序员自己 `malloc` 出来，充当 fiber 的私有栈。
- arm64 的实现高度对称，主要差异是寄存器集不同。

实现总代码几百行汇编 + C++ 足矣——代码量与威力的比很划算。

## 典型使用模式：游戏引擎 job system

- 线程池大小 ≈ 物理核数，用 thread affinity 钉在 CPU 上；另加少量低优先级线程处理 I/O 等阻塞操作。
- job 包装成 fiber，每个 fiber 自带栈。
- 调度器在合适的线程上把 fiber 拉起；fiber 在 wait 点显式 yield，调度器再挑下一个 ready fiber。
- 跨线程恢复 fiber 的能力让"等待点自然编程"成为可能——这是 cooperative + stackful + symmetric 的共同馈赠。

注意事项：

- **同步原语要自己造**（fiber-aware mutex/condition），OS 的 mutex 不能跨线程恢复。
- **TLS 几乎不能用**，否则 fiber 被搬到别的线程就全乱。
- **析构时机完全是你的责任**——fiber 作为"非正常退出的函数"不会帮你 unwind 栈。

## 相关

- C++20 stackless coroutine 相关讨论见 [[stackless-vs-stackful-coroutines]] 与 [[coroutine-awaitable-pattern]]。

## Sources

- [[sources/graphics-guy-fiber-cpp-basics]]
