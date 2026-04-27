---
tags: [引擎架构, 并发, 异步, 线程池, job-system]
date: 2026-04-27
sources: 1
---

# 基于 Fiber 的 Job 调度器（Jobmaster 模式）

Outerra 引擎的 jobmaster 是一个**用协程（协作式上下文切换）实现异步 I/O 并行**的 job 调度器，核心目标是让开发者可以用**普通同步代码**编写包含 I/O 等待的异步任务，同时保证系统在等待时不浪费线程资源。

## 动机

早期方案使用固定数量的线程处理 job，并要求 job 代码显式管理状态机、在等待时"respin"让出控制权。这使得包含 I/O 的代码（纹理加载、地形数据下载、BitTorrent 传输）难以编写，开发者常常把异步操作推迟成同步队列，导致积压和卡顿。

## 架构

```
线程池
├── 线程 A：运行 job-X（执行中）
├── 线程 B：等待 job-Y 的 blocking op（挂起）
├── 线程 C：空闲（等待新 job）
└── ...
```

调度器维护三种线程状态：

- **运行中**：线程正在执行 job 代码。
- **等待 blocking 操作**：线程持有 job 上下文但被挂起，等待磁盘/网络/子任务完成。
- **空闲**：无 job 分配，等待新任务。

调度规则：在任意时刻，最多 N 个线程处于运行状态（N = 核心数），确保不竞争 CPU。当运行中的线程遇到 blocking 操作或显式 wait，它挂起自身上下文，检查：是否有其他 job 的 blocking 已完成（优先调度）；或是否有新 job 在队列中等待——无论哪种情况，当前线程挂起，另一 job 占用 CPU slot。

## 关键实现细节

- **lock-free 队列与对象池**：调度器内部状态管理完全无锁，避免调度器本身成为争用热点。
- **子任务依赖等待**：job 可以 spawn 子 job，并 wait 所有子 job 完成。调度器优先唤醒"所有依赖已就绪"的 job，避免线程饥饿。
- **可配置并发度**：N 可在运行时调整为实际核心数，精确匹配硬件。

## 与其他方案的关系

该模式本质上是**M:N 线程模型**的轻量实现——大量 job 映射到少量线程，靠上下文挂起/恢复（fiber 语义）实现并发。它早于 Naughty Dog 2015 年著名的["Parallelizing the Naughty Dog Engine"](https://www.gdcvault.com/play/1022186)纤程作业系统，但思路相同。

与 [[bitsquid-task-scheduler]] 比较：Bitsquid 的调度器强调无 fiber、无 stack switching 的轻量 task 队列，适合纯计算 task；Outerra jobmaster 则专注于包含 I/O blocking 的异步 job，允许协作式挂起。

## 相关

- [[bitsquid-task-scheduler]] — 无 fiber 的轻量 task 队列对比
- [[ltask-scheduler]] — 另一种 coroutine-based 调度器实现
- [[vfx-multithreading-patterns]] — VFX 行业多线程模式概览

## Sources

- [[sources/outerra-async-job-scheduler]]
