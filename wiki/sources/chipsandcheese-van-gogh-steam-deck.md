---
tags: [source, apu, amd, van-gogh, steam-deck, zen2, rdna2, lpddr5, igpu]
date: 2026-04-27
sources: 1
---

# Van Gogh, AMD's Steam Deck APU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 3 月的文章，深入测评 Steam Deck 搭载的 AMD Van Gogh APU（AMD Custom APU 0405），揭示其作为游戏主机芯片的设计取舍。

## 摘要

Van Gogh 集成四枚 Zen 2 核心（单 CCX，4 MB L3）与 RDNA 2 iGPU（4 WGP，512 FP32 通道），运行在 TSMC 7nm 工艺，最高功耗约 16 W。文章核心发现是 CPU 侧牺牲严重而 GPU 侧相对强健。LPDDR5 内存系统对 CPU 呈现高延迟（超 150 ns，接近 DRAM 的 JEDEC 延迟）和低带宽（约 25 GB/s，远低于理论峰值 88 GB/s），而对 GPU 则能提供超 70 GB/s 的高带宽。时钟爬升策略过于保守（从冷启动到达最大频率需约 1 秒），是 Renoir 笔记本（9.35 ms）的 100 倍。综合而言 Van Gogh 更像一款面向游戏优化的小型主机芯片，CPU 性能绝对数字差，但 RDNA 2 架构本身的延迟与带宽效率优势在低功耗包络下仍得以体现。

## 关键要点

- 16 GB LPDDR5-5500 四通道（128-bit），理论 88 GB/s；CPU 实测约 25 GB/s，GPU 实测 >70 GB/s
- CPU L3 在 Linux schedutil governor 下几乎不可见，切换到 performance 模式后才恢复正常
- GPU iGPU 无 Infinity Cache，以高内存带宽替代（类似 PS5/Xbox Series X 的策略）
- GPU L2 缓存相对 WGP 数目配置偏大（1 MB），小 GPU 客户端数少使延迟更低
- CPU-to-GPU PCIe 带宽超越 RX 6900 XT via PCIe 4.0（受益于无 PCIe 限制的 APU 共享内存）
- RDNA 2 iGPU 的 DRAM 延迟同样糟糕，但带宽充足，高频游戏场景不成瓶颈

## 链接到的概念

- [[rendering/rdna2-architecture]]
- [[computer-systems/zen2-microarchitecture]]
- [[computer-systems/gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/van-gogh-amds-steam-deck-apu
- 本地：`raw/articles/chipsandcheese.com/2023-03-05_van-gogh-amds-steam-deck-apu.md`
