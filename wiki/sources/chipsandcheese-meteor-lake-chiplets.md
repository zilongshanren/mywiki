---
tags: [source, chipsandcheese, intel, chiplet, packaging, cpu]
date: 2026-04-27
sources: 1
---

# Hot Chips 34 – Intel's Meteor Lake Chiplets, Compared to AMD's（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 9 月的文章，分析 Intel 在 HC34 发布的 Meteor Lake chiplet 架构，与 AMD 的 chiplet 策略进行横向比较。

## 摘要

文章从 Intel 客户端产品线演化切入：过去十年 Intel 靠不同单片 die 覆盖不同 SKU，随着核心数增加、异构混合架构普及、SoC 功能膨胀，单片策略的成本已不可持续，Meteor Lake 因此拆分为四个 tile（CPU/iGPU/SoC/IO Extender）堆叠于被动 base die。与 AMD 的 IFOP 方案相比，Intel 的 Foveros Die Interconnect（FDI）牺牲了平面封装的低成本，换来更高 IO 密度和更低 die-to-die 功耗，使 chiplet 策略向移动市场延伸成为可能。文章还深入分析了 iGPU 从 IDI 协议切换为 iCXL 的含义，判断 Meteor Lake 的 iGPU 不再与 CPU L3 共享——这是 Sandy Bridge 以来的首次，动机包括减少环总线 stop 数量、改善低功耗状态管理、以及 iGPU 对共享 L3 本身命中率极低。

## 关键要点

- Meteor Lake 为 Intel 首个面向客户端的 chiplet 设计，四 tile 结构
- FDI（Foveros Die Interconnect）延迟约 <10 ns，与 AMD IFOP 接近，但功耗和密度更优
- iGPU 改用 iCXL 协议，不再通过 IDI 挂载到 CPU L3 ring bus
- iGPU 私有缓存持续扩大，L3 共享的必要性降低
- AMD 同期也在将 chiplet 架构向低功耗移动端延伸（Dragon Range、Phoenix Point）

## 链接到的概念

- [[meteor-lake-chiplet-architecture]]
- [[intel-hybrid-alder-lake]]
- [[golden-cove-microarchitecture]]
- [[mcm-gpu-design]]

## 原文

- 链接：https://chipsandcheese.com/p/hot-chips-34-intels-meteor-lake-chiplets-compared-to-amds
- 本地：`raw/articles/chipsandcheese.com/2022-09-10_hot-chips-34-intels-meteor-lake-chiplets-compared-to-amds.md`
