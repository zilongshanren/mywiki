---
tags: [source, cpu, gpu, amd, phoenix, soc, rdna3, zen4, mobile, apu]
date: 2026-04-27
sources: 1
---

# Hot Chips 2023: AMD's Phoenix SoC（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 9 月的文章，结合 AMD Hot Chips 演讲与实测（Ryzen 7 7840HS 及 ROG Ally Z1 Extreme），全面剖析 AMD Phoenix APU 的 CPU、GPU、XDNA AI 引擎和音频协处理器。

## 摘要

Phoenix（TSMC N4，178mm²，254 亿晶体管）是 AMD 迄今最完整的 APU，将 [[computer-systems/zen4-microarchitecture|Zen 4]] 核心与 [[rendering/rdna3-architecture|RDNA 3]] GPU 整合到同一芯片，同时引入 XDNA AI 加速器和音频 DSP。CPU 侧沿用 Zen 4 微架构但 L3 缩减为 16MB（2MB/core）。GPU 侧为 Radeon 780M，6 WGP / 768 SIMD lanes，配 2MB L2 cache，DDR5/LPDDR5 带宽实测超越早期 GDDR5 显卡。XDNA 由 Xilinx AIE-ML tile 构成，16 个 tile，支持 BF16/INT8，面向低功耗 AI 推理；各 tile 有 64KB 数据 SRAM 和 16KB 程序存储，通过专用 512-bit 接口转发累加器输出，无需经过缓存。Infinity Fabric 实现动态时钟，GPU 密集时降频省电，CPU 密集时提频降延迟。文章还介绍了超声波人体感知（20-35KHz）和 Z8 睡眠状态等细节。

## 关键要点

- TSMC N4，178mm²，比上代 Rembrandt 更小，同 25×35mm BGA 封装
- CPU：8 × Zen 4，L3 缩至 16MB；GPU：Radeon 780M，6 WGP，2MB L2 cache
- LPDDR5 延迟相比 Van Gogh 大幅改善（Van Gogh 有严重的 LPDDR 延迟问题）
- XDNA：16 AIE-ML tile，BF16 5TFLOPS，有 50% 稀疏支持，功耗优于 GPU 执行 AI 推理
- Infinity Fabric 动态时钟：GPU 负载时降频，CPU 负载时升频，兼顾带宽与延迟
- Z8 睡眠态：视频播放可高度驻留，媒体引擎支持 AV1 硬解，race-to-idle 策略节能

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[rendering/rdna3-architecture]]
- [[computer-systems/amd-phoenix-soc]]
- [[computer-systems/van-gogh-steam-deck-apu]]

## 原文

- 链接：https://chipsandcheese.com/p/hot-chips-2023-amds-phoenix-soc
- 本地：`raw/articles/chipsandcheese.com/2023-09-16_hot-chips-2023-amds-phoenix-soc.md`
