---
tags: [cpu, microarchitecture, out-of-order, scoreboard, dependency-tracking, history]
date: 2026-04-27
sources: 1
---

# Scoreboard 调度

Scoreboard（计分板）是一种用于跟踪功能单元占用状态与寄存器依赖的硬件调度机制，首次大规模应用于 1964 年的 [[cdc-6600-architecture]]。它是乱序执行的前身，也是现代保留站（Reservation Station）和 Tomasulo 算法的历史参照点。

## 工作原理

Scoreboard 由两张表构成：

1. **功能单元状态表**：记录每个功能单元当前是否忙碌、正在执行哪条指令、操作数来源寄存器、目的寄存器等。
2. **寄存器结果状态表**：记录每个寄存器是否正在被某个功能单元写入（即"飞行中"）。

指令发射前，Scoreboard 检查三个条件：
- 目标功能单元不忙（无结构冒险）
- 源寄存器不处于"等待写入"状态（无 RAW 冒险）
- 目的寄存器不在被其他单元写入（无 WAW 冒险）

满足后，指令读取操作数并开始执行。执行完成后，Scoreboard 广播回写，同时扫描所有等待该寄存器的指令是否满足发射条件。

## 与 Tomasulo 算法的区别

Tomasulo 算法（1967 年，IBM System/360 Model 91）在 Scoreboard 基础上引入了**寄存器重命名**。关键改进：

- 操作数在发射时从寄存器直接复制到**保留站（Reservation Station）**，解除了对物理寄存器的持续依赖
- 通过公共数据总线（CDB）广播结果，等待中的保留站可以直接捕获，无需等回写完成
- 完全消除了 WAR（写后读）和 WAW（写后写）冒险，Scoreboard 对此仍需结构化串行化

Scoreboard 在没有寄存器重命名的情况下，必须通过检查所有待读寄存器来处理 WAR 冒险，每次回写都触发全面扫描。在现代宽发射 CPU 中，这种开销不可接受，因此 Tomasulo 风格的重命名成为标准。

## 现代意义

纯 Scoreboard 机制在现代高性能 CPU 中已不使用，但以下场合仍可见其变体：

- **顺序处理器（in-order）**：如早期 ARM Cortex-A 系列，使用简化 Scoreboard 跟踪长延迟操作（如 L2 miss、除法）以避免流水线气泡
- **GPU 调度**：某些 GPU 流水线用 Scoreboard 追踪纹理读取等长延迟操作，决定何时可以安全调度下一个 wave
- **教学参考**：Scoreboard 是讲解数据冒险与乱序基础的标准教材，因其比完整 Tomasulo 更易理解

## Sources

- [[sources/chipsandcheese-cdc-6600]]
