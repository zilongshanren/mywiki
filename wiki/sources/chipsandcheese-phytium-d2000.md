---
tags: [source, chipsandcheese, cpu, arm, china, phytium, cortex-a72, microarchitecture]
date: 2026-04-27
sources: 1
---

# China's Phytium D2000: Building on A72?（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 9 月的深度评测，对飞腾 D2000 处理器进行性能测试与微架构解析，并结合地缘政治背景作出评价。

## 摘要

D2000 搭载 8 颗 FTC663 ARM 核心（2.3 GHz，双核 cluster），官称面向桌面/笔记本市场，但实测在 7-Zip、Gem5 编译、libx264、Minecraft 等典型客户端负载中被 2015 年的 Intel i5-6600K（仅 4 核）全面碾压。微架构解析揭示 FTC663 与 Cortex-A72 存在大量不可能巧合的相同之处（NOP 行为、BTB 结构、L1i 大小、向量寄存器分配策略等），强烈暗示并非独立研发。飞腾在 ROB 和 store queue 上有所扩容，但保留了 A72 的所有关键弱点（尤其分支预测退步），改进相互抵消。文章从国产化战略角度评价：D2000 短期无法提供有意义的国产替代，长期能力积累方面也令人忧虑。

## 关键要点

- D2000（FTC663 × 8）输给 2015 年四核 Skylake i5-6600K，输给 Neoverse N1 四核
- FTC663 分支预测实测比 Cortex-A72 更差，是最大性能瓶颈
- BTB 无法做 zero-bubble taken branch（Skylake、N1 均可）
- 内存延迟 164 ns，高于双路 Westmere 的 NUMA 远端延迟
- 向量执行宽度 64 位（128-bit NEON 分两次），远落后于 N1（全宽）和 Skylake（AVX2）
- FTC663 与 A72 相似度远超正常代际演进差异，与 Centaur CNS 改版 Haswell 截然不同

## 链接到的概念

- [[phytium-ftc663-microarchitecture]]
- [[neoverse-n1-microarchitecture]]
- [[branch-predictor-design]]
- [[cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/chinas-phytium-d2000-building-on-a72
- 本地：`raw/articles/chipsandcheese.com/2022-09-28_chinas-phytium-d2000-building-on-a72.md`
