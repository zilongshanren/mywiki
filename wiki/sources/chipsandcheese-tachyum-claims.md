---
tags: [source, cpu, startup, vliw, server, architecture-analysis]
date: 2026-04-27
sources: 1
---

# Tachyum: Too Good to be True?（Chips and Cheese）

[[george-cozma]] 与 [[chester-lam]] 发表于 2022 年 6 月的文章，对 Tachyum Prodigy "万能处理器" 的公开技术资料（Hot Chips 2018 幻灯片、官方规格表、CEO 访谈）进行批判性技术分析。

## 摘要

文章逐一审查了 Prodigy 的架构主张：分支预测器（12-bit Gshare，2000 年代技术）、VLIW 本质（声称 4-wide OoO 但实为 bundle 式调度）、存疑的 iCFP 乱序机制（"poison bits" 暗示，但细节缺失）、向量执行单元（2×1024-bit FMA，算力极强但缓存喂不饱）、虚拟 L3 缓存（每核仅 1 MB L2 + 空闲核贡献）、DDR5-7200 带宽声明（技术上存疑），以及 950W 旗舰 SKU 的热密度问题。整体判断：Prodigy 的多项指标相互矛盾，执行时间线屡次跳票，QEMU 模拟导致主流二进制性能几乎归零，在 AMD MI300、NVIDIA Grace-Hopper 等成熟竞品面前几乎没有竞争空间。

## 关键要点

- 算存比 > 50:1，向量单元注定长期饥渴（对比 AMD MI250X 的 15:1）
- 旗舰 SKU 热密度约 1.9 W/mm²，是 NVIDIA H100 的两倍以上
- x86/ARM/RISC-V 兼容性依赖 QEMU，单线程性能损失约 90%
- ISA 与执行单元深度绑定，后续换代将导致二进制不兼容
- 2017 年成立至今未完成流片；本文发布时距离原定 2020 量产已延期两年

## 链接到的概念

- [[tachyum-prodigy-architecture]]
- [[branch-predictor-design]]
- [[netburst-microarchitecture]]
- [[power-wall]]

## 原文

- 链接：https://chipsandcheese.com/p/tachyum-too-good-to-be-true
- 本地：`raw/articles/chipsandcheese.com/2022-06-28_tachyum-too-good-to-be-true.md`
