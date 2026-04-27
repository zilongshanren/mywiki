---
tags: [source, chipsandcheese, cpu, amd, zen5, strix-point, mobile, microarchitecture]
date: 2026-04-27
sources: 1
---

# AMD's Strix Point: Zen 5 Hits Mobile（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，以 Ryzen AI 9 HX 370 为测试对象，深度剖析 Zen 5 在 Strix Point 移动 APU 上的微架构实现。

## 摘要

本文是 Chester Lam 对 Zen 5 移动版首篇全面微架构分析，从系统级、前端、后端、缓存、内存一路拆解。Strix Point 以 12 颗 Zen 5 核（4P+8E）配合 RDNA 3.5 iGPU 和 LPDDR5-7500，率先在移动端推出 Zen 5，打破惯例。文章揭示了 Zen 5 引入的集群化 Fetch-Decode（仅对 SMT 有效而非单线程加速）、8-wide 重命名、BTB 受害者缓存、更大 TLB 等关键架构新特性，并指出跨集群 core-to-core 延迟异常偏高、向量寄存器堆混合宽度设计的取舍，以及桌面 Zen 4 配合 DDR5 在部分测试中仍胜过移动 Zen 5 的现象。

## 关键要点

- Zen 5 BTB 引入受害者缓存机制，16K 项 L1 BTB 被驱逐目标写入 L2 BTB，净追踪约 24K 目标
- 双路集群 Decode：每集群 4-wide，仅能各服务一个 SMT 线程；单线程无法合并两集群带宽
- 8-wide 重命名（比 Zen 4 的 6-wide 宽 33%），ROB、FP 寄存器堆趋近 Golden Cove 规模
- L1D 从 32 KB 增至 48 KB，延迟保持 4 周期；存储带宽提升至 64 bytes/cycle
- Strix Point 跨集群延迟约 200 ns（高于服务器预期，单芯片设计下令人意外）
- 内存延迟约 128 ns（LPDDR5），优于 Meteor Lake 的 148 ns；但远逊于 DDR5 桌面

## 链接到的概念

- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/strix-point-soc]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/meteor-lake-chiplet-architecture]]
- [[people/chester-lam]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-strix-point-zen-5-hits-mobile
- 本地：`raw/articles/chipsandcheese.com/2024-08-10_amds-strix-point-zen-5-hits-mobile.md`
