---
tags: [source, 并发, 任务调度, 主线程, 事件循环, lua-coroutine, wasm, soluna, cloudwu, 中文博客]
date: 2026-04-19
sources: 1
---

# 嵌入主线程消息循环的任务调度器（云风 / blog.codingnow.com）

[[cloudwu|云风]] 发表于 2025 年 11 月的设计笔记，记录把 [[soluna-2d-engine|soluna]] 移植到 wasm 与 Linux-OpenGL 时遇到的主线程-任务调度器矛盾及其解法。

## 摘要

soluna 基于 [[ltask-scheduler|ltask]] 多线程调度器。图形后端 sokol 不是线程安全的，原设计把所有图形 API 塞进一个 render 服务，用信号量和主线程 sokol 回调同步。D3D / Metal / Vulkan 能忍，但 **OpenGL 把 context 绑在当前线程**、**wasm 要求 canvas/WebGL 调用必须在主线程**，让这个方案无法成立。

解法是把 2022 年"多线程串行运行 Lua VM"的思路推广一次：不是改造 ltask 让主线程伪装成特殊工作线程（复杂度太高），而是**给调度器打一个受控例外洞**——Lua 侧在启动"必须主线程执行"的任务前通知调度器把该虚拟机暂时移出调度表，主线程事件回调通过信号量接手该 coroutine 的特定片段执行，完成后再归还给调度器。**同一个 Lua coroutine 的上半段跑在工作线程、下半段跑在主线程**——这在纯 C 几乎做不到，因为 C 栈绑定线程；Lua coroutine 栈在堆上不依赖 C 栈，天然支持跨线程续跑。

wasm 上原本想用 web worker API，但 worker 不能直接访问 DOM / WebGL，所有 IO 都得转发主线程——正是 wasm pthread 要解决的问题，用 worker 等于把问题搬回来。最终选 pthread + 主线程任务注入。

文末记录一个边角 bug：主线程执行完特殊任务后只把任务推回线程安全队列是不够的——如果 ltask 所有工作线程都已休眠，光入队不会唤醒它们，必须显式唤醒调度器。

## 关键要点

- OpenGL context 绑线程、wasm canvas 必须主线程 → 信号量同步方案失效
- 不改调度器模型，而是给调度器开可控例外通道
- Lua coroutine 栈在堆上，支持跨线程续跑——纯 C 做不到
- Web worker 不能直接访问 DOM / WebGL，转发层成本太高
- 调度器休眠状态下的任务入队必须伴随唤醒
- 与 2022 年"多线程串行运行 Lua VM"同构，都是利用 Lua VM 解耦 C 栈

## 链接到的概念

- [[cloudwu]]
- [[ltask-scheduler]]
- [[soluna-2d-engine]]
- [[main-thread-task-injection]]

## 原文

- 链接：https://blog.codingnow.com/2025/11/task_schedule_in_eventloop.html
- 本地：`raw/articles/blog.codingnow.com/2025-11-22_yun-feng-de-blog.md`
