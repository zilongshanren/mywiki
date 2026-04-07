---
tags: [source, 计算机系统, csapp]
date: 2026-04-05
sources: 1
---

# CSAPP Day 1 —— 信息就是上下文中的比特

Computer Systems: A Programmer's Perspective 学习推送第 1 天。

## 摘要

系统视角的总览：**信息 = 比特 + 上下文**、**编译系统四阶段**、**处理器四操作**、**存储层次**、**虚拟内存**、**文件抽象**、**进程抽象**、**Amdahl 定律**。贯穿概念：同一字节序列在不同解释下意义不同。

## 关键要点

- **信息 = 比特 + 上下文**："All information in a system is represented as a bunch of bits"。
- **编译四阶段**：预处理 → 编译 → 汇编 → 链接。
- **处理器四操作**：Load / Store / Operate / Jump。
- 超标量、乱序、分支预测、SIMD 都在 ISA 抽象下隐藏。
- **虚拟内存**：每进程以为自己拥有独立连续地址空间。
- **文件抽象**：文件/设备/网络 = 字节序列的统一 I/O 模型。
- 关注 cache miss 胜过指令级优化——一次 DRAM miss 可淹没整轮优化。
- 字节序（endianness）是经典跨平台 bug。
- 开关语句 → 跳转表（O(1)）；if-else 链 O(n)——编译器优化重要。
- 游戏崩溃栈追踪（il2cpp）需要懂汇编才能读懂。
- Unity ECS 10-100× 性能提升来自数据布局（AoS→SoA），不是"更快的代码"。

## 链接到的概念

- [[bits-and-context]]
- [[compilation-pipeline]]
- [[virtual-memory]]
- [[memory-hierarchy]]
- [[amdahls-law]]

## 原文

- 链接到：[[raw/articles/csapp/day01]]
