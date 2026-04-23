---
tags: [source, bitsquid, performance, profiling, philosophy]
date: 2026-04-19
sources: 1
---

# A Pragmatic Approach to Performance（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 12 月的文章，是 Bitsquid Blog 里少见的一篇纯方法论总结——不讲具体技术，讲怎么在"程序员时间有限"这个前提下分配优化精力。

## 摘要

七节主旨：(§1) 程序员时间是稀缺资源，目标不是处处最快，而是**该快的地方够快**；(§2) 简单解方案更易懂、易调、易改、易并行化、易替换——它省下的时间可以投到真正的热点上；(§3) 拒绝"先烂写再优化"：系统设计阶段对数据结构和访问模式做一次粗略估算几乎零成本，事后重构代价极高；(§4) 用 **top-down profiler**（带 profiler scope、实时 pipe 到外部工具）找瓶颈，窄化 scope 钻下去；(§5) **bottom-up sampling profiler** 补位——抓跨多处调用的 hotspot，比如 `strcmp()` 出现在 profile 里就是程序在犯傻；(§6) **警惕 synthetic benchmark**：500 个同实例跑同动画的数据访问模式和 50 种不同 unit 完全不一样；(§7) 优化像园艺——美术不断加东西把引擎压趴，程序员再把它扶起来，两者的 dialog 决定引擎能力边界。文章还给了一份设计阶段的**数量级指南**：调用频率 1-10 随便写，100 要 O(n) + cache friendly，1000 要多线程，10000 要认真想；以及 8 条通用指南（静态数据 immutable blob、动态数据大块连续、少用内存、数组优先于复杂结构、线性访问、O(n)、跟踪 active 对象避免"空更新"、多对象支持 data parallelism）。

## 关键要点

- **"程序员时间有限"是第一性原则**——所有后续结论都从这儿推出来；
- **简单解的复利**：易懂/易调/易改/易并行，复杂解只在真正关键路径上才值；
- **设计阶段优化 ≠ premature optimization**：数据结构选型只有设计时最便宜；
- **top-down profiler + 显式 scope** 是主力工具，sampling profiler 是补位；
- **数量级驱动设计**：1/100/1000/10000 对应不同级别的优化义务；
- **反对 micro-benchmark**：真实负载的访问模式和合成数据差异巨大；
- **优化是持续过程**：美术加内容、程序员托住，这是引擎生命周期本身。

## 链接到的概念

- [[pragmatic-performance-philosophy]]
- [[bottleneck-analysis]]
- [[cache-friendliness]]
- [[data-driven-architecture]]
- [[frame-profiler-overlay]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/12/pragmatic-approach-to-performance.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-12-08_a-pragmatic-approach-to-performance.md`
