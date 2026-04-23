---
tags: [并发, 无锁, 设计哲学, 引用计数, 工程权衡]
date: 2026-04-19
sources: 1
---

# 在应用层简化问题，而不是写通用 lock-free

[[ben-supnik|Supnik]] 2016 年初在回顾 CppCon 2015 上 Pablo Halpern 的 work-stealing 讲座和 Fedor Pikus 的 lock-free programming 讲座时，提炼了一条 X-Plane 工程团队长期奉行的准则：**通用 lock-free 数据结构是一个陷阱；真正能落地的方案都是把问题缩小到只需要「该无锁的路径无锁」**。

## 问题：通用 lock-free 很难做对

Pikus 在讲座里抛出了一个让人不安的结论：你写的并发 FIFO 对多线程来说**真的是 FIFO 吗？** 没人知道——因为从「一个正确的无数据竞争程序」出发，你根本**观测不到**并发顺序。任何能够 assert 顺序的测试都必然引入新的同步，从而破坏掉你想测的无锁属性。

Supnik 对此的反应是半开玩笑的「这是个胜利——又一件我不需要写的东西」。但 Pikus 给出的真正工程结论更扎实：

- **只设计你真正需要的东西，避开通用设计。**
- **不要写通用的 lock-free 代码。** —— 做一个没有 fine print、没有附加条件的完全通用 lock-free 结构需要的工程量远远超过你的预期，而最后结果往往带着隐晦的并发 bug。
- **在应用层找机会简化问题。**

## X-Plane 的实例：分层锁定

X-Plane 的艺术资源 API **并不是** lock-free 的——但关键在于**使用**艺术资源的那条 API 是 lock-free 的。两层语义是分开的：

- **加载/卸载**：发生在 worker 线程，异步。需要拿全局资源表锁，因为要在 path → loaded asset 的 map 上插入/查询/删除。加载本身的工作量不是小数（解析 DDS、构造 VBO、生成 mipmap），同步开销相对可以忽略。
- **使用**：渲染主线程拿到一个引用计数 + 指针以后，可以直接用，**永不再碰任何锁**。refcount 保证资源不会在使用过程中消失。

这个设计承认：**这不公平，不是 lock-free，也不是 wait-free——但它在我们真正在乎的那条路径上恰好是 unfair 的方向**。渲染主线程吃尽便宜，加载线程承担代价，符合游戏实时性的利益分配。

Supnik 自己调度器的架构也是**中央 work-pool**（类似 libdispatch），假设后台任务数量大、任务 cold、调度开销相对于任务本身可以忽略。他刻意避开了 work-stealing 里那些炫技的 continuation 机制——再次体现同一哲学：**先问问题有多难，再决定用多复杂的原语**。

## 为什么「unfair 是好事」

通用 lock-free 试图对所有线程都给出同样的进度保证，这就逼你用最强的同步原语（CAS loop、hazard pointer、epoch-based reclamation），每条路径都要付出代价。实时渲染的事实是：**99.9% 的 frame 里没有人在 load/unload**，主线程只是用资源；而加载/卸载已经被异步化了。

这时候把「一次性锁一下全局表」的代价放到本来就不走 fast path 的加载/卸载路径上，让渲染主线程走「只读 refcount 指针」的真正零同步路径，**总功更小、fast path 更快**。

这和 [[performance-by-design|Supnik 的 performance-by-design]] 一脉相承：不要做「通用方案然后优化」，而是在需求阶段把「哪条路径是热的」想清楚。

## 相关

- [[cas-refcount-lowbit-lock]] — 另一个「不如干脆用锁」的 RCU 类算法评估
- [[message-queue-thread-ownership]] — X-Plane 线程间通讯的同构选择
- [[performance-by-design]]
- [[four-horsemen-performance]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-work-stealing-lock-free-chaos]]
