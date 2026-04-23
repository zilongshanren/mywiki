---
tags: [source, bitsquid, data-oriented, sound, memory-layout]
date: 2026-04-19
sources: 1
---

# An Example in Data-Oriented Design: Sound Parameters（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 11 月的文章，用一个具体场景——声音实例上的 `{force, material, weapon}` 参数集合——做五轮 DOD 重构，是"by-the-book C++ 怎么一步步被改掉"的教科书式案例。

## 摘要

起点是典型 C++：`std::map<std::string, ParameterValue>` + `struct ParameterValue { Type; string; float; }`，每个实例一个堆上 map，指针追得到处都是。Frykholm 的五轮改造：(1) 字符串换 `IdString32` 哈希——不是给用户看的就不该用 string；(2) 放进 union，省掉 Type tag——存取时上下文已知类型，放弃 assert 换来 8 字节 POD；(3) `std::map` 换 `std::vector` + 线性搜索——参数典型 <10 个；(4) 不喜欢 vector-of-vectors，每实例 `Parameter params[MAX]` 固定数组——POD 大 blob 但浪费内存；(5) 最终方案：所有参数塞进一个全局 `ParameterNode nodes[MAX_PARAMETERS]` 数组，SoundInstance 只存头指针，用 **array-embedded intrusive linked list** 串起来；分配时从 `last_allocated` 往前扫——同一 sound 的参数天然落到相邻槽位。评论区里 Frykholm 还补了一段性能哲学：**不做 synthetic micro-benchmark**，前期每个系统写成 cache-friendly 是避免 death-by-thousand-cuts，真正的优化应当让 top-down profiler 指路。

## 关键要点

- **字符串哈希化**：只有给终端用户看的字符串才该是 string；
- **union 吃掉 type tag**：访问时类型上下文已知，assert 可以不做；
- **`std::map` 是 red flag**：小量数据 vector 线性搜索通常更快；
- **vectors-of-vectors 警报**：512 实例就是 512 次堆分配；
- **array-embedded linked list**：取链表的灵活性 + 数组的 cache 局部性；
- **分配策略**：递增扫描 free slot，同时刻分配的节点天然相邻——工程上很讨巧；
- **反对 micro-benchmark**：容易过拟合合成数据，对真实场景无用甚至有害。

## 链接到的概念

- [[parameter-nodes-intrusive-linked-list]]
- [[pragmatic-performance-philosophy]]
- [[data-driven-architecture]]
- [[cache-friendliness]]
- [[non-cryptographic-hash]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/11/example-in-data-oriented-design-sound.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-11-07_an-example-in-data-oriented-design-sound-parameters.md`
