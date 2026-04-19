---
tags: [source, cuda, 共享内存, 双缓冲, cellular-automata]
date: 2026-04-19
sources: 1
---

# More Accelerated Game of Life（Boris The Brave）

[[boris-the-brave]] 发表于 2025 年 9 月 21 日的后续短文，采纳读者评论「你被 DRAM 带宽绑死了，用 SRAM」，把 Game of Life 再提速 2.7×，来到每步 0.68 ms。

## 摘要

续篇的关键观察：A40 的 DRAM 696 GB/s 只是外层带宽，SM 内部 L1/Shared 潜在能到 67 TB/s。方案是每个 threadblock 一次把一矩形载入 shared memory，在 SRAM 上连续跑 8 步后才写回 DRAM，内部矩形按步数逐圈缩小以避免 border 污染。配套技巧有三样：shared array 双缓冲、每步 `__syncthreads()`、相邻 block 矩形重叠。实测 8 步 5.4 ms，单步 0.68 ms 击穿了原来的 DRAM 带宽下限；继续拉大步数到 > 8 不再收益，计算已饱和。还给了一个小优化：按 1×3 子和预计算，再在行方向累 3 个——少算不少加法，是 [[convolution-separability-blur|可分离卷积]] 思路的再一次应用。尝试用寄存器数组替代 shared memory 反而掉速，Boris 猜是 register 压 occupancy 所致。

## 关键要点

- SM 片上 SRAM 带宽比 DRAM 高约两个数量级，多步融合是把它榨出来的办法
- 每 threadblock 的写回矩形要比读入小 K 圈（K = 融合步数）
- 双缓冲 + `__syncthreads()` 是共享内存多步计算的必备工程件
- 融合步数有上限：计算资源饱和后继续加反而浪费
- 1×3 预求和共享是把 [[convolution-separability-blur]] 思路塞进 cellular automata

## 链接到的概念

- [[gpu-gol-optimization-ladder]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://www.boristhebrave.com/2025/09/21/more-accelerated-game-of-life/
- 本地：`raw/articles/boristhebrave.com/2025-09-21_more-accelerated-game-of-life.md`
