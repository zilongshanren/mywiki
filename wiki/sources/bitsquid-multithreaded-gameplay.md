---
tags: [source, 游戏引擎, lua, 多线程, actor-model, bitsquid]
date: 2026-04-19
sources: 1
---

# Multithreaded Gameplay（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2015 年 3 月 10 日再次回到 2009 年就开过头的老题目——gameplay 代码的多线程。文章对线程化 gameplay 的困难给出了一个诚实的总结，并提出了一个 Lua VM 之间用 **Actor model** 通信、需要访问引擎 API 时要**以 API 为粒度显式 lock** 的折中方案。

## 摘要

三条根本困难：**多线程代码难写难读**，对 gameplay 这种"乱"代码更是；**gameplay 分散**无法像 engine hotspot 那样定位再 parallelize；**Lua 不原生支持多线程**。第三条其实被第一条涵盖——让 gameplay 程序员写 `mutex/lock/atomic` C++ 本身就是糟糕设定。

作者的选择是 [[actor-model-for-gameplay|Actor model]]：每个 Lua VM（典型是每核一个）只碰自己的本地内存，互相走异步消息。contrived 例子（每 VM 分摊一组数 factor）可行，但**真实 gameplay 根本不长成那样**——它连续打 `PhysicsWorld.raycast()`、挪 unit、查另一个 unit 的位置，频繁穿越到**一大团 mutable state**（引擎）里。给每个 API 调用加 critical section 会让多线程收益蒸发。

2015 年 GDC 和 [Pixeldiet](http://pixeldiet.se) 的同行讨论后他想到的折中：**以 API 为粒度、在一次使用开始/结束时 lock/unlock**：

```
Unit = LuaThreads.lock_api("Unit", player, LockType.WRITE)
Unit.set_position(0, Vector3(0,0,0))
-- more Unit ops on player
LuaThreads.unlock_api(Unit)
```

worker Lua VM 开局是空白——没 API、只有 pure functional 入口。要做点什么必须先 lock 某个 API（甚至限定到某个具体 entity，返回的 `Unit` table 只对该 entity 合法）。主 Lua thread 保留（负责任务分发），在 worker 执行期间挂起；每次 worker 要 lock 一个已被别人 lock 的 API 时，用 Lua [coroutine](https://en.wikipedia.org/wiki/Coroutine) 切换到另一个 worker，而不是阻塞 OS 线程。

作者自己清楚缺陷：**主 Lua thread 仍是"特殊的一位"**、主线程在 worker 跑时无法继续、容易 deadlock（不同 worker 按不同顺序请求 API）。评论区给出两条值得并读的替代：把涉及的物理状态 **double-buffer** 成 read-only snapshot 给 gameplay 用；或把同步操作改成 **enqueue + callback** 的请求—回调链。Niklas 顺便反驳 event-driven 方案：依赖链长时延迟恐怖（10 步决策 = 20 帧），而且一大堆"飞行中"的 event 让系统难以跟踪，target entity 被杀掉还要每个系统能处理 abort。

2015 年这篇没给出"定稿"——作者明说他要开始 tinkering。但这是他**经过几年反复**后愿意押注的模型，比之前若干次半推半就的尝试都更接近可落地。

## 关键要点

- 三条困难：lock/atomic 难写、gameplay 太散、Lua 无原生多线程
- gameplay 代码频繁穿越到"大团 mutable state"——per-call critical section 杀性能
- 选 Actor model：多 Lua VM，本地内存 + 异步消息——无共享无锁
- 但真实 gameplay 必须访问引擎，所以引入 **per-API lock**（甚至 per-entity lock）
- Worker Lua VM 开局空白——要么 lock API，要么只用 pure functional
- 用 [[lua-runtime-dynamism-tricks|Lua coroutine]] 做"等不到锁就切下一个协程"，不阻塞 OS 线程
- 仍有主 Lua thread 这一"特殊位"——还没完美
- 风险：不同 worker 按不同顺序请求 API → deadlock
- 评论区替代：double-buffer read-only snapshot、enqueue + callback
- 作者反驳 event-driven：决策链长时延迟爆炸、"飞行中" event 难跟踪

## 链接到的概念

- [[actor-model-for-gameplay]]
- [[lua-runtime-dynamism-tricks]]
- [[amdahls-law]]
- [[message-queue-thread-ownership]]
- [[main-thread-task-injection]]
- [[bitsquid-data-oriented-entity-system]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/03/multithreaded-gameplay.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-03-10_multithreaded-gameplay.md`
