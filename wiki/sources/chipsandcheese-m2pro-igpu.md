---
tags: [source, rendering, apple, igpu, gpu, apple-silicon, bandwidth]
date: 2026-04-27
sources: 1
---

# A Brief Look at Apple's M2 Pro iGPU（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2023 年 10 月的文章，通过 AWS M2 Pro 裸金属实例，用 OpenCL 微基准测评 M2 Pro iGPU 的缓存层次、带宽、本地内存和 atomic 延迟。

## 摘要

文章揭示 M2 Pro iGPU 的关键权衡：8 KB L1 数据缓存极小（2011 年前水平），但 3 MB L2 缓存带宽超过 1 TB/s，256-bit LPDDR5 内存总线提供超过 200 GB/s DRAM 带宽。这一"以 L2/DRAM 带宽弥补 L1 容量"的策略使 M2 Pro 在带宽受限场景（FluidX3D LBM 模拟）大幅领先 AMD Phoenix。DRAM 延迟（342 ns）是弱点，比 Phoenix 高，接近旧款 Intel HD 530。文章最后对 AMD Strix Halo 的可行性表示怀疑——M2 Pro 模式的高成本在 PC 市场缺乏规模经济支撑。

## 关键要点

- 19 核 iGPU，~289 mm² 单片硅，AWS M2 Pro 裸金属实例可访问
- 8 KB L1d 数据缓存 + 24 KB 纹理缓存（分离）
- 3 MB L2，>1 TB/s 带宽（超越旧款独显 Radeon R9 390 的 L2 带宽）
- DRAM：256-bit LPDDR5，>200 GB/s，但延迟 >342 ns
- Global atomic 延迟 58.57 ns，接近 RDNA 2
- FluidX3D 大幅领先 AMD Phoenix，被 GDDR6 独显超越
- M3 Pro 改用 192-bit（150 GB/s），Chester 认为 200 GB/s 对多数应用并非必需

## 链接到的概念

- [[rendering/apple-m2-pro-igpu]]
- [[rendering/rdna3-architecture]]
- [[rendering/gcn-wave-occupancy]]
- [[computer-systems/van-gogh-steam-deck-apu]]

## 原文

- 链接：https://chipsandcheese.com/p/a-brief-look-at-apples-m2-pro-igpu
- 本地：`raw/articles/chipsandcheese.com/2023-10-31_a-brief-look-at-apples-m2-pro-igpu.md`
