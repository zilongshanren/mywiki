---
tags: [source, computer-systems, cpu, qualcomm, arm, microarchitecture]
date: 2026-04-27
sources: 1
---

# Qualcomm's Oryon Core: A Long Time in the Making（Chips and Cheese）

[[george-cozma]] 与 [[chester-lam]] 发表于 2024 年 7 月的文章，通过微基准测试系统拆解了高通 Oryon 核在 Snapdragon X Elite 上的微架构细节。

## 摘要

Oryon 是高通收购 Nuvia（2021 年）后，时隔七年重新推出的自研核，搭载于 Snapdragon X Elite 笔记本平台。文章通过三个维度展开分析：系统架构（三簇四核，12 MB L2/簇，系统级 SLC 缓存）、核心微架构（8 宽前端，680 项 ROB，120 项整数调度，四条 128 位 FP 管道），以及与 Zen 4（AMD Phoenix）和 Meteor Lake（Intel）的对比测试。

主要发现：Oryon 融合了苹果 Firestorm 的大后端哲学与 Kryo 的宽 TLB 传统；BTB 与 L1i 绑定，8 KB 内单周期 taken branch；单核 DRAM 带宽达 80 GB/s，全芯片超 110 GB/s 领先竞品；x86 二进制翻译与 Arm 平台生态碎片化是主要挑战。

## 关键要点

- 12 核三簇，跨簇延迟高于预期（单片 SoC）
- ROB 680 项、整数调度 120 项，远超 Zen 4
- 无 SVE，向量宽度上限 128 位，但四管道 FMA 吞吐与 Zen 4 持平
- L1D 96 KB，L2 延迟约 20 周期，SLC 6 MB
- LPDDR5X 全芯片带宽 >110 GB/s，单核 DRAM 带宽 80 GB/s
- Cinebench 2024：12 核 Oryon 仅以 2% 功耗差胜 8 核 Zen 4（SMT）

## 链接到的概念

- [[oryon-microarchitecture]]
- [[qualcomm-kryo-microarchitecture]]
- [[branch-predictor-design]]
- [[amd-phoenix-soc]]
- [[intel-hybrid-alder-lake]]

## 原文

- 链接：https://chipsandcheese.com/p/qualcomms-oryon-core-a-long-time-in-the-making
- 本地：`raw/articles/chipsandcheese.com/2024-07-10_qualcomms-oryon-core-a-long-time-in-the-making.md`
