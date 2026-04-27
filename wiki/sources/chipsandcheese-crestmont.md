---
tags: [source, computer-systems, intel, atom, e-core, crestmont, meteor-lake]
date: 2026-04-27
sources: 1
---

# Meteor Lake E-Core：Crestmont 的渐进式演进（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 5 月的深度微架构评测，系统对比 Crestmont 与前代 [[gracemont-microarchitecture|Gracemont]] 的差异，测试平台为 Core Ultra 7 155H。

## 摘要

Crestmont 是 Intel 为 Meteor Lake 设计的新 E-Core 架构，同时承担主 E-Core 与低功耗 LPE-Core 两种角色。文章通过微基准测试逐一拆解分支预测、前端解码、重命名、乱序执行、内存子系统等模块，结论是：Crestmont 对 Gracemont 的改进是真实但保守的——更宽的重命名器（6-wide，比 Gracemont 的 5-wide 提升），更大的 L2 TLB（3072 条目 vs 2048），BTB 容量从 5120 增至 6144，FP 除法器延迟减半。但寄存器堆、LoadStore 队列、ROB 均未变化，AVX-512 仍缺席。LPE-Core 因无共享 L3 而性能受限。作者认为 Meteor Lake 复杂的芯片粒工程挑战是 Crestmont 保守的根本原因。

## 关键要点

- Crestmont 6-wide 超标量乱序，基本是增强版 Gracemont
- BTB 扩至 6144 条目，分支预测器扫描宽度 128B/cycle（Gracemont 为 32B/cycle）
- 重命名器升至 6 uop/cycle；分簇解码机制（[[clustered-decode-atom]]）继承自 Gracemont/Tremont
- L2 TLB 扩至 3072 条目（6-way），FP 除法器延迟 5 cycle（前代 10 cycle）
- LPE-Core 无 L3，2 MB L2 作 LLC，高 DRAM 延迟严重拖累带宽
- L3 带宽仅 ~10–12 B/cycle，与 Alder Lake Gracemont 相比无改善
- Intel 工程带宽被 Meteor Lake 芯片粒切换所消耗，导致 CPU 改动保守

## 链接到的概念

- [[crestmont-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[clustered-decode-atom]]
- [[intel-hybrid-alder-lake]]
- [[golden-cove-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/meteor-lakes-e-cores-crestmont-makes-incremental-progress
- 本地：`raw/articles/chipsandcheese.com/2024-05-13_meteor-lakes-e-cores-crestmont-makes-incremental-progress.md`
