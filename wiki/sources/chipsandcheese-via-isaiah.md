---
tags: [source, chipsandcheese, cpu, 微架构, x86, via, isaiah, nano]
date: 2026-04-19
sources: 1
---

# The Weird and Wacky World of VIA, Part 1（George Cozma / Chips and Cheese）

[[george-cozma]] 2021 年 9 月发表于 [[chips-and-cheese]] 的 VIA x86 两部曲第一集，深挖 2008 年 VIA Nano（Isaiah 核）的微架构——VIA 通过收购 Cyrix 与 Centaur 拿到 x86 license，最终走 Centaur 的 Samuel 核演化路线，一路到 C3/C7；2008 年用 Isaiah 换代，希望用低功耗定位切下差异化市场。

## 摘要

Isaiah 的尺寸在当时"低功耗"核里属于离谱：3-wide 解码（比同代 Bobcat 宽，比 Goldmont 早 8 年）、4096 项 4-way BTB（Sandy Bridge 级）、tournament 式方向预测器带 3 条 BHT（PDP Alpha EV5 风格）、65 项 ROB（Bobcat 晚 3 年才 56 项）、独立 46+48 项整数/FP 寄存器文件、128-bit 宽 Media A/B 管道、FP add 2 cycle 延迟（至今无 CPU 能复制）、L1D 64 KB 16-way 2 cycle 延迟。代价是 4096 BTB 要 2 气泡（每 3 周期才能处理一条 taken 分支），整体热功耗接近同代 Core 2 Duo，完全撑不起"低功耗"招牌。作者推断 Media 单元本是冲着视频解码去的，但硬件解码器很快普及让这笔投资变废。Isaiah 之后在 Fujitsu 65nm → TSMC 40nm → TSMC 28nm（Isaiah II）逐步缩小，但架构骨架不变；CNS 核到 2021 仍未出货。

## 关键要点

- VIA 的 x86 license 来自 Cyrix + Centaur 双购，Samuel 血脉一路演化
- Isaiah 的 BTB、ROB、FP 管道都达到同代大核水平，但定位低功耗
- FP add 2 cycle、L1D 2 cycle 是 2008 年神级数字
- ROB 测量在 Windows 上得 48 项、Linux 上得 65 项，作者选大值
- 分支预测 BHT 有 3 条 + 1 条 meta，模式识别比 Core 2 强
- Media A/B 命名揭示面向视频解码的 SIMD 设计，市场方向错判

## 链接到的概念

- [[via-x86-isaiah-lujiazui]]
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]
- [[zen2-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/the-weird-and-wacky-world-of-via-the-3rd-player-in-the-modern-x86-market
- 本地：`raw/articles/chipsandcheese.com/2021-09-01_the-weird-and-wacky-world-of-via-the-3rd-player-in-the-moder.md`
