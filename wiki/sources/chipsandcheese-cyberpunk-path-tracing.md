---
tags: [source, 渲染, 路径追踪, 光线追踪, rdna2, rdna3, ada-lovelace, 上采样, gpu-profiling]
date: 2026-04-27
sources: 1
---

# Cyberpunk 2077's Path Tracing Update（Chips and Cheese）

[[people/chester-lam|Chester Lam]] 于 2023 年 5 月发表的 GPU 性能剖析文章，使用 Radeon GPU Profiler (RGP) 和 Nsight 分析 Cyberpunk 2077 "Overdrive"路径追踪模式在 RX 6900 XT（RDNA 2）、RX 7900 XTX（RDNA 3）和 RTX 4070（Ada Lovelace）上的表现，并对比 FSR 与 XeSS 两种上采样方案。

## 摘要

Overdrive 模式以每像素一条射线在 1920×1080 分辨率发出，单帧光追调用耗时 162 ms（RDNA 2@1.9 GHz）。最核心的性能瓶颈是每线程需用 256 个向量寄存器，将 SIMD occupancy 限制在 4 波前/SIMD（RDNA 2 理论最大 16）。RDNA 3 通过扩大向量寄存器文件（128 KB→192 KB）、增大各级缓存（L0 16→32 KB，L1 128→256 KB，L2 4→6 MB）、引入 LDS 专用 BVH 遍历栈指令大幅提升效率。Ada Lovelace 则以更大的 L2 缓存（同级别命中率 97%）弥补相对较小的 L1 设计，实现 26.37 ms 的优秀成绩。文章还分析了 XeSS（神经网络上采样，依赖 INT8 dot product）与 FSR（纯算法上采样）的 GPU 利用率差异：FSR 指令占用更低、缓存友好，适合小 GPU；XeSS 在极小 GPU（Zen 4 iGPU）上因 dot product 吞吐瓶颈导致上采样耗时大幅增加。

## 关键要点

- 路径追踪瓶颈：高寄存器压力（256 reg/thread）导致 occupancy 低，难以隐藏内存延迟
- RDNA 2 单 shader engine 提前完成后，剩余 25% GPU 长达 91 ms 空转（负载不均）
- RDNA 3 改进：更大 VRF + 缓存 + 专用 BVH LDS 指令，RT 性能对比 RDNA 2 大幅领先
- Ada 的 L2 缓存（大容量 + 高性能）对路径追踪尤为关键，命中率达 97%
- XeSS 使用 INT8 dot product 进行神经网络推理；FSR 使用传统 FP32/INT32 算法
- 路径追踪下 Cyberpunk VRAM 占用 7.1 GB，8 GB 显卡在多任务时存在压力

## 链接到的概念

- [[rendering/path-tracing-basics]]
- [[rendering/ada-lovelace-architecture]]
- [[rendering/rdna3-architecture]]
- [[rendering/rdna2-architecture]]
- [[rendering/shader-execution-reordering]]
- [[rendering/gpu-latency-hiding]]
- [[rendering/dynamic-resolution-scaling]]

## 原文

- 链接：https://chipsandcheese.com/p/cyberpunk-2077s-path-tracing-update
- 本地：`raw/articles/chipsandcheese.com/2023-05-07_cyberpunk-2077s-path-tracing-update.md`
