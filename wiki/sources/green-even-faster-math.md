---
tags: [source, 数学, 数值计算, 浮点, minimax, GDC]
date: 2026-04-27
sources: 1
---

# Even Faster Math Functions（Robin Green / Bases and Frames）

[[robin-green]] 发表于 2020 年 4 月的文章，是其 GDC 2020「Math for Game Programmers」Summit 演讲稿（因 GDC 2020 取消而以扩展版发布），主题是把 GDC 2002 *Faster Math Functions* tutorial 更新至 2020 年的技术状态。

## 摘要

二十年间数值计算领域有三个方向的进展：（1）**数学库标准化运动**正在把「末位精确（last-bit accurate）」作为可实现目标推广，不同平台的 `sinf()` 将趋于给出相同结果；（2）**Sollya** 等工具可以对 minimax 多项式进行全局优化，而不仅仅是截断精心构造的系数；（3）**FloPoCo** 可以在 VHDL 层面生成针对特定字长优化的定点/浮点数学函数，把「定制硬件」的精度/面积权衡直接暴露给工程师。此外，**双分区表（bipartite table）**方法可以用更少存储换出等价精度；**离散数字振荡器（Digital Resonator）**提供了无需 sin/cos 调用的正弦波生成路径；Taylor 级数在一个冷知识用途上仍然成立——用于生成 reciprocal/sqrt/inverse-sqrt 的 bit-twiddling 初始猜测。

## 关键要点

- **Sollya** 是当代生成 minimax 多项式的首选工具；相比 Mathematica/Maple，它对定点/浮点字长约束有原生支持。
- **FloPoCo** 把 Verilog/VHDL 层的数学单元生成自动化——对嵌入式/FPGA 的「我只有 N 位精度需求」场景有直接价值。
- **双分区表（Bipartite table）**：把输入的高位和低位分别索引两张小表，查结果相加，比单张大表占空间小、比多项式计算快——在 SPU/GPU 的 LUT 带宽瓶颈场景下值得考虑。
- **离散数字振荡器（Digital Resonator / DDO）**：一个简单的两元线性递推就能持续生成高精度正弦波，无需在主循环里反复调用 `sinf`。
- **Taylor 的合法用途**：bit-twiddling 的 reciprocal/sqrt 初始猜测（如 Quake3 inverse-sqrt 的 magic number 背后的原理）本质上是 Taylor 1 阶近似，在这个特殊场合是对的。
- 相较 2002 年演讲，「last-bit accurate 作为行业目标」是最显著的范式转移：精度不再是「各自实现者的灰色地带」。

## 链接到的概念

- [[faster-math-functions]]
- [[robin-green]]
- [[fp64-sincos-minimax]]

## 原文

- 链接：https://basesandframes.wordpress.com/2020/04/04/even-faster-math-functions/
- 本地：`raw/articles/basesandframes.wordpress.com/2020-04-04_even-faster-math-functions.md`
