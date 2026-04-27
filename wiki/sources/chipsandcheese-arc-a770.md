---
tags: [source, rendering, intel, arc, xe-hpg, gpu, microbenchmark]
date: 2026-04-27
sources: 1
---

# Microbenchmarking Intel's Arc A770（Chester Lam & George Cozma / Chips and Cheese）

[[people/chester-lam]] 等人发表于 2022 年 10 月的微测试报告，通过 OpenCL 基准测试系统性分析了 Intel Arc A770（Xe-HPG 架构）的内存层次、带宽扩展性和计算执行特性，并与 Nvidia Ampere、AMD RDNA 2 及若干历史架构进行横向对比。

## 摘要

文章发现 Arc A770 对高占用度有强烈依赖：其 16 MB L2 缓存和内存控制器在满载下可以媲美甚至超越竞争对手，但在低占用度（单 workgroup 或少量活跃 Xe Core）下，VRAM 带宽和缓存扩展性极差——单 Xe Core 的 VRAM 带宽仅约 8 GB/s，连十年前的 AMD GCN 架构都不如。这一根本问题源于 Xe Core 内部的细粒度 round-robin 内存调度和大量 Send 端口竞争，是从 iGPU 时代的 EU 设计继承而来的结构性缺陷。文章还测试了 FMA 吞吐（未达理论值）、执行延迟（高于 AMD/Nvidia 现代 GPU）和 PCIe 带宽，结论是 A770 在高分辨率/高并行场景下有竞争力，但在小 Dispatch 调用密集的场景中会显著落后。

## 关键要点

- L1 至少 192 KB、L2 16 MB（远大于竞争对手），大容量是应对高 VRAM 延迟的主要手段
- VRAM 延迟显著高于 Nvidia Ampere 和 AMD RDNA 2，接近十年前产品水平
- 单 Xe Core VRAM 带宽仅 8 GB/s vs AMD RDNA WGP 的 63 GB/s
- 满载（512 workgroups）下，A770 的 L2 和 VRAM 带宽才能展现竞争力
- FMA 吞吐未达理论值，连 Terascale 2 的理论达成率都不及
- FMA 延迟 ~11-12 cycle，高于 AMD/Nvidia 现代 GPU
- A770 在 GPU 渲染帧中小型连续 Dispatch 调用（如 GHPC 示例中的 barrier 密集序列）面前处于劣势
- 对比 Radeon VII：同样依赖高占用度，但 A770 更依赖，且低占用度 L2 带宽甚至低于 Vega 的 HBM 内存带宽

## 链接到的概念

- [[rendering/xe-hpg-architecture]]
- [[rendering/ada-lovelace-architecture]]
- [[computer-systems/gpu-latency-hiding]]
- [[computer-systems/gpu-latency-microbench-methodology]]
- [[computer-systems/gcn-wave-occupancy]]
- [[computer-systems/async-compute]]

## 原文

- 链接：https://chipsandcheese.com/p/microbenchmarking-intels-arc-a770
- 本地：`raw/articles/chipsandcheese.com/2022-10-20_microbenchmarking-intels-arc-a770.md`
