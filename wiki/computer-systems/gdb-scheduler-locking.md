---
tags: [debugging, threading, gdb, tooling]
date: 2026-04-19
sources: 1
---

# gdb scheduler-locking：多线程调试里的定点麻醉

在多线程程序里断点下来，第一件让人崩溃的事是：**在断点处求值一个表达式，会让整个进程跑起来**。Supnik 2011 年的小记录给出了一个典型场景：他命中断点后想打印一个 `std::vector` 某个元素的值，但 `operator[]` 在 debug build 里其实是一次带越界检查的函数调用。gdb 为了执行这个调用，必须让应用线程短暂「活」过去；而在这个瞬间，X-Plane 的其他工作线程也一起被放开，哪个线程先撞上下一个断点，gdb 就停在哪一个——你看到的 backtrace 很可能是另一个完全无关的线程。

暴力的解决办法是把引擎的线程池开关关到 1（X-Plane 允许通过命令行伪造 CPU 核数），但这会让载入时间难以忍受。

gdb 内置的精确武器是：

```
set scheduler-locking on
set scheduler-locking off
```

开启之后，线程调度器被锁定：只有当前线程可以跑，其他线程保持冻结。这样在断点里对 STL 容器做一长串检查，就不会被别的线程抢断点。Supnik 还顺带提了第三档 `step` 模式——`step` 时锁定、`continue` 时放开——他本人暂没用到。

这个技巧适用范围远不止 C++ STL，本质上任何**在断点上下文里需要求值/调用**的调试动作，都会触发一次隐式的 `continue`，而 scheduler-locking 就是把这次 `continue` 限制在当前线程。与之相关的并发调试技巧还有 [[message-queue-thread-ownership]] 讨论的线程所有权约定，以及工具链层面的 rr / record-replay 思路。

## Sources

- [[sources/supnik-dont-go-anywhere]]
