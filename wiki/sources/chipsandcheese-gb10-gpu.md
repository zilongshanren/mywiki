---
tags: [source, gpu, blackwell, nvidia, igpu]
date: 2026-04-19
sources: 1
---

# Analyzing Nvidia GB10's GPU（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2026 年 3 月的 GB10 iGPU 侧分析。

## 摘要

GB10 iGPU 是 48 SM 的 Blackwell，基本等同于 RTX 5070。但关键是它用的是 **consumer Blackwell（compute capability 12.1）**，不是 datacenter B200/GB300。差异包括 L1/Shared Memory 容量（128 KB vs 256 KB）、FP64 比率（1:64 vs 强 FP64）、5th-gen Tensor Core。文章把 GB10 GPU 与 Strix Halo、Intel Arc B580 在 FluidX3D、VkFFT、FAHBench 等 workload 上横测，以延迟/带宽曲线解释为什么 Nvidia 的大 L2（24 MB）+ 48 个 L1 能在很多场景赢过 AMD 的四层渐进缓存。

## 关键要点

- GB10 不能跑 datacenter Blackwell kernel（cc 12.1 vs 10.0）；官方"同架构"叙事造成 GitHub issue 堆积
- L1 cache 延迟接近 AMD scalar cache，容量大一倍
- SLC（16 MB）对 GPU 几乎不可见，与 L2 非 exclusive，真实角色是引擎间共享
- 计算负载里 GB10 普遍领先 Strix Halo；但 Cyberpunk 2077 因为 Arm ISA 二进制翻译只有 50 FPS（Strix Halo 90 FPS）
- FP16C 模式暴露软件 FP16↔FP32 转换开销
- 两 iGPU 都 bandwidth-limited，Arc B580 的 GDDR6 456 GB/s 在 bandwidth-bound 场景大幅领先

## 链接到的概念

- [[gb10-gpu-blackwell-igpu]]
- [[gb10-memory-subsystem]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/analyzing-nvidia-gb10s-gpu
- 本地：`raw/articles/chipsandcheese.com/2026-03-14_analyzing-nvidia-gb10-s-gpu.md`
