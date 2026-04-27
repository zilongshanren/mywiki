---
tags: [source, rendering, nvidia, gpu, kepler, 28nm, compute]
date: 2026-04-27
sources: 1
---

# Inside Kepler, Nvidia's Strong Start on 28 nm（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2023 年 11 月的文章，对 Nvidia Kepler 架构（GK104 / GK210）做微架构深度解析，以 GTX 680 和 Tesla K80 为测试主体，与 AMD GCN（HD 7950、R9 390）及 Fermi 对比。

## 摘要

Kepler 是 Nvidia 2012 年的 28 nm 首发架构，核心策略：放弃 Fermi 的热时钟（2× 频率执行单元），改为更多执行单元 + 正常时钟，换取功耗效率；同时将调度从硬件记分板移交给编译器静态控制码（每 7 条指令前置一个 64-bit 控制字，包含停顿周期和 dual issue 标志）。SMX 由 4 个调度分区（SMSP）组成，每分区跟踪至多 16 个 warp。纹理缓存实为每 SMSP 12 KB（SMX 合计 48 KB），作者通过多 warp 实验纠正了 Nvidia 白皮书的混淆表述。Kepler 的本地内存延迟和 global atomic 延迟优于 Fermi 和 GCN，但 L2 带宽与 DRAM 带宽均不及 GCN。静态调度方案被 Maxwell 以后所有 Nvidia 架构沿用。

## 关键要点

- 静态调度：编译器控制码消除硬件记分板，降低功耗
- SMX = 4 SMSP，每 SMSP 最多 16 warp，每 cycle dual issue
- FMA 延迟 9 cycle，整数 2/3 FP32 速率，SFU 1/4 整数速率
- 纹理缓存：每 SMSP 12 KB（共 48 KB），而非 Nvidia 文档宣称的"每 SMX 48 KB"单层
- L1/共享内存：64 KB 动态划分（GK210 为 128 KB）；常量缓存从 Fermi 的 4 KB 缩至 2 KB
- GCN 的 L2 带宽与 DRAM 带宽均超越 Kepler（更宽的内存总线）
- 遗产：GK210 Tesla K20x 系列赢得超算（Oak Ridge Titan）；Kepler–Maxwell–Pascal 年代提供了好的用户升级体验

## 链接到的概念

- [[rendering/kepler-architecture]]
- [[rendering/gcn-wave-occupancy]]
- [[rendering/rdna3-architecture]]
- [[computer-systems/gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-kepler-nvidias-strong-start-on-28-nm
- 本地：`raw/articles/chipsandcheese.com/2023-11-24_inside-kepler-nvidias-strong-start-on-28-nm.md`
