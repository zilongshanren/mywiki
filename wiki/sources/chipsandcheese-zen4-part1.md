---
tags: [source, computer-systems, amd, zen4, microarchitecture, frontend, avx512]
date: 2026-04-27
sources: 1
---

# AMD's Zen 4 Part 1: Frontend and Execution Engine（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 11 月，Zen 4 架构深度解析的第一部分，聚焦前端（分支预测、微操作缓存）、重命名/乱序资源和 AVX-512 实现。

## 摘要

文章通过微测试详细测量了 Zen 4 相对 Zen 3 的改进，并与 Intel Golden Cove 进行横向对比。前端方面，L2 分支预测器大幅升级，L1/L2 BTB 容量增加且 L2 BTB 惩罚从 3 cycle 降至 1 cycle，微操作缓存从 4K 增至 6.75K 项。乱序资源方面 ROB 增加约 25%，整数物理寄存器文件利用效率较高。执行单元布局与 Zen 2/3 相同（2×256-bit FMA + 4×256-bit ALU），AMD 选择用频率换性能。AVX-512 实现为"double pumping"（512-bit 指令在进入 256-bit 管道前分为两半），L1D 带宽未增，512-bit 存储消耗两个存储队列项。

## 关键要点

- L2 BTB 惩罚 3→1 cycle 是前端最显著的改进之一
- L1 BTB 容量约 1024-3072 项（依分支密度），借助 BTB 条目共享机制
- 微操作缓存 6.75K 项，NOP 双重融合可达 12 NOP/cycle（特殊路径）
- ROB 容量 320 项（+25%），存储队列维持 64 项不变
- Golden Cove 重命名器可消除更多 idiom（如 MOV r,0）；Zen 4 在 XMM zeroing 上消耗寄存器（Zen 2 不消耗）
- AVX-512 首次由 AMD 桌面架构支持，掩码寄存器文件约 52 项（Intel 服务端规模的一小部分）
- Intel hybrid 芯片（Alder Lake）不启用 AVX-512，Zen 4 因此在支持 AVX-512 的应用中具备独特竞争优势

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/zen2-microarchitecture]]
- [[computer-systems/zen3-bottlenecks]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/op-cache-decoded-uop-cache]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-zen-4-part-1-frontend-and-execution-engine
- 本地：`raw/articles/chipsandcheese.com/2022-11-05_amds-zen-4-part-1-frontend-and-execution-engine.md`
