---
tags: [并发, 引用计数, 数据竞争, 锁, 资源管理]
date: 2026-04-19
sources: 1
---

# 引用计数 + 全局表查找：必须先锁表再减计数

[[ben-supnik|Supnik]] 2016 年 7 月一篇两段短文讲清了一个设计反例：把 atomic decrement 和取全局表锁**按直觉的顺序**排列会炸掉。修法是反直觉的——**先锁表，再做减计数**。

## 典型的错误写法

X-Plane 10.45r2 的艺术资源释放代码：

```cpp
if (atomic_dec(&my_ref) == 0) {
    StLock take_lock(&global_asset_lock);
    global_asset_table.erase(this);
    delete this;
}
```

逻辑直观：

1. 原子递减我的引用计数
2. 如果归零（说明最后一个持有者），再锁全局表、清掉表项、自析构

看起来没问题——**atomic decrement 提供了一致的「我是最后一个」判断**，对吧？

## 第一个 race

**不是**。`my_ref` 变 0 和 `take_lock` 之间存在一个真实窗口，另一个线程可以：

- 拿到全局表锁 → 按名字查找到**我们**（引用计数此刻已经是 0）→ refcount ← 1 → 放锁；
- 然后那个线程开始使用这个资源，但**它手里的指针其实马上要被我们 delete 掉**。

这是经典的「我已经决定要自杀，但别人已经复活了我」竞态。

## 第二个 race：只检查 refcount 也救不回来

Supnik 承认自己当时「too clever」，试图在拿到锁之后**重新检查 refcount**，希望发现「有人复活了我」就中止删除。这修了第一个 race，**但留下了第二个**：

- refcount 还没 dec 到 0 之前（甚至就在 atomic_dec 与后续代码之间），另一个线程：
  - 拿全局表锁、找到资源、refcount++ 到 2、放锁；
  - 那个线程用完、refcount-- 变成 1；
  - 再一次 refcount-- 变成 0，进入自己那条 destroy 分支，拿全局表锁、erase、delete；
- 轮到我们继续走时，**我们才是那个拿着 stale 指针的线程**——`this` 已经被别人删了，再 delete 一次就是 double-free。

根因是：**atomic_dec 到 0 这个判断「已经不再对应真相」了**——在我们锁住表之前，世界是流动的，「最后一个引用」可以被任何竞态者夺走又丢回来。

## 正确的做法：先锁表

```cpp
StLock take_lock(&global_asset_lock);
if (atomic_dec(&my_ref) == 0) {
    global_asset_table.erase(this);
    delete this;
}
```

只要「在表锁下做 refcount 从 1 → 0 的那一跳」，语义就干净了：

- 表锁保护查表路径——别人拿不到锁就不可能把 refcount 从 0 提回 1；
- 我们亲眼看到 refcount 从 1 掉到 0；
- **没人能在此之前增加它**（被锁住）；
- **也没人已经拿着它**（我们是最后一个，由 refcount 保证）。

代价：**所有 refcount 递减都要拿全局锁**。在一个每秒做数千次 unload 的渲染引擎里这听上去要命——Supnik 的现实回应是：大部分 unload 已经在 worker 线程异步发生了，这条路径本来就不是 fast path。**rendering 主线程完全不走 refcount 修改**（一旦拿到 ref 就只读），所以不受影响。

## 更异步的备选方案

Supnik 在文末勾出一个更干净的架构：

- **全局表自己持一个引用计数**——资源只要进了表，就有一票不会消失的 ref；
- 正常线程 refcount 减到 1 时，**不立即删**，而是把这个资源扔进一个待 GC 队列；
- 后台 GC 线程周期性拿一次表锁、一次性清理所有 unused 资源。

这样 fast path 的递减重新变成了无锁的 atomic 操作，锁开销被 batch 到 GC pass 里——本质是**延迟回收（deferred reclamation）**的一种变体，和 epoch-based / hazard pointer / RCU 的 quiescence 思想同源。

评论区读者提了一个 epoch-based 替换方案：给表项加一个 epoch 序号，resource 复活时带新 epoch；unload 时只在 epoch 匹配的前提下才 erase。Supnik 认同这是一条合法路径——他之前在 [[cas-refcount-lowbit-lock]] 里也讨论过同类 CAS-loop 变体。

## 关键教训

- 「atomic 到 0」**不意味着**「没人再持有你」，除非你同时锁住了**持有者获取你的那条入口**。
- lock-free 思维有时候是陷阱：把**查找路径**锁起来比**保证 fast path 无锁**更重要。
- [[app-space-lock-free-simplification|应用层简化]]——Supnik 的一贯做法：**在真正冷的那条路径上吃锁，让真正热的那条（渲染）保持无锁**。

## 相关

- [[cas-refcount-lowbit-lock]] — 另一条「用指针低位当 spin lock」路线，同一问题的别解
- [[app-space-lock-free-simplification]] — 本案例是这套哲学在 resource release 上的落地
- [[ben-supnik]]

## Sources

- [[sources/supnik-worst-lock-ever]]
- [[sources/supnik-second-worst-lock]]
