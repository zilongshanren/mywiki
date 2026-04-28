---
tags: [gpu, amd, cdna4, mi350, mi355x, hpc, ai, chiplet, 矩阵运算]
date: 2026-04-27
sources: 2
---

# AMD CDNA 4 / MI350 架构

CDNA 4 是 AMD 第四代计算 GPU 架构，以 MI350x（1000 W）和 MI355x（1400 W）为代表产品。它是对 [[cdna3-mi300x-architecture]] 的渐进式迭代，设计重心从扩展总体规模转向精细调优：重点提升低精度矩阵运算吞吐，同时通过更宽的 LDS 和更高效的 I/O 能效维持向量算力领先。

## 执行单元变化

CDNA 4 的 CU 在向量侧保持不变——每 CU 仍有 128 条 FP32 lane，全精度向量算力相对 MI300X 略有下降（CU 数量小幅减少）。主要变化在矩阵侧：

- 低精度矩阵吞吐整体翻倍，MI355X CU 与 Nvidia B200 SM 在 FP6 上持平
- FP6 以与 FP4 相同的速率实现，是 MI350 的差异化设计点；AMD 判断 FP6 在未来既可用于推理，也有潜力用于训练
- TF32 硬件加速被移除，以 BF16 替代（吞吐更高，可软件仿真 TF32 或降为 FP32）

在向量算力方面，AMD 依然靠更多 CU 和更高时钟维持对 Nvidia 的整机领先。

## LDS 扩容与新指令

CDNA 3 的 LDS 容量自 2012 年 GCN 以来一直是 64 KB。CDNA 4 做出了关键改动：

- LDS 容量从 64 KB 增至 160 KB，读带宽翻倍至 256 bytes/clock
- `GLOBAL_LOAD_LDS` 指令扩展至最大 128 bits/lane（原为 32 bits/lane）
- 新增 **LDS 读转置指令**：矩阵乘法时至少有一个操作数访问模式天然 awkward（行主序 × 列主序），LDS 内置的 crossbar 可直接处理转置，减少软件显式转置的开销

每 CU 的 LDS 扩容并未改变 CU 不合并 L1 和 LDS 的基本架构（与 Blackwell SM 128 KB 合一方案形成对比）。CDNA 4 CU 仍有独立的 32 KB L1 向量缓存。Blackwell SM 在 228 KB Shared Memory 配置下单 SM 的软管理存储更大，但 MI355X 合计有约 40 MB LDS 对 B200 的约 33 MB Shared Memory。

## Chiplet 布局演变

CDNA 4 保持 XCD（计算 die） + IO Die 的 chiplet 策略：

- **XCD**：升至 TSMC N3P，每片 36 CU（启用 32，4 用于 harvesting 提升良率）；32 是 2 的幂次，便于张量 tiling 对齐，减少尾部计算开销
- **IO Die**：维持 N6（HBM PHY、SERDES、Infinity Cache SRAM 在先进工艺下不受益，N6 成熟良率更经济）
- **基础 die 数量**：从 MI300X 的 4 片缩减至 2 片，每片 IO Die 改为承接 4 枚 XCD（原为 2 枚）

基础 die 合并带来的直接收益是 HBM PHY 总线加宽，使 I/O 可在更低频率和电压下运行（V² 电压平方功耗缩减），为 compute 释放更多功耗空间。

## 内存子系统

MI355X 升级至 HBM3E，带宽提至 8 TB/s，容量 288 GB，领先 Nvidia B200 的 7.7 TB/s / 180 GB。高带宽对应更好的 FLOP/byte 比率：MI355X 约 0.05 bytes/FP32 FLOP，较 MI300X 的 0.03 有所改善，但仍低于 Blackwell 的约 0.10（Nvidia 更依赖 DRAM 带宽，AMD 更依赖缓存层级）。

## 战略定位

CDNA 4 的策略与 AMD 从 Zen 3 到 Zen 4 的 CPU 路线高度相似：相同的 chiplet 框架，更新的制造工艺，重点调优执行单元中的薄弱环节（矩阵侧）。AMD 在 CDNA 3 上已取得 HPC 超算领域的领先（El Capitan 顶级超算），CDNA 4 选择在胜利方程式基础上稳步演进。这一策略也与 Nvidia Blackwell 对 Hopper 的处理方式相似——向量执行基本不变，专注矩阵侧提升。

## Sources

- [[sources/chipsandcheese-cdna4]]
- [[sources/chipsandcheese-mi350-interview]]
