---
tags: [并发, 无锁, CAS, 引用计数, RCU]
date: 2026-04-19
sources: 1
---

# CAS 与引用计数：低位当锁的自旋变体与 differential refcount

[[ben-supnik|Supnik]] 2011 年在博客上回到一个他 2009 年提过的问题：**单条 CAS 指令没法把「解引用指针」和「给指向对象 +1 引用」两件事打包成原子操作**，所以朴素 CAS + refcount 组合起来会让读者在「刚拿到指针、还没来得及加 refcount」的瞬间撞上一次 update，把对象释放掉。

这篇博客提出一种务实变体，引出了评论区 Dmitry Vyukov 的 **differential reference counting** 方案。

## 问题

CAS + refcount 合力保护「内容可被替换的一份数据」：

- **读者**：读指针 → 做 refcount++ → 用数据 → refcount−−（到 0 回收）
- **更新者**：复制一份旧数据 → 造一份新副本 → CAS 换指针 → 把旧副本的 baseline +1 扣掉；最后一个退出的读者释放

致命缝隙：读者读完指针、还没有 `refcount++` 的那一瞬间，更新者如果刚好把指针换掉并把 baseline 扣掉，读者手上的指针可能指向**已释放**内存。一次 CAS 无法同时更新「外部指针」和「内部 refcount」。

## Supnik 的变体：用指针低位做自旋锁

2 字节对齐的指针低位一定是 0，**把低位当 flag**：

```
read_begin:
  loop: old = ptr; CAS(ptr, old, old | 1)  // 抢到 lock bit
  atomic_inc(&old->refcount)
  CAS(ptr, old | 1, old)                    // 放 lock bit
  return old
```

读者在「读指针 + refcount++」这段窗口内持有低位锁，其它读者自旋。更新者试图换指针时也必须看到低位是 0，因此写者被迫等这段窗口结束。

这不是完全无锁——是把临界区压到极短的若干条原子指令。Supnik 自己点名一个**结构性缺陷**：更新后**没有办法阻塞等「旧副本真的被所有线程释放完」**。也就是说你没法做到「this update is fully committed」这个强保证。这在生产系统里常常就意味着不能用于需要「读屏障」语义的场景（经典 RCU quiescence）。

## Dmitry Vyukov：differential reference counting

评论区 Vyukov 给出一个**无自旋**的 wait-free 方案，用双字 atomic RMW：

- 每个 ptr cell 带一个 **outer counter**；每个 object 带一个 **inner counter**。
- 读者 acquire：外计数 +1 读 ptr → 对象 inner +1 → 外计数 −1 转移完成（若外计数已因指针被换而不可减，就减 inner）。
- 写者 swap：把当前 outer 数累加到对象 inner 上 → CAS 换指针；成功则旧 cell 的 outer 实际被「转移」到对象 inner，旧对象的生命周期由 inner 单独管理。

代价是 32 位机上 **位数紧张**：要么吃 alignment 低位做 counter（worker 多时可能溢出），要么把指针换成 bounded pool 的数组偏移（限制对象总数但能省出高位）。Vyukov 补充：**动态对齐**（64 worker 就 64-byte align）能把这个问题压到基本不存在。

## 这类算法为什么总被绕开

Supnik 的原话：「每隔几个月我回来看一眼 RCU 类算法」——不常用的根本原因是**没有 quiescence 语义**，写者无从得知旧副本何时彻底释放干净。业务代码里只要有「改完配置，等一下，再做下一步」的语义，这套就用不了。

对比之下：

- 想要**安全并发更新** + 明确释放时机：用 **强线程安全引用计数** 或 differential refcount；不能满足 full barrier。
- 想要**完整 RCU 语义**：Linux 内核那套才管用——但要求用户能忍受「grace period」和单向只能被 kernel 调度的 quiescent state。

Supnik 的价值在于把「这种算法在生产代码里落不下来」的具体原因讲清楚，而不是停在「这里有个 race」。

## 相关

- [[semaphore-vs-condvar-latency]] — 另一篇 Supnik 对并发原语的实测
- [[message-queue-thread-ownership]] — X-Plane 的线程通讯替代路线
- [[ben-supnik]]

## Sources

- [[sources/supnik-cas-reference-counting]]
