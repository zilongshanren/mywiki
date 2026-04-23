---
tags: [系统设计, 事件, 回调, 轮询, 消息机制, bitsquid]
date: 2026-04-19
sources: 1
---

# Polling / Callbacks / Events：低层到高层的三种通知方式

[[niklas-frykholm|Niklas Frykholm]] 《Managing Coupling》第二篇，解决一个具体问题：**低层系统需要告诉高层系统某件事发生了**（例如动画系统在脚触地的一帧通知 gameplay 层播脚步声），这种通知应该怎么传？

一个前提：**反方向是没问题的**。高层系统本就知道所有低层系统，可以直接调它们。本文讨论的只是"**低层 → 高层**"这单一方向。

三种常见技术：polling（轮询）、callbacks（回调）、events（事件队列）。Niklas 的结论和直觉相反——**优先用 polling**。

## 1. Polling：被低估的朴素方案

桌面世界的常识里，polling 是"不礼貌"的，因为它意味着 busy-wait、把 CPU 吃到 100%。

**但游戏循环里这个前提就不成立**：每 33ms / 17ms 我们本来就要干几百件事。只要不是在 poll 大量对象，poll 对帧时间的影响接近于零。

而且 **poll 驱动的代码往往比 callback 驱动的更清晰**。比如"A 键按下时 character controller 做点事"，在 controller 内部直接 poll `input.A_is_pressed()` 比注册一个 callback、在 callback 里把消息 forward 给 controller 要直接得多。

**Niklas 的立场**：**只要对象数不爆炸，优先 poll**。合适的场景：文件下载完成、server 列表刷新、存档状态、手柄输入……

不适合 poll 的典型场景是**物理碰撞**——N×N 对可能的碰撞关系，逐个 poll 不现实（你真想这样做的时候其实已经是在写 event 系统了）。

## 2. Callbacks：请一定要延迟执行

回调的关键设计问题：**事件发生时立即调用，还是排队到本帧稍后某一点统一执行**？

Niklas 坚定推荐**后者**——延迟回调。理由：

- **cache 友好**：立即回调会立即跳到另一段代码里，搅烂 I-cache 和 D-cache。
- **可并行**：立即回调让多线程执行必须到处加锁；延迟回调可以先把 callback 推进队列，事后在安全点统一处理。
- **避免自杀**：立即回调最恶心的 bug 是——回调在执行中把"正在被遍历的对象"给删了。延迟意味着遍历循环里只是往队列 append，执行在 `execute_callbacks()` 这个明确的节点。
- **SPU/worker 生成、主线程 merge**：多个 worker 各自 append 自己的 callback 队列，在同步点合并，直接可用。

注意：**延迟回调和 polling 的形态开始像了**——回调"只在我主动调 `execute_callbacks()` 时才真的发生"。这不是巧合：polling 思想的核心是"控制 **何时** 观察变化"，延迟回调保留了同一控制点。

### C++ 里回调的工程写法

Niklas 的几点反经验：

- **不要用成员函数指针**：C++ 成员函数指针的类型和 cast 规则让"通用回调机制"几乎不可能写干净；
- **不要用 observer pattern**（继承 `AnimationEventObserver` 再 override）：大堆样板代码 + 堆分配；
- **不要上 FastDelegate 那种平台 hack**：虽然漂亮，但把引擎的核心机制建在一堆平台 specific 的 trick 上不值当。

他的写法是朴素的 **C 风格函数指针 + user data**：要调成员函数？写一个小 static 转发函数就行。作者有一句很到位的观察：

> 每次你想设计一个"干净灵活的 C++ API"，它最后都趋同到纯 C。

为了让 user data 能装更多东西，不止一个 `void*`，他用了一种"胖回调"：

```cpp
struct Callback16 {
    void (*f)(void);
    char data[12];
};
```

16 字节装下函数指针和足够多的参数；调用时把 `callback.data` 当第一个参数：

```cpp
typedef void (*AnimationEventCallback)(void*, unsigned);
AnimationEventCallback f = (AnimationEventCallback)callback.f;
f(callback.data, event_id);
```

**函数指针来回 cast、`data` 里塞 raw bytes**——Niklas 对这种"裸内存的威力"毫不掩饰：类型安全固然好，但**把一块 raw memory 当各种东西看的自由度，在高性能引擎里价值极大**。万一 cast 错了？99% 会立刻大崩溃，当场就改对了。

### 回调引用的对象死了怎么办

延迟回调的唯一真问题是：callback 被生成时对象还在，执行时对象可能已经被销毁。这个问题在 [[system-decoupling-patterns|Managing Coupling]] 里已经用 **ID 引用** 解决过——callback 里存的是 ID 而不是指针，执行时先查一下对象还在不在。

## 3. Events：callback 的 enum 化

Event 系统几乎和 callback 一样，**唯一差别是"不存函数指针、存一个 enum"**。高层系统 poll 到这个 enum 时自己决定做什么。

Niklas 给的经验区分：

- **callback 适合单点监听**："这条音效播完告诉我"——接收者已知且专门。
- **event 适合成批处理**："把这一帧所有碰撞遍历一遍，看谁的受力足以打碎物体"——接收者统一处理一整流。

### 极简的 event 存储

Niklas 对 event 队列的实现也极朴素：**一块 raw buffer**（`Vector<char>` 或 `char[FIXED_SIZE]`），所有 event 按格式连续串起来：

```
[event_1_enum][event_1_data][event_2_enum][event_2_data]...
```

高层系统线性扫一遍，按 enum 分发。这种表示**可以自由地 move / copy / merge / 跨 core 传递**——又一次，**raw data buffer 的威力**。

### 关于 event 系统的反面警告

Niklas 在最后一段强调一条原则——**event 系统不应该是一个全局 switchboard**。每个低层系统的 event 流应该有且仅有**一个**高层消费者，这个消费者清楚知道所有 event 的语义、数据布局和处理方式。

> An event system should not be a magic global switchboard that dispatches events from all over the code to whoever wants to listen to them. Because that would be horrid!

这一点经常被滥用的 pub/sub 系统违反——任何地方 publish，任何地方 subscribe，最后谁都不知道一个 event 到底会触发什么副作用。[[dependencies|耦合]] 以另一种看不见的形式被种回代码库。

## 组合使用的直觉

三种方式在 Bitsquid 的工程里是**正交并用**的：

- **对象少、查询廉价** → polling
- **低层 → 单个高层、单点监听** → 延迟 callback
- **低层 → 单个高层、批量处理** → event 队列
- **跨系统广播** → **不要做**

## 消费节奏与溢出

评论区问：event 谁来清？——**消费者每帧处理完一次就清空**。生产过快导致溢出？**要么扩 buffer，要么丢最旧的，要么暂时冻结生产者**——这是每个子系统要自己根据语义决定的权衡。

## 相关

- [[system-decoupling-patterns]] — 本系列第一篇：四条耦合管理原则
- [[id-based-lifetime-with-kill-flag]] — 延迟回调中引用对象是否还活着的查询机制
- [[handle-based-resource-manager]]
- [[intent-vs-state]] — poll 对应"看状态"，callback/event 对应"看意图"
- [[flow-graph-data-oriented-runtime]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-managing-coupling-part-2]]
