---
tags: [计算机体系结构]
date: 2026-04-05
sources: 1
---

# Flynn 分类法

用 **指令流 × 数据流** 分类处理器架构：

| 分类 | 全称 | 含义 | 例子 |
|---|---|---|---|
| **SISD** | Single Instruction, Single Data | 单核单流 | 传统单核 CPU |
| **SIMD** | Single Instruction, Multiple Data | 一条指令对多数据 | AVX、SSE、NEON |
| **MISD** | Multiple Instruction, Single Data | 几乎不存在 | 容错冗余计算（稀有） |
| **MIMD** | Multiple Instruction, Multiple Data | 多核各干各的 | 多核 CPU、集群 |
| **SIMT** | Single Instruction, Multiple Threads | SIMD 的变体 | GPU 执行模型 |

## 对现代处理器的局限

现代处理器越来越不容易归类：
- **超标量**：单核同时执行多条指令（SIMD + MIMD 混合）。
- **SMT/Hyperthreading**：同一核并行两个指令流。
- **乱序执行**：动态重排指令。

## SIMT（GPU）

GPU 的执行模型：一条指令**同时**在一大批线程（warp / wavefront）上执行。每个线程有自己的寄存器和本地变量，但**同一 warp 内指令必须相同**——这就是为什么 GPU 分支会让整个 warp 串行执行各分支（branch divergence）。

## 与 [[amdahls-law]] 的关系

Flynn 的分类帮助识别代码**能不能并行化**：
- SIMD 友好代码（向量/矩阵运算）→ 高 `p`。
- 包含大量分支/不规则访问 → 低 `p`。

## 相关

- [[amdahls-law]]
- [[cpu-performance-formula]]
- [[aos-vs-soa]]

## Sources

- [[sources/caqa-day01]]
