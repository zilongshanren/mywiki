---
tags: [并发, 任务调度, 主线程, 事件循环, lua-coroutine, wasm, opengl, cloudwu]
date: 2026-04-19
sources: 1
---

# 嵌入事件循环的主线程任务注入

很多图形 API（OpenGL、Metal 在某些平台）要求**必须在主线程调用**；而主线程又通常被事件消息循环（Windows message loop / sokol callback / JS event loop）占据，不具备时间片的完整控制权。这就和自研任务调度器（如 [[ltask-scheduler|ltask]]）的前提冲突：调度器需要对所有时间片有完整控制权才能简单高效地做决策。这篇记录的是 [[cloudwu|云风]] 在把 [[soluna-2d-engine|soluna]] 移植到 wasm / Linux-OpenGL 时提出的解法：**给调度器打一个洞，让指定任务必须在主线程的事件回调中执行**。

## 问题结构

soluna 的底层是 ltask 多线程调度器。图形后端 sokol 不是线程安全的——原设计是把所有图形 API 调用塞进一个 render 服务，再用**信号量**在主线程 sokol 回调里和渲染服务同步。D3D / Metal / Vulkan 这么用没问题，它们被设计为跨线程可用。

但 OpenGL（Linux 上开启）和 wasm 破坏了这个假设：

- **Linux-OpenGL**：context 绑定在**当前线程**。最初通过额外 `MakeCurrent` 调用绕开，能跑但脆弱。
- **wasm**：web worker API 和 pthread 两套并发模型都有限制，比如 worker 中无法直接发起 DOM / canvas / WebGL 调用，必须转发回主线程。把所有 IO 都中转一遍代价太大。

云风一开始想避免改调度器——"只要不并发调用 sokol 就够了"。事实证明不够。**真正需要的是让图形 API 调用全部从主线程的 sokol 回调里直接发起**，而不是绕开问题。

## 解法：Lua VM 的时间片暂时让渡

这个方案和 2022 年云风那篇"[多线程串行运行 Lua 虚拟机](https://blog.codingnow.com/2022/09/multithread_lua_vm.html)"同构：**利用 Lua 有把运行流程抽象成数据（coroutine）这一能力，绕开 C 栈绑定线程的限制**。

具体步骤：

1. Lua 侧在启动"必须主线程执行"的任务前，**通知调度器把该虚拟机从调度表暂时移出**。
2. 主线程的事件回调函数通过信号量发现有新任务到来，接手执行该 coroutine 的特定片段。
3. 片段执行完毕后，**把虚拟机归还给调度器**，后续可以在普通工作线程继续跑。

这让**同一个 Lua coroutine 的上半段跑在工作线程、下半段跑在主线程**成为可能——这在纯 C 实现里几乎做不到，因为 C 栈绑定线程；而 Lua coroutine 的栈存在于内存堆上、不依赖 C 栈，天然支持这种"跨线程续跑"。

## 不改造调度器，而是打洞

另一种自然想法是把主线程回调**伪装成一个特殊工作线程**注册进 ltask。云风明确拒绝了这条路：主线程回调没有完整时间片、休眠策略和普通工作线程也不一样，把它硬塞进调度器会污染整个调度模型。**宁可在调度器上开一个受控的例外通道**，也不要为这一个场景重写调度器——"把主线程伪装成功能不完整的特殊工作线程"代价太高。

## 边角：唤醒休眠的调度器

实施中漏了一个 bug：主线程执行完特殊任务后把任务推回**线程安全的任务队列**是不够的——如果 ltask 的所有工作线程当前都没活干、已经进入休眠，光入队不会唤醒它们，任务会滞留到下一次事件驱动。**必须显式检查调度器休眠状态并唤醒**。这类"队列非空但 worker 全睡"的边界是手写调度器都会踩一次的坑。

## wasm 上没用 web worker 的原因

云风了解到 wasm 上有 pthread 和 web worker 两套多线程 API 后，原本想用 worker 实现一遍——更贴近 web 原生语义。最终放弃，原因是：

- Worker 不能直接访问 DOM / WebGL，**所有 IO 都要转发主线程**——这正是 wasm pthread 要解决的问题，用 worker 等于把问题搬回来。
- 转发层让整个引擎的 IO 路径都要改造，复杂度不值得。

pthread 路线 + 主线程任务注入已经够用。

## 和"多线程串行运行 Lua VM"的联系

两者是同一把锁的两种用法：

- 上次（2022 年）：在 C 阻塞操作前**解锁**Lua VM，让调度器可以把 VM 调给别的 coroutine 用；阻塞结束后重新加锁，等当前任务完成再继续。
- 这次：Lua 调用前**把 VM 从调度表移出**，让主线程接管运行该 coroutine 的一小段；执行完再归还。

两者的共同点是：**Lua coroutine 状态与 C 栈解耦，给跨线程流程编排开了后门**。这条路也可以反过来说——纯 C / C++ 做这类事必须引入 fiber、stackful coroutine 等额外基础设施，而 Lua 免费送了你这个能力。

## 相关
- [[cloudwu]]
- [[ltask-scheduler]]
- [[soluna-2d-engine]]
- [[lua-design-philosophy]]
- [[actor-model-for-gameplay]] —— 脚本层 per-API lock 模式的替代对照

## Sources

- [[sources/cloudwu-main-thread-task-injection]]
