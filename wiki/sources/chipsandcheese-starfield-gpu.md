---
tags: [source, gpu, rendering, profiling, rdna3, ada-lovelace, starfield, performance-analysis]
date: 2026-04-27
sources: 1
---

# Analyzing Starfield's Performance on Nvidia's 4090 and AMD's 7900 XTX（Chester Lam & Ryan Mull / Chips and Cheese）

[[people/chester-lam]] 与 Ryan Mull 发表于 2023 年 9 月的文章，使用 Nvidia Nsight Graphics 与 AMD Radeon GPU Profiler 解剖 Starfield 一帧中耗时最长的三个 shader，揭示 [[rendering/rdna3-architecture|RDNA 3]] 在该游戏中相对 Ada Lovelace 出乎意料表现的原因。

## 摘要

Starfield 以 compute shader 为主（含大量 texture 采样），像素着色器次之。在最长的两个 shader 中，AMD 7900 XTX 靠 SIMD 寄存器文件三倍于 Nvidia（192KB vs 64KB）实现更高占用率（~10 threads/SIMD vs 4-5），从而更好地隐藏纹理采样延迟（534 clocks，其中 292 clocks 通过切换线程消化）。第三个 compute shader 中 AMD 反超 RTX 4090：该 shader 以 wave64 模式运行，L2 带宽成为瓶颈，Nvidia RTX 4090 的 L2 利用率超过 90%，而 AMD 凭借 5.78TB/s 高带宽 L2 避免了带宽瓶颈。总结：AMD 的优势来自寄存器文件更大（高占用率）和 L2 带宽更宽；Nvidia 靠庞大 shader array（128 SM）在整帧上仍胜出，RTX 4090 完帧 18.1ms vs 7900 XTX 的 20.2ms。

## 关键要点

- RDNA 3 SIMD 寄存器文件 192KB，是 Nvidia SMSP 64KB 的 3 倍，决定了占用率差距
- 高占用率在 texture sampling 场景（L1 延迟高）下尤为关键
- wave64 模式下每线程用 2× 寄存器容量，占用率降回 8 threads/SIMD，但宽向量弥补
- L2 带宽约 5.78TB/s（RDNA 3），第三 shader 中 Nvidia RTX 4090 反而 L2 bandwidth bound
- Turing（Titan RTX / 3090 Ti 前代）占用率差，issue utilization 仅 26-35%
- Nvidia 低寄存器文件是有意设计：减小 SM 面积以放更多 SM，在寄存器需求低时仍有效

## 链接到的概念

- [[rendering/rdna3-architecture]]
- [[rendering/ada-lovelace-architecture]]
- [[rendering/gpu-latency-hiding]]
- [[rendering/gpu-memory-hierarchy-latency]]
- [[rendering/gcn-wave-occupancy]]
- [[rendering/gpu-register-file-occupancy]]

## 原文

- 链接：https://chipsandcheese.com/p/analyzing-starfields-performance-on-nvidias-4090-and-amds-7900-xtx
- 本地：`raw/articles/chipsandcheese.com/2023-09-14_analyzing-starfields-performance-on-nvidias-4090-and-amds-79.md`
