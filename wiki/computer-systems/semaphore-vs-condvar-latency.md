---
tags: [并发, 同步原语, pthread, 消息队列, X-Plane]
date: 2026-04-19
sources: 1
---

# 信号量 vs 条件变量：消息队列唤醒延迟

[[ben-supnik|Supnik]] 在把 X-Plane 10 的飞行模型改成多线程时，拿 Shark profile 发现 worker 线程唤醒一次要 **200 µsec**。瓶颈不是工作量，而是「一堆线程同时醒来抢锁」——换掉同步原语以后降到 **80 µsec**，其中 45 µsec 还是 mach semaphore 信号本身。问题不出在 pthread 的性能，而出在 pthread 条件变量**内置的锁语义**。

## pthread 条件变量到底贵在哪

OS X 的 pthread（至少在 10.5 时代的 libc 源码里）大致这样实现：

- 一个 **spin lock** 保护 mutex 和 cond var 自己的「内部结构」；
- 一个 **OS semaphore** 提供真正的阻塞；
- **`pthread_cond_wait` 在被唤醒后必须重新获取原 mutex**——这是 POSIX 语义的一部分。

第三条就是灾难的来源：若一次 signal 唤醒多个 worker（比如 broadcast 或者 N 个 worker 等同一队列），它们**全部醒来去抢同一把 mutex**，命中的只有一个，其余再度阻塞。这就是 Supnik 描述的「total train wreck of lock contention」——一次唤醒串行化成 N 次阻塞/唤醒循环。

## 换成 semaphore + critical section

Windows 版本原本就在用的设计：

- **critical section（其实是 spin lock）** 只保护队列内容本身，不保护 pthread 内部；
- **mach semaphore** 单独管计数。

关键区别是**锁的粒度**：新设计里锁只覆盖「把消息入/出链表」那几条指令，而且**持锁时不进入 pthread 任何代码**。要唤醒的线程直接用 mach semaphore signal，不需要在醒来后重新抢某把 mutex——这把原本隐藏在 `pthread_cond_wait` 里的「重锁阶段」彻底干掉。

结果：200 µsec → 80 µsec，其中信号量开销 45 µsec（5–10 µsec/调用）几乎是 mach 原语的极限，剩下的 35 µsec 是队列管理 + 调度唤醒。

## 为什么 spin lock 合适

Supnik 特别指出两点：

1. **uncontested pthread mutex 会 fast-path**，不一定进内核；但只要**两个以上线程**同时争，就立即 sleep。而受保护的代码只有几条指令时，sleep 的系统调用比 spin 多好几个数量级。
2. **消息队列的临界区极短**——只涉及链表头指针增减——完美匹配 spin lock 的使用场景。

另一个实际加成：当队列在唤醒之前就已经非空（比如 Supnik 的两级队列设计，外层只是一个「去看内层队列」的通知），semaphore 的 wait 会走**原子快速路径**，连系统调用都不进，更快。

## 对未来 lock-free ring buffer 的注记
Supnik 在文末讨论把队列改成 ring buffer FIFO：用两把 semaphore（filled/free count）+ 原子读写指针。关键不变量是 **「两把 semaphore 之和可以小于 buffer 容量」**——因为总是先 decrement 再 increment，这天然阻止读写指针追尾覆盖对方正在处理的 slot。代价是放弃严格的消息顺序（两个 reader 可能乱序交出）和一些现有 API 方便的 inspect/edit 操作。结论是：**API 的约束（能否容忍写阻塞、能否放弃锁定修改）才是决定同步设计的真正门槛，不是性能数字**。

## 跨平台追记：Linux NPTL

Supnik 几天后的 [[sources/supnik-semaphore-nptl|follow-up]] 承认上面那些让 OS X pthread 昂贵的实现细节，在 Linux 的 **NPTL**（Native POSIX Thread Library）里多数不存在：pthread mutex 是 spin-sleep 混合、`sem_t` 有原子计数器、底层一切同步都建立在 **futex** 之上——未争用路径全部只用原子操作。OS X pthread 在未争用情形也走 user-space spin lock 簿记，但 Supnik 判断 futex 路径更快。这把结论拉回到一个朴素的观察：**同步原语的「正确选择」是平台依赖的**，没有放之四海皆优的方案——为 OS X 自研 semaphore+critical section 的动机在 Linux 原生 pthread 上其实并不那么紧迫。

## 相关

- [[message-queue-thread-ownership]]
- [[main-thread-task-injection]]
- [[vfx-multithreading-patterns]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-semaphore-vs-condvar]]
- [[sources/supnik-semaphore-nptl]]
