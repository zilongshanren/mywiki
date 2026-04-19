---
tags: [source, hardware, memory, igpu, arm]
date: 2026-04-19
sources: 1
---

# Inside Nvidia GB10's Memory Subsystem, from the CPU Side（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 12 月的 GB10（DGX Spark）CPU 侧内存子系统深度实测。

## 摘要

GB10 是 Nvidia 与 Mediatek 合作、把 Blackwell 架构集成进 iGPU 的 SoC，CPU 侧有 10 个 Cortex X925 + 10 个 A725，分两簇。文章用 pointer chasing + per-thread/shared array 带宽测量方法，系统测了 L1/L2/L3/SLC/DRAM 五层延迟带宽，并与 AMD Strix Halo 对照。关键发现：两簇结构非对称（簇 0 = 8 MB L3，簇 1 = 16 MB L3 + 100+ GB/s 外部带宽），LPDDR5X @ 8533 MT/s 给出 113 ns 优秀 DRAM 延迟，SLC 主要服务 CPU↔GPU 共享而非 CPU L4；GPU 高带宽需求会挤出 CPU 延迟（突破 400 ns）。

## 关键要点

- A725 配 512 KB L2 + 21 ns L3 延迟，与高性能目标不匹配，像是面积妥协
- X925 配 2 MB L2 + 14 ns L3，均衡得多
- DSU-120 Snoop Control Unit 管同簇一致性，High Performance Coherent Fabric 管跨簇——跨簇 c2c 最坏 240 ns（Strix Halo ~100 ns）
- iGPU 高带宽会让 CPU 侧 latency 升到 351–400 ns
- 簇 1 外部带宽 100+ GB/s 是 AMD 客户端从未达到的水平

## 链接到的概念

- [[gb10-memory-subsystem]]
- [[cache-coherence-cross-cluster]]
- [[memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-nvidia-gb10s-memory-subsystem
- 本地：`raw/articles/chipsandcheese.com/2025-12-31_inside-nvidia-gb10s-memory-subsystem-from-the-cpu-side.md`
