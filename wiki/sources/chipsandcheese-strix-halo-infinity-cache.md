---
tags: [source, gpu, amd, strix-halo, infinity-cache, 内存子系统]
date: 2026-04-27
sources: 1
---

# Evaluating the Infinity Cache in AMD Strix Halo（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 10 月的文章，借助 Strix Halo 开放的 Infinity Fabric 性能计数器首次对 Infinity Cache 实际命中率和带宽放大效果进行量化测量。测试设备由 ASUS 提供（ROG Flow Z13，Ryzen AI MAX+ 395）。

## 摘要

文章设计了一套基于 CS（Coherent Station）与 UMC（Unified Memory Controller）流量差异的测量方法：CS 可见但 UMC 不可见的流量近似为 Infinity Cache 命中。在 3DMark Time Spy Extreme、Wild Life Extreme、GHPC、Unigine Valley/Superposition 等多种负载下系统记录数据，验证 32 MB Infinity Cache 能否防止 256 GB/s LPDDR5X-8000 成为瓶颈。结论是该组合在合理分辨率下工作良好：实测 DRAM 带宽始终低于理论上限，而 CS 侧流量显示若无缓存则多个场景需要 335 GB/s 以上的 DRAM。

## 关键要点

- 测量原理：CS 流量 − UMC 流量 ≈ Infinity Cache 命中流量
- Strix Halo 32 MB Infinity Cache 有效将 GPU 对 DRAM 的带宽需求降低 40–73%（依负载而异）
- 3DMark Time Spy Extreme：CS 侧峰值流量约需 335 GB/s，实测 DRAM 带宽约为一半
- Wild Life Extreme 8K：Strix Halo iGPU 约 10 FPS，DRAM 带宽压力低于 30 FPS 场景
- 分辨率越高，命中率越低；1080P 下 IF 侧流量峰值反而最高（因帧率最高）
- PS5（无 Infinity Cache，448 GB/s GDDR6）在 Time Spy Extreme 带宽需求下勉强够用
- AMD 工具不暴露 Infinity Cache 命中率，Chester 呼吁 AMD 在未来工具中开放此数据
- 误差来源：4 CS 采样（×4 外推）、CPU 流量计入 miss、1 秒采样粒度

## 链接到的概念

- [[rendering/infinity-cache-efficacy]]
- [[computer-systems/strix-halo-soc]]
- [[rendering/rdna4-architecture]]
- [[computer-systems/gpu-memory-hierarchy-latency]]
- [[computer-systems/memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/evaluating-the-infinity-cache-in
- 本地：`raw/articles/chipsandcheese.com/2025-10-22_evaluating-the-infinity-cache-in-amd-strix-halo.md`
