---
tags: [内存管理, 分配器, 数据导向, bitsquid, 页分配]
date: 2026-04-19
sources: 1
---

# 页粒度的子系统分配器

[[niklas-frykholm|Niklas Frykholm]] 在 2013 年初推到极致的一条主张：**整个引擎只从全局分配器拿"整页"的内存，剩下全部切分工作由各子系统自己在它拿到的页上完成**。这是从"一次 GC/cache miss 痛点"出发、推到 C++ 手动内存管理世界的一个彻底简化。

## 起点：GC 并不是真敌人

作为软实时程序员，Niklas 过去对 GC 不感冒——哪怕 Lua 用的是增量 GC（见 [[lua-incremental-gc]]），profiler 上那块时间总让他觉得"白耗"。但随着 Bitsquid 向 [[data-driven-architecture|数据导向设计]] 演化，他注意到一个现象：内存**以大 chunk 为单位分配**的代码（资源当整块 blob、类似对象按 SoA 打成一条数组）对 GC 非常友好——GC 要扫的对象从几万个变成几十个。

他用 Lua 做了对比实验：一个 per-bullet 对象 vs 两条大数组（pos/vel），后者**快 50 倍**，而且 **GC 时间也减半**，哪怕 `Bullet` 代码本身不生产任何垃圾——原因就是堆上对象少了，GC 遍历量小。

结论：**问题不在 GC，而在"多且小"的分配**。GC 语言、malloc 语言都一样会被小分配拖死——cache 稀、fragmentation 多、allocator overhead 高、内存问题难追踪。

## 提议：只允许"整页级"全局分配

把全局分配器的能力压缩成一条规则：**子系统一次只能申请整数页（page）**。拿到之后，页内怎么切是子系统的家务。好处层层叠叠：

- **子系统最懂自己的访问模式**，它能把这块页排成 SoA、ring、pool 各种最合适的布局；全局 allocator 永远不知道这些。
- **按系统追踪内存变得显然**：全局只剩少量几个大分配，每个带系统 tag，每个系统吃多少一目了然。
- **系统内部追踪也变容易**：它知道自己的对象是什么，分配出错时能给出 "是 actor X 的 animation buffer" 这种有意义的报告。
- **关停系统 = free 一块 / 几块页**，不留内存碎片泄漏残余。
- **彻底消灭外部碎片**：所有全局分配都是整页；通过 virtual memory 的页映射，address space 本身可随意重排——只要用 64-bit 地址空间，**address space fragmentation 也可以不在乎**。
- **外部碎片变内部碎片**：一块页最多浪费半页末尾，但这种浪费**属于某一个子系统**——可以独立优化，不会像外部碎片那样是"全局无主问题"。
- **缓冲区溢出与悬垂指针更易捕获**：跨页访问大概率 page fault，问题当场现形。

## 与已有机制的关系

- [[custom-allocator-interface]]：Bitsquid 的 Allocator 抽象本就允许每个系统持有私有 heap；页粒度是这条抽象的进一步纪律化——**私有 heap 必须从页分配器长出来，而不是从 kitchen-sink 分配器**。
- [[linear-allocator]] / [[bump-allocator-wasm-guest]]：子系统在自己拿到的页上做的事，通常就是这类 simple arena——不需要通用 malloc 的所有功能。
- [[virtual-memory]]：这条策略完全建立在虚拟内存机制之上。物理页可以按需 commit、可以按页 remap，"address space 不等于 physical footprint"是这套设计的地基。
- [[a-metric-for-memory-fragmentation]]：用"外部碎片"作全局 KPI 的时代结束——按页分配意味着"外部碎片"在地图上不存在，监控应转向每个子系统的内部利用率。
- [[lua-incremental-gc]]：原文里的 GC vs 手动内存管理的讨论起点；两者共用一个结论——**颗粒度**才是决定性变量。

## 迁移性

这个方案**可以渐进铺开**——一次改一个子系统：把它的分配器换到 page allocator 后面即可。暂时不好改的子系统可以继续用旧 kitchen-sink 分配器，或把 kitchen-sink 自己装进一块从页分配器取来的私有 heap——它爱怎么烂都污染不到别人。

对 Go 使用 GC 的选择，Niklas 的评价也由此转变：一开始觉得"低层语言不应该 GC"，后来承认 Go 把**大分配 / goroutine 共享状态**组织好以后，GC 的开销是可接受代价。

## Sources

- [[sources/bitsquid-gc-and-allocation-sizes]]
