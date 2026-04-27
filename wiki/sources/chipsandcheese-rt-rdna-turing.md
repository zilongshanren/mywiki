---
tags: [source, raytracing, bvh, rdna2, rdna3, turing, pascal, nvidia, amd, gpu]
date: 2026-04-27
sources: 1
---

# Raytracing on AMD's RDNA 2/3, and Nvidia's Turing and Pascal（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 3 月的文章，通过 AMD Radeon GPU Profiler 和 Nvidia Nsight Graphics 对比四代 GPU 架构（RDNA 2/3、Turing、Pascal）在光线追踪场景下的 BVH 结构选择与硬件利用率差异。

## 摘要

文章的核心主题是：AMD 与 Nvidia 在 BVH 构建策略上走了截然不同的路。AMD 选择窄树（每个 box node 仅 4 个子节点，每个 triangle node 仅 4 个三角形），树深度达 19 跳；Nvidia 选择极宽树（一个节点可以直接包含数百乃至数千个三角形），仅需 3 跳即可到达叶子。AMD 策略对 cache 容量要求高但相交检测吞吐压力小；Nvidia 策略最小化 latency 跳数但需要极高的相交检测吞吐。两家都取得了显著进步：RDNA 3 通过翻倍 L0/L1 缓存、增加 LDS 专用 BVH 指令、扩大向量寄存器文件（提升占用率）来对冲深树的延迟代价；Nvidia Ampere 则将三角形测试速率翻倍、修复 Turing 的 INT32/FP32 分裂问题来增强吞吐。Pascal 在无专用硬件时的纯 compute shader 实现揭示了延迟隐藏不足和指令缓存缺失对 SM 利用率的严重影响。

## 关键要点

- AMD BVH（Cyberpunk 2077 TLAS）：70720 个节点，总大小 11 MB，从根到三角形需 19 跳
- Nvidia BVH（Nsight 呈现，待验证）：3 跳即达叶子，单个 triangle node 可包含数百至数千三角形
- RDNA 2 光追统计：平均 28.7 Gb box tests/s，3.21 Gb triangle tests/s @ 1800 MHz underclocked
- RDNA 3 改进：L0+L1 命中率提升，占用率从 10/16 增至 12/16，box tests 提升至 45.2 Gb/s
- Turing SM：仅 32 warps（vs Pascal 64），INT32/FP32 路径静态分离导致 SM 利用率仅 11%
- Pascal 纯 compute RT：单 dispatch 耗时 26.72 ms，SM 平均 IPC 仅 1.09，大量 long scoreboard stall

## 链接到的概念

- [[rendering/rdna2-architecture]]
- [[rendering/rdna3-architecture]]
- [[rendering/ada-lovelace-architecture]]
- [[rendering/hybrid-raytracing-pipeline]]
- [[rendering/bvh-traversal-hardware]]

## 原文

- 链接：https://chipsandcheese.com/p/raytracing-on-amds-rdna-2-3-and-nvidias-turing-and-pascal
- 本地：`raw/articles/chipsandcheese.com/2023-03-22_raytracing-on-amds-rdna-2-3-and-nvidias-turing-and-pascal.md`
