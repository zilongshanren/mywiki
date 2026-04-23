---
tags: [游戏引擎, 多线程, 并发, lua, actor-model, bitsquid]
date: 2026-04-19
sources: 1
---

# Gameplay 并发：Actor model + per-API lock

"让 gameplay 程序员写 mutex/lock/atomic 的 C++"在工程现实里是糟糕设定——gameplay 代码"乱、碎、常改"，同步原语越多越难 debug。[[niklas-frykholm|Niklas Frykholm]] 2015 年重访这个问题，给出一个偏向[[actor-model-for-gameplay|Actor model]]的方案：多个 Lua VM 每核一个，互相走异步消息；要访问引擎 API 就按 **API 粒度显式 lock**，用 Lua coroutine 切换避免 OS 线程阻塞。

## 为什么传统多线程不适合 gameplay

三条困难由作者概括：**(1)** 锁 / 原子 / 信号量写不易读更不易（尤其对 gameplay 这种"messy"代码），实验迭代频繁的场景和同步严谨相抵触；**(2)** gameplay 涉及所有子系统（physics、input、UI、audio……），找不到 engine 那样集中可切片的 hotspot；**(3)** Lua 这类脚本语言不原生支持多线程——让 gameplay 程序员下沉写 C++ 基本等于放弃脚本层。

[[amdahls-law|Amdahl 定律]]的现实压力不可回避：硬件核心数线性上升，任何还串行的部分最后都会成为瓶颈。

## Actor model + Lua VM

每个 Lua VM 只操作自己的本地内存，彼此通过异步消息通信——无共享内存，不需要显式同步。Bitsquid 的想法是 **每个核跑一个 worker VM** + 一个主 VM。简单的 `{ 'factor', n }` 任务分发很干净，但真实 gameplay 根本不是这样——它频繁打 `PhysicsWorld.raycast()`、挪 unit、读 unit 位置，**反复穿越到引擎那团 mutable state 里**。

把所有引擎 API 加 critical section 会让多线程收益归零。

## 折中：API 粒度显式 lock

作者的提议是改变"同步粒度"：不再对每个 API 调用加锁，而是让用户在一次使用开始/结束显式 lock：

```
Unit = LuaThreads.lock_api("Unit", player, LockType.WRITE)
Unit.set_position(0, Vector3(0,0,0))
-- 对 player 做更多 Unit 操作
LuaThreads.unlock_api(Unit)
```

几个关键约束：

- worker Lua VM **开局白板**——除了纯函数 API 外什么也没有，想做事必须先 lock 一个 API；
- lock 可以窄到 per-entity（上例里 `Unit` table 仅对 `player` 合法）；
- 遇到 API 已被别的 worker 占用时，用 [[lua-runtime-dynamism-tricks|Lua coroutine]] **切换到另一个 worker**——协程意义下等锁，不阻塞 OS 线程；
- 主 Lua thread 仍"特殊"：worker 跑时主挂起，worker 做完主恢复收集结果。作者承认这不完美——主线程期间没法继续工作损失了一部分并行度。

## 其他候选与反驳

评论区两条替代值得对比：

- **Double buffer**：每帧发一份 **read-only snapshot** 给 gameplay 看——gameplay 只读，engine 单方面写下一帧。不用显式 lock，代价是内存与一帧延迟。
- **Enqueue + callback**：raycast 之类从同步改成"排队请求、下一帧发结果"。降低耦合，但引入一帧延迟。

作者对**纯 event-driven** 方案有明确反驳：如果决策链涉及多个 event（AI 打 ray、根据命中发 health 查询、根据 health 发决策……），10 步链 = 20 帧延迟；而且同时在 flight 的 event 会让系统"看不清现在在算啥"，target entity 被杀掉时每个系统都要处理 abort——复杂度爆炸。

## 风险点

- **Deadlock**：不同 worker 按不同顺序 lock 多个 API，经典交叉锁死；
- **主线程瓶颈**：主 Lua thread 是还没消化的单点；
- **用户依然可能写错**：lock 模型比 per-call lock 容易 reasoning，但不是没抽象泄漏。

## 和其他方案的关系

- [[message-queue-thread-ownership]]：每个子系统持一个 incoming queue、外部通过消息访问——是"把 mutable state 改成 actor"的硬路线。Bitsquid 的方案更务实，引擎内部仍是传统 mutable state，只在 Lua 层面套 actor 外壳；
- [[main-thread-task-injection]]：另一种折中——gameplay 串行在主线程，把 pure 任务 spawn 出去——适合引擎已深度单线程的老系统。
- [[bitsquid-data-oriented-entity-system]]：Bitsquid 的 SoA component manager 本身对并行极友好（每类 component 一块数据），但 Lua 层的 gameplay 访问是另一问题域。
- [[bitsquid-task-scheduler]]：Bitsquid 自己的任务调度器把 engine 子系统的并行已经拿下——本文面对的是**脚本层并行**这个独立问题。

## 相关

- [[amdahls-law]] — 单线程占比决定上限
- [[lua-runtime-dynamism-tricks]] — Bitsquid 把 Lua 用到的各种 trick，含 coroutine
- [[message-queue-thread-ownership]] — 另一种 actor 化：subsystem 持 inbox
- [[main-thread-task-injection]] — 引擎主循环外注入 worker 任务
- [[bitsquid-task-scheduler]] — engine 层任务并行
- [[vfx-multithreading-patterns]]

## Sources

- [[sources/bitsquid-multithreaded-gameplay]]
