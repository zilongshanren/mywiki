---
tags: [source, chipsandcheese, cpu, amd, k8, athlon64, netburst, 历史]
date: 2026-04-27
sources: 1
---

# AMD's Athlon 64: Getting the Basics Right（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 7 月的文章，以 Athlon FX-62（90nm，2.8 GHz）和 Athlon 64 6000+（65nm）为样本，对 AMD K8 微架构进行深度解析，并与同期 [[netburst-microarchitecture|Intel Netburst]] 做全面对比。

## 摘要

K8 是 K7 的保守演化版本：添加 x86-64 支持、片上集成内存控制器（IMC）、少量缓冲区扩容，其他几乎不变。对比纸面规格远胜的 Netburst，K8 凭借低延迟 IMC（DRAM 延迟约 60ns vs Netburst 的 94ns+）、低惩罚存储转发（失败仅 10-15 周期 vs Netburst 的 51-100 周期）和 3 周期 L1D 延迟，在实际应用中保持竞争力。"把基础做对"而非追求激进创新，是 K8 得以在 2003-2006 年与更大规模公司竞争的核心原因。

## 关键要点

- K8 整数侧为三条对称通用流水线（含 AGU+ALU），load-op 指令不拆分，节省 ROB/调度资源
- BTB 与 L1i 紧耦合（coupled BTB），简化前端但削弱了 L1i miss 后的预取能力
- FPU 作为独立协处理器，128-bit SSE 操作拆分为 2 个 64-bit micro-op，向量带宽受限
- K8 统一 load/store queue（2 个队列共 12+32 项），不分 load/store 独立 queue
- 直到 2006 年 Intel Merom 出现，K8 才真正失去竞争力

## 链接到的概念

- [[amd-k8-microarchitecture]]
- [[netburst-microarchitecture]]
- [[branch-predictor-design]]
- [[memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-athlon-64-getting-the-basics-right
- 本地：`raw/articles/chipsandcheese.com/2022-07-28_amds-athlon-64-getting-the-basics-right.md`
