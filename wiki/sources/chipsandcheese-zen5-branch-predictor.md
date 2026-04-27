---
tags: [source, computer-systems, cpu, amd, zen5, branch-predictor, frontend]
date: 2026-04-27
sources: 1
---

# Zen 5's 2-Ahead Branch Predictor Unit（Chips and Cheese）

[[george-cozma]] 与 Camacho 发表于 2024 年 7 月的文章，深入解析 AMD Zen 5 前端的核心创新——2-Ahead 分支预测器的历史起源、设计原理及 Zen 5 具体实现。

## 摘要

2-Ahead BPU 的学术根源可追溯至 1990 年代初（Seznac 等人），彼时被多核扩展路线取代；在单核性能重新成为焦点的今天，AMD 将其引入 Zen 5 作为前端基础性重构。文章解释了 x86 指令边界线性解析使宽解码器面积超线性增长的根本困难，而 2-Ahead BPU 通过"同时预测两个 basic block"绕过了这一瓶颈。Zen 5 的实现包括双 fetch 管道（2×32 字节/周期，各对接 4 宽解码簇）、双端口 6 宽 Op Cache（12 ops/周期）、16K 项 L1 BTB 和 8K 项 L2 BTB（victim 缓存语义），可处理每周期 2 个 taken branch，并额外维护第 3 个预测窗口。

## 关键要点

- 2-Ahead BPU：每周期预测跨越 taken branch 的两个连续 basic block
- 双端口指令 fetch：两条独立 32 B/周期管道 + 两个 4 宽解码簇
- Op Cache 双端口化，12 ops/周期，SMT 时两线程静态分区
- L1 BTB 16K 项（疑为双端口造成），L2 BTB 8K 项（victim cache 语义）
- 第 3 预测窗口通过 5 位长度字段编码，减少状态存储
- AMD CTO：Zen 5 是"从头设计"；Zen 6 将发挥 Zen 5 奠定的基础

## 链接到的概念

- [[zen5-2ahead-branch-predictor]]
- [[branch-predictor-design]]
- [[zen4-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/zen-5s-2-ahead-branch-predictor-unit-how-30-year-old-idea-allows-for-new-tricks
- 本地：`raw/articles/chipsandcheese.com/2024-07-26_zen-5s-2-ahead-branch-predictor-unit-how-a-30-year-old-idea.md`
