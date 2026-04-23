---
tags: [source, bitsquid, 数据导向, 脚本系统, 可视化编程]
date: 2026-04-19
sources: 1
---

# Visual Scripting the Data-Oriented Way（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 9 月的文章，介绍 Bitsquid 的可视化脚本系统 **Flow**，以及为什么其运行时不是传统的 OO 节点图。

## 摘要

Bitsquid 用两层脚本互补：Lua 给程序员写 gameplay 逻辑，**Flow** 给美术/关卡设计师用节点图挂特效、破坏、交互。Flow 编辑器里的数据是 OO、易改、跨版本——这是 source 数据。但**运行时**完全不碰 OO：整张图压成一整块连续 blob，每个节点有个类型 id，用 `switch` 分派动作；节点间的指针全部变成 blob 内的 offset。动态状态（blue links）放在另一个 blob 里，实例化时 `memcpy` 一份就行。整块可以单次 `malloc`、单次落盘、单次 DMA 到 SPU、想 memcpy 想读盘都不用做指针 fixup。Flow 本身不做重算——它只把事件路由到底层系统——所以他刻意**不**多线程它，避免系统间同步代价。

## 关键要点

- **编辑器数据 ≠ 运行时数据**：编辑器用 JSON / OO，运行时用 platform-specific binary blob，随时可从 source 重编；
- 节点 dispatch 用 `switch(type_id)` 而非虚函数——评论里有人提议换 jump table / vtable，作者承认收益有限但代码更漂亮；
- blob 里指针全是 offset，**允许 memcpy、DMA、直接读盘**；
- **静态 blob + 动态 blob 分离**：静态的是共享编译结果，每个实例克隆一份小的动态 blob，释放时整块回收、"超便宜的 GC"；
- Flow 不 update、只响应事件；不多线程——Flow 只是高层 router，计算放在底层 animation state machine 等**已经多线程**的系统里；
- Flow 和 animation state machine 的通信靠 32-bit 字符串 hash（事件名），与 [[static-hash-value-debug-assert|静态 hash]] 呼应；
- "file formats for memory"——作者自己对 DOD 的口号：内存也是盘。

## 链接到的概念

- [[flow-graph-data-oriented-runtime]]
- [[offset-based-resource-blobs]]
- [[data-driven-architecture]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/09/visual-scripting-data-oriented-way.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-09-17_visual-scripting-the-data-oriented-way.md`
