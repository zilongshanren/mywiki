---
tags: [软件设计, 编程心态, aposd]
date: 2026-04-05
sources: 1
---

# 战略编程（Strategic Programming）

**战略编程**是 Ousterhout 对 [[tactical-programming]] 的反制：

> "Your primary goal must be to produce a great design, which also happens to work. This is strategic programming."
> 你的首要目标必须是产出一个优秀的设计，它恰好也能工作。这就是战略编程。

注意语序：一个优秀的设计、恰好也能工作——而不是「能工作的代码，以后再修饰」。这是大多数工程文化里优先级的根本翻转。

## 投资心态

> "Strategic programming requires an investment mindset. Rather than taking the fastest path to finish your current project, you must invest time to improve the design of the system."

有两种投资：

- **主动投资（Proactive）**：动笔前探索多个设计方案，即使更慢也选最干净的。想象系统将来可能如何演化，选一个能容纳变化的形态。写清楚意图。
- **被动投资（Reactive）**：工作中发现设计问题时，**修掉它**而不是绕过去。这是最难养成的习惯，因为修比绕更贵。

Ousterhout 的经验建议：把 **10-20% 的开发时间**花在设计投资上。小到不会搞乱排期，大到能产生复利。

## 不是完美主义，是复利

一种常见误读是「战略编程就是要求每行代码都完美」。不是。它要求的是**对系统长期健康的持续小维护**。战略编程的生产力曲线初期较慢，然后后发赶超——因为战术项目会被自己累积的复杂性淹没。

> "The most effective approach is one where every engineer makes continuous small investments in good design."

注意：是**每个工程师**、**持续地**、**小投资**。不是某人偶尔花一周大重构，而是全团队在每次提交时都留出一点设计余量。**战略编程是文化，不是项目**。

## 为什么「以后再重构」会失败

只要商业压力持续，「以后」永远不会来。当前的 crunch 结束了，下一个 crunch 又开始了。战略编程是**今天**要做的事，不是对明天的期望。

## 行业证据

Ousterhout 举了 Facebook 的例子：口号从「Move fast and break things」迭代到「Move fast with solid infrastructure」，因为多年的战术累积产出了一个不稳定、难维护的代码库，影响了招聘。反观 Google 和 VMware，战略文化成了竞争护城河：强代码库吸引强工程师，强工程师维护强代码库，正向飞轮一旦转起来就反过来运作。

## 相关
- 对立面：[[tactical-programming]]
- 极端战术的人格化：[[tactical-tornado]]
- 基础：[[complexity]]、[[zero-tolerance]]
- [[future-proofing-tests]] —— Ben Supnik 把「是否该为未来设计」落成可操作的三问测试
- [[pragmatic-performance-philosophy]] — Frykholm 的务实性能观：数据结构前期决策 + profiler 驱动后期优化

## Sources

- [[sources/aposd-day03]]
