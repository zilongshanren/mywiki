---
tags: [source, cpu, arm, cortex-a725, microarchitecture, gb10, efficiency-core]
date: 2026-04-27
sources: 1
---

# Arm's Cortex A725 ft. Dell's Pro Max with GB10（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2026 年 1 月的文章，以 Dell Pro Max（搭载 Nvidia GB10）为测试台，深入分析 Cortex-A725 效率核微架构。

## 摘要

A725 是 Arm 7 系列效率核的最新代，5-wide 乱序，ROB 224 entry（从 A710 的 160 扩容）。文章最重要的结论是：A725 去掉了 MOP Cache，改用预解码 sideband bits 降低解码成本，因为 MOP Cache 与预解码叠加属于过度设计。在结构调整上，A725 对关键乱序结构（ROB、整数 RF、内存队列）扩容，同时缩减 FP/向量资源（向量 RF 从 128-bit 条目改为 64-bit）以节省面积，并将 TLB entry 从指令侧向数据侧转移。与 Intel Skymont 的横向对比显示两者分支预测能力相近，但 Skymont 更高的主频在核心密集型 workload 上占优；A725 在内存延迟主导的场景几乎不受时钟影响。

## 关键要点

- 放弃 MOP Cache，采用 5-bit predecode sideband——预解码已足够，MOP Cache 是冗余
- ROB 从 160 扩至 224（对标 Skylake/Zen 2 量级）
- FP/向量寄存器由 128-bit 条目改为 64-bit，128-bit 向量重命名 entry 减少
- L1 DTLB 32→48 entry，L1 ITLB 48→32 entry（数据侧更重要）
- L2 TLB 升至 1536 entry，支持 "8×32" 页面聚合（类 AMD page smashing）
- 四整数管道全部支持单周期操作（A710 有一管只能多周期）
- SPEC CPU2017：时钟不足导致在核心密集 workload 上输给更高频的 Neoverse N2；内存延迟主导场景与 Neoverse N2 持平

## 链接到的概念

- [[computer-systems/cortex-a725-microarchitecture]]
- [[computer-systems/cortex-a710-microarchitecture]]
- [[computer-systems/skymont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-a725-ft-dells-pro-max
- 本地：`raw/articles/chipsandcheese.com/2026-01-27_arms-cortex-a725-ft-dells-pro-max-with-gb10.md`
