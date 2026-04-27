---
tags: [source, computer-systems, cpu, loongson, chinese-cpu]
date: 2026-04-27
sources: 1
---

# Loongson 3A6000: A Star among Chinese CPUs（George Cozma & Chester Lam / Chips and Cheese）

[[people/george-cozma]] 与 [[people/chester-lam]] 发表于 2024 年 3 月的文章，对龙芯 3A6000 进行全面微架构分析，与 AMD Zen 1/2/4 及 Intel Golden Cove 做详细比对。

## 摘要

龙芯 3A6000 搭载 LA664 核心，是 3A5000（LA464）的重大升级：从 4 宽乱序扩展至 6 宽，新增 SMT，大幅扩大乱序缓冲区，并修复了长期拖累性能的 DDR4 控制器。分支预测器大幅改进，接近 Zen 2 水准，并修复了 3A5000 在 L2 指令带宽上的严重缺陷。整数执行基本保持 4 管道格局，但浮点/向量方面扩展至 4 个 256-bit 向量加管道，L1D 降至 3 周期延迟。主内存延迟从 144 ns 降至 104 ns。综合性能约在 Zen 1 水平，在 2.5 GHz 下表现出色，但受制于低主频，实际应用中仍逊于 Zen 2。SMT 实现保守（大多数资源静态平分），首代 SMT 规避风险合理。

## 关键要点

- LA664：6 宽乱序，ROB 规模接近 Zen 3，首次引入 SMT
- 分支预测器接近 Zen 2 准确度，远超 3A5000
- L1D 延迟 3 周期（LA464 为 4 周期），L2 延迟 12 周期
- 向量 FP 加法：4 管道 × 256-bit，优于 x86 的 2 管道；但 FMA 吞吐量仍是 Zen 2 的一半
- L1D 写带宽达 512 B/cycle，与 Intel Golden Cove 并列
- DRAM 延迟 104 ns（DDR4-2666），控制器大幅改善但仍不算出色
- SMT 保守实现（静态分区），避免第一代出错

## 链接到的概念

- [[computer-systems/loongson-3a5000-microarchitecture]]
- [[computer-systems/loongson-3a6000-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/zen2-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/non-scheduling-queue]]

## 原文

- 链接：https://chipsandcheese.com/p/loongson-3a6000-a-star-among-chinese-cpus
- 本地：`raw/articles/chipsandcheese.com/2024-03-14_loongson-3a6000-a-star-among-chinese-cpus.md`
