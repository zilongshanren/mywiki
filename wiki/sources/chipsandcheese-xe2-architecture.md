---
tags: [source, gpu, intel, xe2, igpu, lunar-lake, rendering]
date: 2026-04-27
sources: 1
---

# Lunar Lake's iGPU: Debut of Intel's Xe2 Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 10 月的 iGPU 架构评测，通过微基准与游戏测试对比 Xe2、Xe-LPG（Meteor Lake）和 RDNA 3.5（AMD Strix Point）。

## 摘要

Xe2 是 Xe-LPG 的演进版，核心变化在于将两个 8-wide Vector Engine 合并为一个 16-wide Vector Engine，减少指令控制开销并简化分支发散行为。每个 Xe Core 的 XMX 矩阵加速单元（Lunar Lake 重新引入，Meteor Lake iGPU 缺席）为 2048-bit，支持 INT2 以上精度。L2 缓存从 Meteor Lake 的 4 MB 翻倍至 8 MB，层级 Z 缓存增加 50%（4→6 KB），颜色缓存增加 33%。光追单元每 Xe Core 增至 3 条遍历管线（box tests：18/cycle），较前代提升约 50%。性能方面，Lunar Lake iGPU 在 Cyberpunk 2077 中显著领先 Meteor Lake，接近 AMD Phoenix（上代），但仍落后 AMD Strix Point RDNA 3.5。AMD 在 L1/L2 带宽和 FP32 吞吐上具有明显优势，但更耗内存带宽（功耗代价）；Intel 靠大缓存降低 DRAM 访问，效率导向策略鲜明。

## 关键要点

- Vector Engine 合并：8-wide×2 → 16-wide×1，每 Xe Core FP32 吞吐不变，但分支发散惩罚更简单直观
- XMX 矩阵单元回归（INT2 起支持），AMD 仅有 WMMA（最低 INT4），无专用矩阵硬件
- L2 扩至 8 MB（最大 laptop iGPU L2），但延迟高于 Meteor Lake；AMD L2 更小但延迟更低
- Lunar Lake GPU DRAM 延迟 >400 ns，Strix Point <250 ns，差距显著
- Cyberpunk 1080p 低画质 Lunar Lake 帧率领先 Meteor Lake 约 50%，但仍落后 Strix Point
- Xe2 同时用于 Lunar Lake iGPU 和即将到来的 Battlemage 独显，架构跨产品线统一

## 链接到的概念

- [[rendering/xe2-igpu-architecture]]
- [[rendering/xe-hpg-architecture]]
- [[rendering/rdna35-architecture]]
- [[computer-systems/meteor-lake-chiplet-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/lunar-lakes-igpu-debut-of-intels
- 本地：`raw/articles/chipsandcheese.com/2024-10-08_lunar-lakes-igpu-debut-of-intels-xe2-architecture.md`
