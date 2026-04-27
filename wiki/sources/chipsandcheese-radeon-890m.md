---
tags: [source, chipsandcheese, gpu, amd, rdna35, igpu, strix-point, radeon-890m]
date: 2026-04-27
sources: 1
---

# AMD's Radeon 890M: Strix Point's Bigger iGPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，对 Strix Point APU 中的 Radeon 890M（RDNA 3.5，GFX1150）进行全面测试，重点测量缓存/内存延迟与带宽、计算吞吐、CPU-GPU 带宽以及 Cyberpunk 2077 实际游戏表现。

## 摘要

Radeon 890M 是 AMD 最新移动 iGPU，在 Phoenix（6 WGP RDNA 3）基础上扩大至 8 WGP，架构升级至 RDNA 3.5。本文拆解了其缓存层次（L0 16 KB + L1 256 KB per Shader Array + L2 2 MB），重点对比了与 Phoenix、Intel Meteor Lake、Qualcomm Snapdragon X Elite 以及老款 Steam Deck（Van Gogh）的差距。Radeon 890M 在带宽上明显领先 Meteor Lake，LDS 延迟有显著改善。实测约 96 GB/s 系统带宽（LPDDR5-7500），全局 atomic 延迟也因更好的架构而改善。在 Cyberpunk 2077 中清晰超越 Phoenix，但需要约 50W 系统功耗发挥最佳性能，降至 15W TDP 时约 30 FPS，仍可与 Meteor Lake 竞争。

## 关键要点

- 8 WGP（比 Phoenix 多 33%），两个 Shader Array 各含 4 WGP 和 256 KB L1
- 实测 LPDDR5-7500 带宽约 96 GB/s，与 Snapdragon X Elite Adreno GPU 的 97.82 GB/s 接近
- LDS 延迟大幅改善（超出时钟提升能解释的范围），thread-to-thread atomics 同步受益
- CPU 到 GPU 复制带宽约 38 GB/s，优于 PCIe 4.0 x16 的 32 GB/s 上限
- 峰值计算约 5.1 TFLOPS（wave32 dual-issue），同代 Steam Deck 被远远甩开
- Strix Point 是首次 AMD 移动 iGPU（RDNA 3.5）架构比桌面独显（RDNA 3）更新的产品

## 链接到的概念

- [[rendering/rdna35-architecture]]
- [[rendering/rdna3-architecture]]
- [[computer-systems/strix-point-soc]]
- [[computer-systems/amd-phoenix-soc]]
- [[people/chester-lam]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-radeon-890m-strix-points-bigger-igpu
- 本地：`raw/articles/chipsandcheese.com/2024-08-24_amds-radeon-890m-strix-points-bigger-igpu.md`
