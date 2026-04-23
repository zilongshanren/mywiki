---
tags: [source, bitsquid, 内存管理, 数据导向, 分配器]
date: 2026-04-19
sources: 1
---

# Garbage Collection and Memory Allocation Sizes（Bitsquid, 2013-01）

[[niklas-frykholm|Niklas Frykholm]] 2013 年 1 月的文章——一次"反思 GC"到"重塑 C++ 全局分配器纪律"的跨栈推理。

## 摘要

作者以"软实时程序员不信任 GC"起头，但随着 Bitsquid 往数据导向设计迁移，他发现自己自然而然地开始以**大块**形式分配内存（资源整块 blob、同构对象 SoA 数组）。在 Lua 做对比实验：per-bullet 对象 vs pos/vel 双大数组，后者**快 50×**，GC 时间还**减半**。也就是说，GC 的痛点本质不是 GC，而是"对象多而小"。这个洞察越过语言边界——C++ 的 malloc 同样吃碎片、cache miss、overhead。由此他提出："**全局分配器只发整页，每个子系统在自己的页里自理**"。好处一路列下来：外部碎片消失（address space 用 64 位也不怕）、按系统追踪内存变得显然、fragmentation 变成"某子系统的内部问题"、关停系统就是一把 free、溢出和悬垂指针更易 page fault 暴露。并且这条策略**可以渐进铺开**——一次改一个系统。评论区提到 RAII 的替代路线，以及 Go 选 GC 的权衡，作者都给了温和但明确的回应。

## 关键要点

- GC 的成本不在 GC 算法本身，而在"对象颗粒度过小"——数据导向式的大块布局即使对 GC 也友好。
- 实测：LuaJIT 下 SoA 数组版 50× 更快，GC 时间减半，哪怕该系统本身不创造垃圾。
- "多且小的分配" 同样伤 C++：cache 稀、allocator overhead、fragmentation、bug 追踪困难。
- 新纪律：**全局 allocator 只发整页**，剩下交给子系统——SoA / pool / ring 各自最合适。
- 外部碎片 → 内部碎片，且内部碎片有主（某个子系统），优化有靶子。
- 渐进迁移可行：一次改一个子系统即可，旧 kitchen-sink 分配器可以装进私有 heap 内继续运行。
- 对 Go 选择 GC 的评价：goroutine 共享语义下 GC 是可接受代价；这从以前的"奇怪选择"改口。

## 链接到的概念

- [[page-granular-system-allocator]]
- [[custom-allocator-interface]]
- [[linear-allocator]]
- [[virtual-memory]]
- [[a-metric-for-memory-fragmentation]]
- [[lua-incremental-gc]]
- [[data-driven-architecture]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2013/01/garbage-collection-and-memory.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2013-01-31_garbage-collection-and-memory-allocation-sizes.md`
