---
tags: [游戏引擎, 并行, 任务调度, 多线程, bitsquid]
date: 2026-04-19
sources: 1
---

# Bitsquid 任务调度器

[[niklas-frykholm|Niklas Frykholm]] 2010 年写的一套自研调度器，刚把上一版基于 Windows Vista ThreadPool 的实现扔掉。设计目标明确、实现小巧，整套代码几天就写完——这是"[[good-parallel-computer|不要用中间件]]"哲学的一个典型例证。

## 目标

- **甩掉 Vista ThreadPool**，要对 job 线程有完全控制；
- **最小化 context switch**——避免 thread oversubscription；
- **能做到全系统 task 化**：所有代码都跑在 task 里，没有 `wait()`，代码流程完全由依赖图驱动；
- 同时**向后兼容**有 main thread / render thread 的混合模式（从串行 → 完全 task 化是渐进过渡）；
- 支持**外部处理器**（SPU、GPU）；
- 支持**任务的层级分解**——animation 作为一个 task 看，放大能看到 animation 内部又是一张子图。

## Task 数据结构

一个 task 是个简单 POD：

- **work**：要执行的 WorkItem（函数指针 + 数据块，可跑在 CPU / SPU / GPU）；
- **affinity**：必须绑定到特定线程（比如 render thread）的 hint；
- **parent**：父任务 id。Task 有 "completed = 自己的 work 跑完 + 所有子 task 跑完"这个定义，用 `open_work_items` 计数器实现；
- **dependency**：**单个**依赖任务。不支持数组——为了让结构保持 POD；
- **priority**：可用来排序。

**单依赖不是限制**：想依赖多个，就加一个空 work 的"anonymous task"把那些依赖当子任务挂上去，然后依赖这个 anonymous task——它跑完就代表所有子任务跑完。

## 开放表（Open List）

Bitsquid 不显式追踪"completed task"，而是维护一个**所有未完成 task 的列表（open list）**——不在 open list 里的 id 就视作完成。这张表和"待执行的 work queue"是**分开**的：

- work 被调度到 worker 线程时 → 从 **queue** 里移除；
- task 真正完成（所有子任务都跑完）时 → 从 **open list** 里移除。

## 线程模型

总线程数 = `CPU core 数`：

```
worker_thread_count = number_of_cores - main_thread_count
```

**main thread**（比如 update 和 render 两条）跑自己串行代码，可以随时创建 task。它们也有 `wait()`——但**wait 不 sleep**，而是转去帮 task manager 消化任务，直到自己等的那个 task 完成才返回（见 [[main-thread-task-injection]]）。

**worker thread** 空闲时 sleep，有新 task 时被叫醒。

只要任务够多、同步点够少，**所有线程要么在跑自己的串行代码、要么在跑 task——100% 核心利用率**。

## Immediate-mode 任务图

Bitsquid 不提倡"预构建静态 task graph"。取而代之的是**每一帧动态创建 task + 依赖**：

```c
void World::update() {
    TaskId animation   = _tasks->add(animation_task(_animation));
    TaskId scene_graph = _tasks->add(scene_graph_task(_scene_graph));
    _tasks->depends_on(scene_graph, animation);

    TaskId gui = _tasks->add(gui_task(_gui));

    TaskId gui_scene = _tasks->add_empty();
    _tasks->add_child(gui_scene, scene_graph);
    _tasks->add_child(gui_scene, gui);

    TaskId render = _tasks->add(render_task(this));
    _tasks->depends_on(render, gui_scene);

    TaskId sound = _tasks->add(sound_update_task(_sound));

    TaskId done = _tasks->add_empty();
    _tasks->add_child(done, render);
    _tasks->add_child(done, sound);

    _tasks->wait(done);
}
```

这种 "immediate-mode" 写法比静态图更贴合实际代码——代码本来就有分支、虚调用，根本不是静态调用图。

## `begin_add` / `finish_add` 原子性

评论里 Bjoern Knafla 抠了一个 race：当你 `add(task_a)` 后立刻 `depends_on(task_b, task_a)`，假如 `task_a` 在 `depends_on` 之前就被 worker 抢跑完了会怎样？

Frykholm 的回答是：真实 API 是 `begin_add()` / `finish_add()` 两段式——`begin_add()` 把 task 放进 queue 和 open list，但 **open_work_items 被初始化成 2 而不是 1**。这样即使 worker 跑完 work，计数器也只到 1，不会触发 completion。调用者可以安心地 `depends_on` / `add_child`。最后 `finish_add()` 把计数器减 1，这时候才允许完成。

## 优先级 vs 关键路径

理论上要跑得最快，每帧都应该算**关键路径**、动态调整优先级。但：

- 不同场景关键路径差别大（渲染 bound 还是 CPU bound）；
- 动态调整让 profile / debug 变难、系统更难推理。

Frykholm 选了更简单的做法：**每个 job 有静态 priority**，调度时取优先级最高的；**priority 由游戏配置，不由引擎写死**（不同游戏的瓶颈不同，让集成引擎的团队按自己负载调）。详见 [[worker-task-dispatch-priority]]。

## 全局 queue，不做 work-stealing

所有 task 进**一个全局 queue**，worker 从这里抓。Frykholm 故意没做 per-thread queue 和 work-stealing，理由是：

- 当前任务粒度每个 heavy job 最多切到 `5 × thread_count` 份，这个粒度下**全局 queue 不会成瓶颈**；
- 更细粒度不会提高核心利用率；
- 真要 >32 核了，再考虑 lock-free global queue。

Queue 后来从 ring buffer 升级成 **priority queue（heap-backed）**。依赖未满足的 task 放在 "holding area" 不入队；affinity task 进**per-thread queue**。

## 未实现的优化：idempotent re-execution

OS 有时会把某个关键路径上的 task 挂起，整个图被拖慢。Frykholm 有个设想：**如果 task 是纯函数（idempotent）**，就允许多个线程同时跑同一份 task——任何一个跑完就释放依赖。没实现，因为会引出"一份跑完"和"全部跑完"两种完成状态，模型变复杂；而且 Bitsquid 的瓶颈平台不在 PC。

## 长任务怎么办

长任务分两类：

- **外部等待型**（网络、文件 IO）：调度器不管，由对应 manager 每帧轮询；
- **长计算型**（比如重建 AI 导航图）：切成 chunk，每帧排一个 chunk task，做负载均衡。

## 为什么不用 TBB

评论里有人问为什么不直接用 Intel TBB。Frykholm 的反答被很多引擎团队引用：

- 中间件**不会做得刚好是你要的**；
- 用中间件等于你要理解"原问题 + 中间件对这个问题的前设"两层；
- 中间件带着一套**它假设你会怎么用**的 API，会让你的代码变僵；
- 代码量大、互相耦合，想只拿一部分出来难；
- 文档往往不够好。

更直接的一句话是：**这类需要深理解 + 极致控制 + 问题本身不大的系统，自己写更清楚**。他点名 Lua 是少数的例外——"implementation 漂亮、API 也好"。

## 相关

- [[worker-task-dispatch-priority]] — 同一时期别的引擎在调度 priority 上的做法
- [[main-thread-task-injection]] — main thread `wait()` 时帮忙处理任务的模式
- [[cpu-scheduler-design]] — 调度器设计的一般讨论
- [[good-parallel-computer]] — 任务粒度与硬件假设
- [[fiber-cpp-basics]] — 后来的协程 / fiber 方案可以看作对这篇设计的扩展

## Sources

- [[sources/bitsquid-task-management-practical]]
