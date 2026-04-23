---
tags: [软件设计, 游戏引擎, 架构原则, bitsquid]
date: 2026-04-19
sources: 1
---

# 不许延迟一帧

Niklas Frykholm 在 2012 年关于 [[ragdoll-velocity-inheritance|ragdoll 速度继承]] 的博客里顺手立起一条 Bitsquid 引擎的内部戒律：**Thou Shalt Not Have Any Frame Delays**——任何请求到了就该当帧生效，不许推到下一帧。

## 为什么看似便宜的延迟是陷阱

延迟一帧的解法在很多棘手问题上都**看起来非常便宜**。想要前一帧的变换？延一帧就有了。想要避免本帧的循环依赖？延一帧拆开就好了。想让 A 发生在 B 之后？延一帧反正下一帧再跑。

但这会让对象进入一个**自相矛盾的过渡态**：它已经不是原来的 A 了，又还没成为应有的 B。这种灰色状态会像病毒一样扩散：

- 代码里开始长出 `if (is_transitioning_to_ragdoll) ...` 这种补丁逻辑。
- 一个原本只是想"做 A、B、C、D 四步"的函数，如果 A、B、C 各自都有一帧延迟，就会被迫变成一个需要跨 4 帧运行的状态机。
- 上层逻辑要反复问"我现在究竟是什么状态"，调用方也被迫学习这个多态过程。

本来要解决的**一个**数据流问题，现在变成了**整个系统**都要配合的状态机问题——这就是延迟一帧的真实代价。

## 作为 API 契约

"动作立即生效"其实是一条非常强的 [[api-fast-path-design|API 契约]]：调用 `set_kinematic(actor, false)` 之后，`actor` 就是非 kinematic 的，没有"可能下一帧才是"这种可能性。这种一致性让调用方的心智模型变得线性、可读、可测。

Bitsquid 的 [[system-decoupling-patterns|子系统解耦]] 在这种约束下反而更有价值——三个互不相识的系统都能在同一帧里有序往前推进，就得靠每个子系统内部**不把决策外包给下一帧**。

## 什么时候可以破例

原则不是教条。有些场景天然就是多帧的：

- **异步资源加载** 本质上必须跨帧。
- **网络预测回滚** 必须保留若干帧历史。
- **每帧只能递进一小步的迭代算法**（如某些约束求解器）。

区别在于这些情况下延迟是**显式、被命名、被文档化的**（如 `queue_load(...)` 返回一个 future）——而不是悄悄把一条副作用推到下一帧。

## 相关

- [[ragdoll-velocity-inheritance]] — 原则的出处场景
- [[system-decoupling-patterns]]
- [[api-fast-path-design]] — 命令式 API 的立即生效契约
- [[intent-vs-state]] — 另一个把决策做成"立即生效"的相关原则
- [[crash-on-unexpected-errors]] — Bitsquid 同根同源的另一条 "不留灰色地带" 戒律
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-inheriting-velocity-ragdolls]]
