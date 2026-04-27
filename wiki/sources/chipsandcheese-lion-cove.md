---
tags: [source, computer-systems, intel, p-core, lion-cove, lunar-lake]
date: 2026-04-27
sources: 1
---

# Intel Lion Cove 架构预览（George Cozma / Chips and Cheese）

[[people/george-cozma]] 发表于 2024 年 6 月的架构预览文章，介绍 Lion Cove——Intel P-Core 在 Lunar Lake 中的新一代微架构。

## 摘要

Lion Cove 是 [[golden-cove-microarchitecture|Golden Cove]] 系列的继任者，最大变化是将统一数学调度器（Unified Math Scheduler）拆分为独立的整数调度器（6 端口）和向量调度器（4 端口）。拆分带来两个好处：可对向量调度器独立做时钟门控以节省功耗，同时降低了端口设计复杂度。缓存层次也做了重构：原 L1 降级为 L0（4 cycle，48 KB），新增 192 KB 的 L1（9 cycle），L2 增至 3 MB。Lunar Lake 版本移除了超线程以简化 Thread Director 调度，但架构通过"Sea of Cells"可定制化设计，可在未来其他产品中重新启用。核心宽度从 6-wide 扩至 8-wide，ROB 从 512 扩至 576，整数 ALU 增至 6 个，整数乘法器首次增至 3 个，向量 SIMD ALU 增至 4 个，IPC 提升约 14%。

## 关键要点

- 分离整数/向量调度器是 P6 系以来最大的微架构结构变化
- 双调度器允许向量部分独立时钟门控，功耗与面积均改善
- 新增 L0/L1 两级缓存：L0 恢复 Skylake 级 4 cycle 延迟，L1 192 KB 充当缓冲
- 8-wide 宽度，ROB 576 条目，整数乘法器 3 个（首次实现 >1/cycle 整数乘）
- Lunar Lake 版移除超线程；其他产品形态可按需恢复
- Sea of Cells 设计理念让单架构支持多产品定制化

## 链接到的概念

- [[lion-cove-microarchitecture]]
- [[golden-cove-microarchitecture]]
- [[intel-hybrid-alder-lake]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-lion-cove-architecture-preview
- 本地：`raw/articles/chipsandcheese.com/2024-06-04_intels-lion-cove-architecture-preview.md`
