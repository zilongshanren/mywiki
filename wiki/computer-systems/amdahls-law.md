---
tags: [计算机体系结构, 性能]
date: 2026-04-05
sources: 2
---

# Amdahl 定律

**并行加速的理论上界**：

```
Speedup = 1 / ((1 - p) + p/n)
```

其中 `p` 是可并行化部分的比例，`n` 是处理器数量。

## 残酷的上界

当 `n → ∞`，加速比趋近 `1 / (1 - p)`：

| p（并行部分） | 最大加速 |
|---|---|
| 50% | 2× |
| 80% | 5× |
| 90% | 10× |
| 95% | 20× |
| 99% | 100× |

**95% 可并行时，哪怕无限核，最多加速 20×**——剩下 5% 的串行部分天花板。

## "Make the common case fast"

Amdahl 定律直接推出经典优化原则：**优化用得最多的那部分**。优化罕用部分哪怕优化 1000× 也不会产生明显效果。

## 游戏引擎含义

游戏代码的串行部分通常比预想大：
- OS/Driver 调用
- Lock contention
- I/O 等待
- Renderer submit（必须串行）
- Main thread 的大量固有工作

Unity 的 DOTS 是通过**重新设计数据布局和任务系统**，让更多代码变得**数据并行**——相当于提高 `p` 值，而非增加核数。

## 相关
- [[cpu-performance-formula]]
- [[aos-vs-soa]]
- [[power-wall]]——导致多核时代与 Amdahl 的硬约束
- [[flynn-taxonomy]]
- [[optimization-leverage-ratio]] —— Supnik 的工程化版本：profile 读出来的杠杆率

## Sources

- [[sources/caqa-day01]]
- [[sources/csapp-day01]]
