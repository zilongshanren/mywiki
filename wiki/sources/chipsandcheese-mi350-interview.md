---
tags: [source, gpu, amd, cdna4, mi350, hpc, ai, chiplet, 访谈]
date: 2026-04-27
sources: 1
---

# AMD's Freshly-baked MI350: An Interview with the Chief Architect（George Cozma / Chips and Cheese）

[[people/george-cozma]] 在 AMD Advancing AI 2025 活动上对 AMD Senior Fellow 兼首席 Instinct 架构师 Alan Smith 进行的访谈，揭示了 MI350 系列多项设计决策背后的工程权衡。

## 摘要

访谈围绕 MI350（CDNA 4）的关键设计决策展开：为何仍基于 GFX9（Vega/GCN 派生）而非 RDNA 3/4 的 GFX11/12；LDS 未与 L1 合并而是扩容至 160 KB 并带宽翻倍；FP6 以与 FP4 相同的速率实现（领先级 FP6 性能是预设目标）；TF32 被移除，以 BF16 替代；XCD 由 40 CU 减至 32 个启用（4 个用于 harvesting，便于 TSMC N3P 良率）；IO Die 维持 N6 节点（SRAMs 等结构不随先进工艺受益）；从四基础 die 改为两基础 die，使 HBM PHY 总线加宽，降低频率和电压从而提升能效。

## 关键要点

- MI350 仍基于 GFX9：CDNA 架构已针对 HPC/AI 深度优化，本代不适合做大微架构变更
- LDS 扩容至 160 KB + 带宽翻倍：直接为 Tensor Core 速率服务，避免 LDS 成为矩阵运算瓶颈
- FP6 = FP4 速率：FP6 被判断为可同时用于推理和训练，决策在数年前锁定，是 MI350 差异化点
- TF32 移除：BF16 可覆盖 TF32 的应用场景，且吞吐量更高；需要 TF32 可用 BF16 仿真或降为 FP32
- 每 XCD 32 CU 启用（36 物理，4 harvesting）：power-of-two 便于张量 tiling 对齐，减少尾部计算开销
- IO Die 留在 N6：HBM PHY、SERDES、Infinity Cache SRAM 在先进工艺下不受益，N6 成熟良率更优
- 双 IO Die 设计：总线加宽，HBM3E PHY 频率/电压降低，提升 I/O 能效，为 compute 留出更多功耗空间
- MI350x 1000 W / MI355x 1400 W，提供气冷和直接液冷两种方案

## 链接到的概念

- [[computer-systems/cdna4-architecture]]
- [[computer-systems/cdna3-mi300x-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-freshly-baked-mi350-an-interview
- 本地：`raw/articles/chipsandcheese.com/2025-06-20_amd-s-freshly-baked-mi350-an-interview-with-the-chief-archit.md`
