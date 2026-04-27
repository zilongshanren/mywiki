---
tags: [source, rendering, nvidia, gpu, maxwell, kepler, 28nm, compute, gaming, gcn]
date: 2026-04-27
sources: 1
---

# Maxwell: Nvidia's Silver 28nm Hammer（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 1 月的文章，对 Nvidia Maxwell 架构（GM204 / GM200）做全面微架构分析，以 GTX 980 Ti 为主要测试对象，与 Kepler（GK104 / GK210 / Tesla K80）及 AMD GCN（R9 390 / Fury X）做详细对比。

## 摘要

Maxwell 的核心策略是在 28 nm 工艺不变的前提下提升性能效率：删除 Kepler 中利用率低的执行资源（高比例 FP64、共享 FP32 单元、64-bit 宽 Shared Memory bank），换取每颗 die 上容纳更多 SM，并拉高时钟频率。GM204 对标 GK104，SM 数量从 8 增至 16，FP32 通道从 1536 增至 2048。旗舰 GM200（GTX 980 Ti）的计算性能在非 FP64 场景远超 GK110（GTX 780 Ti）和 AMD R9 390。Shared Memory 扩至 96 KB 且不再兼任 L1 缓存，新增原生整数原子 ALU 大幅降低共享内存原子延迟。静态调度控制码升级为 21-bit/指令（Kepler 为 8-bit），引入精细粒度 barrier 和编译器管理寄存器重用缓存。L2 容量翻倍（GM200 达 3 MB），配合基于瓦片的光栅化减少对 VRAM 带宽的依赖。代价是彻底放弃高性能 FP64，数据中心 Maxwell 产品直到 Pascal P100 才获接替。

## 关键要点

- 删除 Kepler 的 shared FP32 单元和可配置 FP64，SM 面积降低，SM 数量增加
- Shared Memory：96 KB 专用（不兼 L1），新增 CAS 原子 ALU，延迟超越 AMD GCN
- 静态调度控制码密度从每 7 条增至每 3 条一个控制字，引入细粒度 barrier 和寄存器重用缓存
- L2 容量 GM200 达 3 MB（GK210 的 2 倍），低延迟优于 GCN；带宽实测利用率低于 AMD
- VRAM 带宽与 Kepler 相近，通过瓦片光栅化降低带宽依赖，使 GTX 980 Ti 与 R9 390 竞争
- FP64 全线降至 1:32 比率，Maxwell 数据中心产品（Tesla M60）失去 HPC 竞争力
- Pascal 直接继承 Maxwell 微架构，Steam 2023 年硬件调查 Pascal 仍在前十

## 链接到的概念

- [[rendering/maxwell-architecture]]
- [[rendering/kepler-architecture]]
- [[computer-systems/gcn-wave-occupancy]]
- [[computer-systems/gcn-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/maxwell-nvidias-silver-28nm-hammer
- 本地：`raw/articles/chipsandcheese.com/2024-01-08_maxwell-nvidias-silver-28nm-hammer.md`
