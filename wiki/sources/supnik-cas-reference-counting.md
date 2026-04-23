---
tags: [source, 并发, 无锁, CAS, RCU]
date: 2026-04-19
sources: 1
---

# CAS and Reference Counting Revisited（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2011-01-04 的文章，接续他 2009 年写的「CAS and reference counting don't mix」。文章本身给出一种「**指针低位当自旋锁**」的变体，但博客真正的价值出在评论区：Dmitry Vyukov 进来把「**differential reference counting**」的 wait-free 做法讲清楚。

## 摘要

根本问题：**一次 CAS 没法同时完成「读指针 + 给对象加 refcount」**，因此朴素方案里读者有一段极短窗口可能撞上 update、拿到一个已释放的对象。Supnik 的思路是用 2 字节对齐指针的**低位当 lock bit**：读者进入前 CAS(ptr, ptr | 1) 抢位，`atomic_inc` 完 refcount 后 CAS 回去放位——自旋锁把临界区压到几条原子指令。他诚实指出**最大短板**：这套算法**没法阻塞等「旧副本释放完」**，没有 RCU grace period，不能用于需要「更新完全 commit」语义的场景。评论区 Vyukov 给出 differential refcount 方案：每个指针 cell 带 outer counter、每个对象带 inner counter，通过 double-word XCHG/XADD 实现 wait-free；成本是 32-bit 环境下位数紧张，但可用动态对齐或 bounded pool 解决。

## 关键要点

- 经典缺口：读 ptr → refcount++ 不能原子化，中间可被 update 追杀。
- Supnik 变体：指针低位当 lock；读者自旋、更新者也得等低位 clear。
- 算法弱点：**无 quiescence**——「此次 update 已经被所有线程看见」没法断言。
- Vyukov 的 differential refcount：outer（指针 cell 上）+ inner（对象上）两层 counter；指针换位时把 outer 的累计数「转移」到 inner。
- 32-bit 位宽约束：要么吃 alignment 低位当 counter，要么把 ptr 换成 bounded pool index。
- 动态对齐（64 worker → 64-byte align）基本消除 counter 位数问题。

## 链接到的概念

- [[cas-refcount-lowbit-lock]]
- [[semaphore-vs-condvar-latency]]
- [[message-queue-thread-ownership]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/01/cas-and-reference-counting-revisited.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-01-04_cas-and-reference-counting-revisited.md`
