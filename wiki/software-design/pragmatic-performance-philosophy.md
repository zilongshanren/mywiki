---
tags: [performance, philosophy, profiling, 方法论, bitsquid]
date: 2026-04-19
sources: 1
---

# 务实的性能观

Niklas Frykholm 2011 年的一篇总结——Bitsquid 引擎写了若干年之后，他把自己的性能哲学浓缩成七条。主旨非常简单：**程序员时间是稀缺资源，目标是 maximum performance for minimum effort**。

## 七条

1. **程序员时间有限**——不可能每行都榨到极限；目标是"该快的地方够快"。
2. **简单解方案的复利**——易懂/易调/易改/易并行/易替换。只有当复杂解快 2× 以上且在 hot path 上才值。
3. **设计阶段是优化机会**——数据结构和访问模式的决策只有设计时最便宜，事后重构代价极高。这不是 premature optimization，因为不做这层会 **death-by-a-thousand-cuts**。
4. **top-down profiler 找热点**——带显式 scope、live pipe 到外部工具，然后 scope 窄化到根因。
5. **sampling profiler 补位**——抓跨多处调用的 hotspot（比如 `strcmp()` 出现在 profile 里就是程序在犯傻）。
6. **警惕 synthetic benchmark**——500 同实例 vs 50 异构实例的访问模式完全不同，优化容易过拟合。
7. **优化是园艺**——美术不断加内容把引擎压趴，程序员扶起来，这种 dialog 本身就是引擎的生命周期。

## 数量级驱动设计

每当 Frykholm 设计一个新系统，他会估算"一帧调多少次"：

- **1-10**：随便写；
- **100**：O(n)、data-oriented、cache friendly；
- **1000**：支持多线程；
- **10000**：认真想清楚。

## 8 条通用指南

- 静态数据放进 immutable 单分配 blob；
- 动态数据分配在大块连续内存；
- 尽量少用内存；
- 数组优先于复杂数据结构；
- 线性访问内存；
- 保证 O(n)；
- 避免 "do-nothing update"——维护 active 对象列表；
- 多对象系统要支持 data parallelism。

## 这套观点的位置

和 [[strategic-programming]] 是同一侧：**前期投资换长期收益**。反对面是"先烂写再优化"的极端 [[tactical-programming]] 解读。Frykholm 的说法更精细——**数据结构决策前期做、局部优化后期做**，由 profiler 指挥。

它也与 [[bottleneck-analysis]]、[[cache-friendliness]]、[[data-driven-architecture]] 构成 Bitsquid 设计哲学的主干。具体落地案例遍布 Bitsquid Blog：[[animation-stream-cache-layout]]、[[parameter-nodes-intrusive-linked-list]]、[[custom-memory-allocation]] 等。

## 相关
- [[strategic-programming]]
- [[tactical-programming]]
- [[bottleneck-analysis]]
- [[cache-friendliness]]
- [[data-driven-architecture]]
- [[frame-profiler-overlay]]
- [[red-flags]]
- [[performance-by-design]] —— Supnik 同期（2015）的「高性能是设计出来的」立场帖
- [[four-horsemen-performance]] —— Supnik 续篇：把「为什么后期救不回」拆成四条具体机制

## Sources

- [[sources/bitsquid-pragmatic-performance]]
