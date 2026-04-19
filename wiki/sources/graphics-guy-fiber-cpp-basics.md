---
tags: [source, 计算机系统, 并发, C++, 协程, 游戏引擎]
date: 2026-04-19
sources: 1
---

# Fiber in C++: Understanding the Basics（A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2023 年 8 月的教程文，系统讲 fiber 的动机、与 thread/coroutine 的差异，以及在 x64（System V ABI）上的最小实现细节；arm64 版本的完整源码挂在 gist。

## 摘要

文章开篇交代为什么 AAA 游戏从 preemptive 多任务转向 cooperative 多任务：OS 抢占式调度 context switch 频繁且不可控、调度器对游戏无知、等 I/O 或 job 依赖时没体面方式 yield；传统补救（加线程池、job nesting、拆任务）各有缺陷。然后对比 thread / C++20 coroutine / fiber：coroutine 是 stackless 且 asymmetric（yield 只能回 caller），无法覆盖 job system 里"在任意深度挂起、yield 到任何另一个 job"的需求，而 fiber 天生 stackful + symmetric。随后以 x64 / System V ABI 为例拆解寄存器集（16 个通用寄存器 + RIP + XMM/YMM/ZMM），说明 fiber switch 本质是一次 callee-saved 寄存器的保存/恢复外加 RSP/RIP 切换；栈内存由程序员自行分配；入口函数没有正常返回地址，需要自建终止机制。最后强调 fiber 的坑：局部变量不会自动析构（smart pointer 易泄漏）、TLS 几乎不能用、OS 同步原语（mutex）跨线程恢复后不安全，需要自造 fiber-aware 同步。

## 关键要点

- Preemptive multitasking 的根本问题：任务不能廉价地主动 yield。
- Cooperative multitasking 要求任务互相信任，"yield at reasonable point"。
- C++20 coroutine 是 stackless + asymmetric；fiber 是 stackful + symmetric，后者对 job system 几乎是必需。
- fiber switch = 保存 callee-saved 寄存器 + 切 RSP/RIP；总量几百行汇编 + C++ 即可。
- 典型 job system 设置：线程数 ≈ 核数 + thread affinity + 少量低优先级 I/O 线程；job 包装成 fiber。
- fiber 的副作用：手动管理析构、自造同步原语、禁用 TLS。
- 关键先例：Naughty Dog 引擎（GDC 2015 Christian Gyrling）用 fiber 做 job system 的成功实践。

## 链接到的概念

- [[fiber-cpp-basics]]
- [[stackless-vs-stackful-coroutines]]
- [[coroutine-awaitable-pattern]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/fiber_in_cpp_understanding_the_basics/
- 本地：`raw/articles/agraphicsguynotes.com/2023-08-26_fiber-in-c-understanding-the-basics.md`
