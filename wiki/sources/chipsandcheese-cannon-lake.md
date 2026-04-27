---
tags: [source, computer-systems, intel, cannon-lake, palm-cove, 10nm, avx512]
date: 2026-04-27
sources: 1
---

# Cannon Lake: Intel's Forgotten Generation（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 11 月，借助微测试数据和 Fritzchens Fritz 的芯片解剖照片，对 Intel Cannon Lake（Palm Cove 核心，10nm 工艺）进行了全面分析，涵盖工艺问题、核心微架构、AVX-512 实现、iGPU（Gen 10）和系统代理设计。

## 摘要

文章使用唯一出货的 Core i3-8121U 进行基准测试，证实 10nm 早期在性能/功耗上彻底失败：在相同功耗窗口下不如 14nm 的 Kaby Lake，甚至在低功耗段输给同为 14nm 的 Atom 架构 Goldmont Plus。核心（Palm Cove）与 Skylake 几乎相同，仅有调度器和队列的微小扩大，以及 AVX-512 的加入。AVX-512 实现存在 256/512-bit FMA 模式不可并存的限制（被卡在 1 IPC）。iGPU（Gen 10）因良品率不足被完全禁用，是 Cannon Lake 出货失败的直接原因，但其设计创新（SLM 移入子切片、更大 L3、媒体引擎）全部在 Ice Lake（Gen 11）中实现量产。

## 关键要点

- 10nm 密度优势真实（Palm Cove 核心面积仅为 Kaby Lake 的 43%），但性能/功耗未改善
- AVX-512 在 libx264 上有优势，但去掉指令集加成后纯整数测试（7-Zip）10nm 依然落后
- 调度器 58→62 项，加载追踪 72→80 项，存储队列 56→58 项——纯微调
- BTB 约 4608 项（vs Skylake ~4096），密集分支零气泡行为略改善
- AVX-512 FMA 实现：port 0/1 的两个 256-bit FMA 融合为一个 512-bit 单元，不可切换模式，混合指令流被卡在 1 IPC
- Gen 10 iGPU 占芯片面积 45%，5 个子切片 × 8 EU = 320 FP32 lanes（Gen 9.5 为 192）
- Gen 10 引入 SLM 入子切片（后在 Ice Lake 量产），iGPU L3 重布局缩短访问路径
- 系统代理新增大型 IPU（摄像头 RAW 处理）和 GNA（语音 AI 加速），预示 Intel SoC 化方向
- iGPU 被禁用后需搭配独显运行，彻底破坏超低功耗定位

## 链接到的概念

- [[computer-systems/cannon-lake-microarchitecture]]
- [[computer-systems/skylake-microarchitecture]]
- [[computer-systems/sunny-cove-microarchitecture]]
- [[rendering/xe-hpg-architecture]]
- [[computer-systems/dennard-scaling]]

## 原文

- 链接：https://chipsandcheese.com/p/cannon-lake-intels-forgotten-generation
- 本地：`raw/articles/chipsandcheese.com/2022-11-15_cannon-lake-intels-forgotten-generation.md`
