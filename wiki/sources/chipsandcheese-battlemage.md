---
tags: [source, computer-systems, rendering, intel, gpu, battlemage, arc-b580, xe-core]
date: 2026-04-27
sources: 1
---

# Intel's Battlemage Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 2 月的文章，对 Intel Arc B580（Battlemage）GPU 进行完整的微架构分析，横向对比前代 Alchemist（A770）。

## 摘要

Battlemage 在纸面规格全面缩水的情况下（5 个 Render Slice vs A770 的 8 个、192-bit vs 256-bit 内存总线），依然通过大量架构改进超越了前代。主要变化包括：将 Alchemist 的 XVE 对合并为更宽的单个 XVE（吞吐量不变但控制逻辑更清晰）、L1 data cache 从 192 KB 扩至 256 KB、全局内存 atomic 操作方式彻底重构（解决 A770 的奇异 L2 带宽膨胀问题）、新增 SIMD1 标量内存访问优化路径（比 SIMD16 低约 15 周期延迟）。L2 latency 大幅改善。分歧处理从 Alchemist 的 awkward 双 XVE 共享控制逻辑变为直观的 SIMD16/32 独立行为。文章还通过 VTune 定量展示了 XMX 矩阵单元与向量单元的协同发射情况。

## 关键要点

- Arc B580：5 Render Slice、2560 FP32、18 MB L2、192-bit GDDR6 @ 19 GT/s（456 GB/s）
- 合并后的 XVE 分歧行为更直观：SIMD16/32 各自独立处理，比 Alchemist 更敏捷
- 256 KB L1/SLM 块（vs Alchemist 192 KB），当前 SLM 优先分配
- 标量内存访问（SIMD1）在 Battlemage 上首次带来真实约 15 周期延迟降低
- 全局 atomic 操作彻底重构，性能按 Xe Core 数量线性扩展（前代不行）
- 尽管 VRAM 带宽和 L2 容量少于 RTX 4060，18 MB L2 足以在大多数负载下避免触及带宽上限
- PCIe 4.0 x8 链路在大纹理流加载场景（如 DCS）存在瓶颈

## 链接到的概念

- [[computer-systems/battlemage-architecture]]
- [[rendering/xe-lpg-igpu-architecture]]
- [[rendering/rdna4-architecture]]
- [[rendering/gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-battlemage-architecture
- 本地：`raw/articles/chipsandcheese.com/2025-02-11_intels-battlemage-architecture.md`
