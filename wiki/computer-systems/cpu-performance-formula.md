---
tags: [计算机体系结构, 性能]
date: 2026-04-05
sources: 1
---

# CPU 性能公式

```
CPU Time = IC × CPI / Clock Rate
```

- **IC（Instruction Count）**：执行的指令数
- **CPI（Cycles Per Instruction）**：每条指令的平均周期数
- **Clock Rate**：时钟频率

## 三项之间的权衡矩阵

优化任一项可能让另一项变差：

| 优化方式 | IC | CPI | Clock Rate |
|---|---|---|---|
| CISC（x86） | ↓（复杂指令） | ↑（复杂译码） | — |
| RISC（ARM/RISC-V） | ↑（简单指令） | ↓（简单译码） | ↑（利于短周期） |
| 超标量 | — | ↓（并行执行） | — |
| 深度流水线 | — | — | ↑ |
| 短流水线 | — | ↓（分支 hazard 少） | ↓ |

## Pentium 4 的教训

Pentium 4（31 级流水线）追求极高 Clock Rate，但 CPI 因分支预测失败代价大幅上升——**最终单线程性能输给了 13 级流水线的 Pentium M**。

这说明：**三项不能只盯一项优化**。

## RISC vs CISC 的现代收敛

现代 x86 内部把 CISC 指令翻译成 µops（微操作），本质上是动态 RISC 化——IC 的 CISC 优势被抹平。

## 相关

- [[amdahls-law]]
- [[dennard-scaling]]
- [[power-wall]]

## Sources

- [[sources/caqa-day01]]
