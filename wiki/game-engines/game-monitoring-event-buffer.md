---
tags: [游戏引擎, 性能监控, 数据导向, 调试工具, bitsquid]
date: 2026-04-19
sources: 1
---

# 游戏监控：TLS event buffer 与在线/离线 visualizer

游戏里有一类 bug 不能靠断点抓——它只在"和上一帧/下一帧对比"的时间维度上才存在：掉帧毛刺、动画抖动、相机突跳。[[niklas-frykholm|Niklas Frykholm]] 在 2011 年给 Bitsquid 搭的 **monitoring 系统**就是为这类问题生：把游戏当成一个陌生的生物，戳它、看曲线、直到你看出问题。

## 核心思路：全都是 event，画面都是后处理

不要为每种可视化各做一套管线。只做一件事：**把事件写进一个大缓冲，visualizer 负责读**。事件类型有 `ENTER_PROFILER_SCOPE`、`LEAVE_PROFILER_SCOPE`、`ALLOCATE_MEMORY`、`FREE_MEMORY`、`RECORD_GLOBAL_FLOAT` 等。每个事件是一个以 type id 打头的变长 struct——和 [[offset-based-resource-blobs]] 同一套 "file format for memory" 信念。

`record_global_float("application.delta_time", dt)` 这种调用就把一条 `{name_ptr, value}` 追加进缓冲。画 delta-time 曲线、帧率曲线、bone 旋转、相机位置、内存碎片（参考[[a-metric-for-memory-fragmentation]]）、网络带宽，全都是同一个通道。

## TLS thread-local buffer + 批量 flush

**多线程写同一个大 buffer 必然需要 mutex**——把这变成每帧的锁热点很蠢。做法是每个线程各一个 64 KB 的 `__thread` 小 cache：线程把 event 往自己的 cache 里 append，等 cache 满或帧末才去抢全局 buffer 的锁一次性 flush 过去。`record_global_float` 的 hot path 只有几条指令、零分配、零同步：

```cpp
if (_thread_buffer_count + 12 > THREAD_BUFFER_SIZE)
    flush_thread_buffer();
char *p = _thread_buffer + _thread_buffer_count;
*(unsigned *)p = GLOBAL_FLOAT;
*(RecordGlobalFloatEvent *)(p+4)->name = name;
*(RecordGlobalFloatEvent *)(p+4)->value = value;
_thread_buffer_count += 12;
```

所有 debug buffer 从**独立的 debug heap** 分配，与游戏正常堆隔离；不污染 shipping 配置里的内存账单。

## 字符串指针即 interned ID

注意 event 里存的是 `const char *name`——指针本身，不是字符串内容。因为 `record_global_float` 只接受**静态字符串字面量**，它们在进程里地址唯一且生命周期永久。于是"同名事件的 name 指针相等"，省内存、省 strcmp、struct 定长。这是[[string-handling-game-runtime|string interning]] 最轻的一种形式：整个程序的编译期 `.rodata` 就是一张现成的 intern 表。

如果真要动态字符串，就得手动把它复制到一块永久内存——评论区 Niklas 也提到：跨网络传给离线工具时，第一次遇到新指针就把 `(ptr, "actual_string")` 专门写一条"字典消息"过去，离线端建映射表还原名字，后续只传指针即可。

## 在线 visualizer + TCP 离线 visualizer 双通道

global buffer 在每帧末被两类消费者读：

- **在线 visualizer** 就在游戏里画——叠在游戏画面上的实时曲线、柱状图；
- **离线 visualizer** 通过 TCP 把整份 buffer 推给 PC 上一个独立工具，PC 内存近乎无限，可以保留整局游戏的历史用于回放、横扫、多维分析。

消费完，buffer 整体 reset，下一帧开始复用——和 [[linear-allocator]] 同构的帧生命周期管理。

## 流式消费的两个细节

评论区里最常被问的是**处理模型**：

1. **不删事件、只读不写**。所有 reader 都看得到整份流，各自挑自己关心的 type 跳过其它，本来就 O(n) 扫一遍。
2. **子系统若要抢占事件**，比如一个事件应由唯一一个子系统消费，就在上面套一个 master 分发器读到事件后手动路由到目标子系统。每个子系统只维护 outgoing 事件队列，上游拉取——这顺带解决了跨系统的同步顺序问题。

## 和 Lua 脚本的联动

因为 buffer 是普通函数调用产生的，Bitsquid 把 record 接口整体 expose 给 [[lua-cpp-binding|Lua]]。举个作者原文例子：有人怀疑鼠标驱动更新率太低，几行 Lua 在控制台就能挂一个 updator 每帧 `Profiler.record_statistics("mouse", Mouse.axis(0))`，然后 `graph make mousegraph / graph add_vector3 mousegraph mouse` 立即出图验证——从"我想看 X"到"我看到了 X"只要 30 秒。这是 Lua 作为引擎**可视化探针**而非 gameplay 语言的典型用法。

## 与其他设计的呼应

- 和 [[bitsquid-task-scheduler]] 兼容：TLS buffer 避开了 task 系统的锁热点；
- 事件 buffer 是**连续 POD struct**——能和 [[offset-based-resource-blobs]] 一样被 DMA、memcpy、直接 dump 到盘；
- 性能关键字段（帧时、内存）走 C 侧 record，调参/探针类随时用 Lua 插入，分工清晰。

## Sources

- [[sources/bitsquid-monitoring-your-game]]
