---
tags: [source, computer-systems, cpu, intel, xeon-phi, avx512, hpc]
date: 2026-04-27
sources: 1
---

# Knight's Landing: Atom with AVX-512（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 12 月的文章，深度测评 Intel Xeon Phi 第二代产品 Knight's Landing（KNL）的微架构特性。

## 摘要

Knight's Landing 是基于 Silvermont 架构的高度改造版本，面向高性能计算（HPC）场景。Intel 将其向量执行单元扩展至 AVX-512，2×512-bit FMA 能力占据核心约 39% 的面积。核心保留了非常小的乱序引擎，但通过 SMT4（四路超线程）来掩盖高延迟。KNL 集成 72 个核心（每片 64 个启用），搭配 16 GB 片上 MCDRAM，理论带宽高达 409 GB/s，显著超越当时主流桌面 GPU。文章通过分支预测、指令缓存、ROB 大小、AVX-512 吞吐量、存储子系统带宽/延迟等微基准全面测量 KNL 性能，揭示其为"围绕喂饱巨大向量单元而构建的小型乱序核心"。SMT4 在向量密集型任务（如 Y-Cruncher）下提供显著增益，但在分支密集型代码中精度急剧下降。

## 关键要点

- KNL 核心面积 2.93 mm²（14nm），其中向量单元占 1.14 mm²（39%）
- AVX-512 FMA 吞吐量与 Skylake-X 持平，但延迟更高（6 vs 4 周期）
- MCDRAM 带宽约 350 GB/s（实测），延迟约 176 ns（比 DDR4 的 147 ns 更高）
- SMT4 通过掩盖分支目标延迟和依赖链停顿，在 Y-Cruncher 等场景下让 KNL 超越 Ryzen 3950X
- 没有 L3 缓存，每核仅有 1 MB L2；MCDRAM 缓存模式下命中效率接近 flat 模式
- Renamer 不支持 zeroing idiom 消除依赖，不支持 move elimination
- SNC4 + Quadrant 模式对带宽/延迟影响有限，表明 mesh 互联带宽充裕

## 链接到的概念

- [[computer-systems/knights-landing-microarchitecture]]
- [[computer-systems/avx512-cache-efficiency]]
- [[computer-systems/clustered-decode-atom]]
- [[computer-systems/gracemont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/knights-landing-atom-with-avx-512
- 本地：`raw/articles/chipsandcheese.com/2022-12-08_knights-landing-atom-with-avx-512.md`
