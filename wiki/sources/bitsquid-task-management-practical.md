---
tags: [source, bitsquid, 并行, 任务调度]
date: 2026-04-19
sources: 1
---

# Task Management - A Practical Example（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 3 月公开 Bitsquid 新版任务调度器设计，整套实现"几天写完"。

## 摘要

放弃 Vista ThreadPool，自己做一套能做到**全系统 task 化**（无 explicit `wait()`、代码流完全由 task 依赖驱动）、同时向后兼容"main thread + worker"混合模式的调度器。task 是个 POD，四个字段：work item / affinity / parent / 单个 dependency / priority。"单依赖不是限制"——想依赖多个就挂在一个空 work 的 anonymous task 的 children 下。**Open list**（所有未完成 task）和 **work queue**（待执行 work）是两个独立结构。`wait()` 不 sleep——main thread 等的时候反过来去帮 scheduler 消化任务。`begin_add` / `finish_add` 两段式初始化避免了 race。评论里 Frykholm 解释了为什么不用 TBB——中间件让"原问题 + 中间件假设"两层都要理解，代码鲁棒性反而下降。

## 关键要点

- 线程数 = core 数，无 over/undersubscription；
- **Open list** 与 **work queue** 解耦；
- **Immediate-mode task graph**：每帧动态加 task + 依赖，不用静态图；
- 全局 queue，无 work-stealing（粒度到 `5 × thread_count` 就够）；priority queue（heap）做排序；有 holding area 存依赖未满足的 task；affinity 入 per-thread queue；
- **静态优先级**比动态关键路径更好调试；优先级由**游戏**配置，不是引擎写死；
- 设想过 idempotent task 可让多线程同跑以吸收 OS context switch，未实现；
- 长任务拆成 chunk 按帧排；纯外部等待（IO/网络）不入 scheduler，由 manager 轮询。

## 链接到的概念

- [[bitsquid-task-scheduler]]
- [[worker-task-dispatch-priority]]
- [[main-thread-task-injection]]
- [[cpu-scheduler-design]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/03/task-management-practical-example.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-03-25_task-management-a-practical-example.md`
