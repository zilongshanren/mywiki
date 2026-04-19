---
tags: [source, cuda, triton, gpu-优化, cellular-automata]
date: 2026-04-19
sources: 1
---

# Accelerated Game of Life with CUDA / Triton（Boris The Brave）

[[boris-the-brave]] 发表于 2025 年 9 月的长文，用 Conway Game of Life 当标尺做了一轮 GPU kernel 优化阶梯：A40 上从 PyTorch 的 223 ms 一路打到 bitpacked 64-bit CUDA 的 1.84 ms，120× 提升。

## 摘要

文章把一个简单 cellular automata 作为基准负载，挨个对比 PyTorch、torch.compile、naive CUDA、naive Triton、grouped CUDA（每线程多 cell）、位打包（8/32/64 位）几档方案。每一档都贴出 kernel 代码、实测耗时、以及「占 DRAM peak 带宽百分比」这个统一指标。核心结论：(1) torch.compile 能自动给 5× 提升；(2) 手写 CUDA 加 group loop 可达 78% peak；(3) 位打包把存储压到 1 bit/cell 后下限从 11.5 ms 降到 1.4 ms，64-bit CUDA 已逼近；(4) Triton 在这个负载上输给手写 CUDA，可能和 A40 老架构、整数负载无关 tensor core 有关。评论区提醒 Boris 还忽略了「一次算 K 步」的 SRAM 复用空间——这构成续篇 [[sources/boristhebrave-gol-multistep]] 的起点。

## 关键要点

- DRAM 带宽下限（11.5 ms）作为贯穿的标尺
- block size 选型没有解析最优，1×128 因 warp + 连续访问胜出
- 每线程多 cell（group loop）比单线程一 cell 能把 peak 带宽利用率从 44% 抬到 78%
- 位打包 1 bit/cell 把下限本身降到 1.4 ms，64-bit 按位 SWAR 算法离下限很近
- Triton 对这种整数密集、无浮点、无 async copy 的负载发挥有限，不等价于 CUDA
- 放弃了 Hashlife、多步融合等更深度优化，后者在续篇处理

## 链接到的概念

- [[gpu-gol-optimization-ladder]]
- [[cuda-memory-hierarchy]]
- [[gpu-latency-hiding]]

## 原文

- 链接：https://www.boristhebrave.com/2025/09/11/accelerated-game-of-life-with-cuda-triton/
- 本地：`raw/articles/boristhebrave.com/2025-09-11_accelerated-game-of-life-with-cuda-triton.md`
