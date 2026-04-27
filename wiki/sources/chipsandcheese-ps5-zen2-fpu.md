---
tags: [source, computer-systems, cpu, amd, zen2, ps5, fpu]
date: 2026-04-27
sources: 1
---

# The Nerfed FPU in PS5's Zen 2 Cores（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 3 月的文章，通过 AMD BC-250（挖矿卡，搭载 PS5 同款 Zen 2 核心）对 PS5 定制 Zen 2 FPU 进行微基准与性能计数器分析。

## 摘要

Fritzchens Fritz 的芯片照片揭示 PS5 的 Zen 2 核心 FPU 面积从 0.91 mm² 缩小至 0.59 mm²。Chester 通过 BC-250 的性能计数器确认：AMD 删除了 FP3 端口，FP2 仅保留存储功能，FMA/加法吞吐量降为 2 管道。寄存器堆容量（160 条目 × 256-bit）和调度队列（36 条 scheduler + 64 条 NSQ）完全保留，延迟也未改变。实测结果：libx264 速度下降 14.9%，Y-Cruncher 下降 16.4%，SSIM 几乎持平（0.45%）；游戏 FPU 使用率极低（不足 1%），对 PS5 游戏场景几乎无影响。整个核心面积仅缩小 5.8%，限制了策略推广价值。Zen 4c 后续采用了更全面的面积缩减路线（35% 全核），不再重复此策略。

## 关键要点

- PS5 Zen 2 删除 FP3，FP2 仅保留 store，等效双管道 FPU
- 寄存器堆、scheduler、NSQ、执行延迟完全保留
- 面积节省：FPU 减 35%，但整核只缩 5.8%
- 游戏负载 FPU 使用率 <1%，对 PS5 使命无实质影响
- 重向量计算（Y-Cruncher）损失 16.4%；scheduler 满载率从 6.48% 升至 17.32%
- 后续 Zen 4c 通过物理设计、SRAM 密度优化实现全核 35% 缩减，不再砍执行管道

## 链接到的概念

- [[computer-systems/zen2-microarchitecture]]
- [[computer-systems/van-gogh-steam-deck-apu]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/dispatch-stall-breakdown]]
- [[computer-systems/non-scheduling-queue]]
- [[computer-systems/zen4c-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/the-nerfed-fpu-in-ps5s-zen-2-cores
- 本地：`raw/articles/chipsandcheese.com/2024-03-20_the-nerfed-fpu-in-ps5s-zen-2-cores.md`
