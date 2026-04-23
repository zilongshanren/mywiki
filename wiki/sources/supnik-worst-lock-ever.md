---
tags: [source, 并发, 数据竞争, 引用计数, 锁, x-plane]
date: 2026-04-19
sources: 1
---

# Worst. Lock. Ever.（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2016 年 7 月的 race condition 拆解，承接两天前的 [[supnik-asan-big-bucks]]——X-Plane 10.45r2 艺术资源释放路径上的一个设计错误：把 atomic decrement 放在拿全局表锁**之前**，引入两条几乎对称的 race。

## 摘要

错误代码：`if(atomic_dec(&my_ref) == 0) { lock(table); erase(this); delete this; }`。第一条 race：`atomic_dec` 到 0 与 `lock(table)` 之间，另一个线程可以拿表锁、按名字找到这个资源、把 refcount 从 0 抬回 1、放锁——然后 we proceed to delete，留下那个线程拿 stale 指针。第二条 race 在 Supnik 的「聪明修法」（拿锁后重检 refcount）下依然存在：在 `atomic_dec` 与拿锁之间，另一个线程可以完整地走完「查表 +1、用完、-1 变 1、再 -1 变 0、拿锁 erase + delete」全程；轮到 we 拿锁时，`this` 已经被别人删了，double-free。**根因**：atomic_dec 到 0 「是最后一个」的判断只在**持续锁住查表路径**的前提下才成立。正解：**先拿表锁，再在锁下做 decrement**——锁住查表入口就锁住了「被复活」的唯一途径。代价是每次 refcount 递减都要摸一次全局锁，但 X-Plane 大部分 unload 已经异步化，渲染主线程根本不碰 refcount，所以无痛。文末给出更异步的架构草图：表自持一份 ref、对 refcount==1 的资源排 GC 队列、后台线程 batch 清理——与 epoch-based / RCU 同源。评论区有读者提出 epoch-tagged map 的替代实现，Supnik 认同是一条合法路径。

## 关键要点

- atomic_dec 到 0 **不等于**「没人还能再找到你」
- 必须锁住「能让别人找到你的入口」（全局表）才能安全走 destroy
- 「聪明修法」（锁内重检 refcount）只堵第一条 race，留下对称的第二条
- 正解是**先锁表再 dec**，代价仅落在已经异步化的冷路径上
- 更优架构：表自持 ref + 后台 GC batch 清理（延迟回收）
- epoch-based 变体也是合法替代

## 链接到的概念

- [[refcount-decrement-before-table-lock-race]]
- [[cas-refcount-lowbit-lock]]
- [[app-space-lock-free-simplification]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/07/worst-lock-ever.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-07-08_worst-lock-ever.md`
