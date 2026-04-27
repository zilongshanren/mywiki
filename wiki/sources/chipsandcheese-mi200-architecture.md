---
tags: [source, chipsandcheese, amd, gpu, hpc, cdna, mi200, instinct]
date: 2026-04-27
sources: 1
---

# Hot Chips 34 – AMD's Instinct MI200 Architecture（Chester Lam & Mohamed Ahmed / Chips and Cheese）

[[chester-lam]] 与 [[mohamed-ahmed-chipsandcheese]] 发表于 2022 年 9 月的文章，分析 AMD 在 HC34 展示的 Instinct MI200（CDNA2）加速卡架构。

## 摘要

MI200 延续 CDNA1（MI100）路线但在数值精度层面跨越式提升：SIMD 单元全面升级为 64 位宽，实现全速 FP64，每 CU 的 FP64 FLOPS 是 MI100 的 4 倍，同时接近 NVIDIA H100 的 FP64 水平。双 GCD chiplet 设计通过片内 Infinity Fabric 链路相连，由于带宽仍不足以暴露统一内存，系统级暴露为两个独立 GPU。MI200 通过 Infinity Architecture 3 实现了与 AMD Trento EPYC 的 CPU-GPU 硬件缓存一致性，以及将 NIC 直连到 GPU 以利用 HBM 带宽，最终助力 AMD 将 Frontier（世界第一超算）落地。文章还预告了 CDNA3（MI300）将采用 CPU+GPU chiplet 封装、统一内存架构与 FP8 矩阵支持。

## 关键要点

- 全速 FP64：CDNA2 每 CU FP64 吞吐量是 CDNA1 的 4 倍
- 统一向量/矩阵寄存器文件：从 MI100 的分离设计合并为 512 项统一 RF
- 每 GCD HBM2E 带宽 1.6 TB/s，L2 带宽 4096 B/clk（MI100 的 2 倍）
- 双 GCD 通过片内 IF 互联，但暴露为两个 GPU（带宽限制所致）
- MI250X 与 AMD Trento 之间实现硬件 CPU-GPU 缓存一致性
- Frontier（世界第一）和 LUMI（世界第三）超算均采用 MI250X

## 链接到的概念

- [[cdna2-mi200-architecture]]
- [[mcm-gpu-design]]
- [[gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/hot-chips-34-amds-instinct-mi200-architecture
- 本地：`raw/articles/chipsandcheese.com/2022-09-18_hot-chips-34-amds-instinct-mi200-architecture.md`
