---
tags: [source, game-engines, concurrency, async, job-system]
date: 2026-04-27
sources: 1
---

# Asynchronous Job Scheduler（Outerra）

[[people/outerra-team]] 发表于 2010 年 9 月，介绍 Outerra 引擎中 jobmaster 组件的设计动机与架构。

## 摘要

早期 Outerra 使用固定线程数的 job processor，要求 job 代码显式维护状态机，在 I/O 等待时发出"respin"以让出控制权，导致异步代码难以编写，开发者常把 I/O 任务推入同步队列积压。jobmaster 引入协作式上下文挂起（fiber 语义），允许开发者写普通同步代码处理纹理加载、地形数据下载等 I/O 密集操作，同时保证系统利用所有核心。调度器维护"运行/等待 blocking/空闲"三态线程池，N 个线程同时运行（N=核心数），遇到 blocking 时当前线程挂起上下文、转交 CPU 给其他可继续的 job。支持子任务依赖等待，优先调度依赖已就绪的 job。内部用 lock-free 队列与对象池维护状态，避免调度器自身成为锁争用热点。

## 关键要点

- 核心思路：协作式上下文切换，让同步代码在 I/O 等待时自动让出线程。
- 最多 N 个线程同时运行，N 可配置为 CPU 核心数。
- 子任务依赖等待：wait 所有 children 完成，调度器优先调度"就绪"的 job。
- 全 lock-free 调度器内部状态。
- 附带 logger/grapher 组件用于可视化 job 时序和性能问题。

## 链接到的概念

- [[fiber-based-job-scheduler]]
- [[bitsquid-task-scheduler]]

## 原文

- 链接：https://outerra.blogspot.com/2010/09/asynchronous-job-scheduler.html
- 本地：`raw/articles/outerra.blogspot.com/2010-09-26_asynchronous-job-scheduler.md`
