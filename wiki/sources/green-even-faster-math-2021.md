---
tags: [source, 数学, 数值计算, FPGA, 硬件数学, GDC]
date: 2026-04-27
sources: 1
---

# Even Faster Math Functions, 2021 Edition（Robin Green / Bases and Frames）

[[robin-green|Robin Green]] 2021 年 9 月 6 日发布的 GDC 2021 虚拟讲座配套文章。GDC 2021 仅分配 30 分钟，Green 砍掉了 2020 年扩展版的大部分内容，专注于**硬件层面数学函数实现**的核心方法论，面向 FPGA 设计者。

## 摘要

本文是 [[sources/green-even-faster-math|2020 年扩展版]] 的精简变体。Green 明确说明：30 分钟时长迫使他聚焦于「在硬件里工作最好的主要思想」，实质上是一个 FPGA 数学单元设计的压缩课程。涵盖五个主题：**数字递推算法（Digit Recurrence）**、**小乘法器与位堆（Small Multipliers and Bit Heaps）**、**CORDIC 的正确用法（CORDIC 是锤子，只用于钉子）**、**双分区表（Bipartite Tables）**和**等间距步长的三角函数（Trig at Regularly Spaced Steps）**。内容高度浓缩，鼓励读者追溯参考文献获取细节——从 Green 自己的话看，这更像一张「FPGA 数学实现的地图」，而非自包含的教程。

与 2020 年版相比，本文去除了 Sollya/FloPoCo 工具介绍、离散数字振荡器（DDO）的详细推导，以及 minimax 多项式与 Taylor 的对比论证；主干转向 FPGA 的门级/位级优化方法。

## 关键要点

- **数字递推（Digit Recurrence）**：一次输出一位结果的迭代算法，面积效率高，适合资源受限的 FPGA 场景。
- **位堆（Bit Heap）**：用压缩器树（compressor tree）延迟加法，把多条乘积项合并成一次进位传播——比串行加法更省延迟和面积。
- **CORDIC 的用途限制**：CORDIC 在旋转/三角函数上的经典用途被过度推广；在可以用小乘法器的 FPGA 上，多项式近似往往更优，"CORDIC is a hammer, use it only for nails"。
- **双分区表**：把输入的高位和低位分别索引两张小查找表、结果相加，达到单张大表的精度却只用更小存储——已在 2020 年版讨论，本文再次强调为 FPGA 设计的推荐路径。
- **等间距三角函数（Trig at Regularly Spaced Steps）**：当输入是等间距步长（如音频合成、旋转矩阵序列），可以用递推而非逐次查表，大幅降低每步开销。
- 文章定位为参考索引而非完整教程，实质内容依赖配套参考文献。

## 链接到的概念

- [[faster-math-functions]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2021/09/06/even-faster-math-functions-2021-edition/
- 本地：`raw/articles/basesandframes.wordpress.com/2021-09-06_even-faster-math-functions-2021-edition.md`
- 前篇：[[sources/green-even-faster-math]] — GDC 2020 扩展版（Sollya / FloPoCo / DDO / bipartite tables）
