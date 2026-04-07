---
tags: [source, 计算机体系结构, caqa]
date: 2026-04-05
sources: 1
---

# Computer Architecture Day 1 —— 量化方法

Computer Architecture: A Quantitative Approach (Hennessy & Patterson) 学习推送第 1 天。

## 摘要

体系结构是「选择与互联硬件组件的科学与艺术」。**Flynn 分类法**、**SIMT**、**Latency vs Throughput** 权衡。**Amdahl 定律**与「使常见情况快」。**CPU 性能公式** `CPU Time = IC × CPI / Clock Rate`。

## 关键要点

- 「科学与艺术」：可量化指标（科学）+ 设计权衡判断（艺术）。
- Flynn 分类法：SISD/SIMD/MISD/MIMD；对现代处理器越来越不够用。
- **SIMT（GPU 执行模型）**。
- **Amdahl 定律**：`Speedup = 1 / ((1-p) + p/n)`；95% 可并行时最大加速 20×。
- "Make the common case fast"——优化优先级从 Amdahl 推导而来。
- **CPU 性能公式**：`CPU Time = IC × CPI / Clock Rate`——三项之间的权衡矩阵。
- **Pentium 4 的 31-stage pipeline** 教训：高频率但单线程性能差。
- 游戏并行化的实际限制：OS 调用、锁竞争、I/O 的串行部分。Unity DOTS 通过重设计数据并行提高有效 p。

## 链接到的概念

- [[amdahls-law]]
- [[flynn-taxonomy]]
- [[cpu-performance-formula]]
- [[latency-vs-throughput]]

## 原文

- 链接到：[[raw/articles/computer architexture a quantitative approach/day1]]
