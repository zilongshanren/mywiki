---
tags: [source, gpu, amd, rdna4, register-allocation, occupancy, raytracing, vgpr]
date: 2026-04-27
sources: 1
---

# Dynamic Register Allocation on AMD's RDNA 4 GPU Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 4 月的文章，详解 RDNA 4 动态 VGPR 分配机制的设计动机、实现细节及与 Nvidia setmaxnreg 的异同。

## 摘要

传统 GPU 在线程启动时静态分配寄存器，寄存器用量决定了最大占用率。AMD 的内联光追模式将遍历与着色合并在同一线程中，不同阶段的 VGPR 需求差异很大，导致整体 VGPR 配额必须按峰值设置，压缩了并行度。RDNA 4 为此引入动态 VGPR 分配模式：线程以最小寄存器块启动，运行中通过 `s_alloc_vgpr` 指令按需申请或释放寄存器块（以 16 或 32 个寄存器为粒度）。驱动通过 `SQ_DYN_VGPR` 寄存器直接设置每 SIMD 的活跃线程数，而非由静态寄存器配额推算。死锁避免模式为每个线程保留足够到达最大 VGPR 的余量，以牺牲一定吞吐换取活性保证。Nvidia 的 `setmaxnreg` 机制语义不同：是 warpgroup 内的同步寄存器再分配，灵活度低但与常规线程可共存于同一 SM。

## 关键要点

- 静态 VGPR 分配对光追 inline 模式造成占用率瓶颈，RDNA 4 通过动态模式解决
- `s_alloc_vgpr` 可申请/释放寄存器，SCC 指示成功与否；失败时 shader 需轮询等待
- 死锁避免模式保留 7 个寄存器块（最大 8 块减去 1 个初始块）给单一线程通过
- 动态模式仅限 wave32 compute shader；图形 shader 及 wave64 不支持
- 同一 WGP 内动态与非动态线程不可混用
- 目前仅在 indirect 光追模式（带函数调用）中观察到实际使用动态 VGPR

## 链接到的概念

- [[computer-systems/rdna4-dynamic-vgpr]]
- [[computer-systems/rdna4-architecture]]
- [[computer-systems/gpu-register-file-occupancy]]

## 原文

- 链接：https://chipsandcheese.com/p/dynamic-register-allocation-on-amds
- 本地：`raw/articles/chipsandcheese.com/2025-04-05_dynamic-register-allocation-on-amd-s-rdna-4-gpu-architecture.md`
