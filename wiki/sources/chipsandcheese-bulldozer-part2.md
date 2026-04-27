---
tags: [source, computer-systems, cpu, amd, bulldozer, microarchitecture, cache, memory, 32nm]
date: 2026-04-27
sources: 1
---

# Bulldozer, AMD's Crash Modernization: Caching and Conclusion（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 1 月的文章，深度分析 AMD Bulldozer 的缓存子系统并给出综合结论。

## 摘要

Bulldozer 的缓存体系是其最薄弱的环节之一。L1D 从 K10 的 64 KB 削减到仅 16 KB（为兼顾 32nm 工艺时序目标），且改为 write-through 设计（与 Netburst 的惨痛历史相似）。AMD 引入了 4 KB 写合并缓存（WCC）来部分缓解写带宽问题，但效果有限。L2 扩大到 2 MB 且带宽翻倍，是架构中少有的亮点。然而 L3 继承了 K10 的 Northbridge 中心化架构，未引入 Sandy Bridge 的 ring bus，导致 L3 延迟高达 18 ns 以上，L3 带宽极差，更因 victim cache 操作使实际 L3 流量翻倍。综合来看，Bulldozer 的失败并非单一原因，而是工艺节点挑战、过于激进的设计目标、以及 Sandy Bridge 异常强大这三者叠加的结果。文章指出 Bulldozer 在技术上为后来的 Zen 铺路，如同 Netburst 为 Sandy Bridge 铺路。

## 关键要点

- L1D：16 KB write-through + 4 KB WCC，延迟 4 周期，L1D miss rate 超 K10 两倍以上
- L2：2 MB 16-way，延迟 20 周期，带宽大幅提升是架构亮点，可分别向两线程提供独立 16 B/cycle 路径
- L3：8 MB 64-way，延迟 >18 ns（比 Sandy Bridge 的 ring-based L3 差得多），带宽 ~35 GB/s 但实际 L3 需承受双倍流量（victim cache 写回）
- Northbridge 瓶颈：维持 K10 中心化设计，2.2 GHz 时钟限制，超频到 2.4 GHz 才能勉强改善 L3 延迟
- L2 TLB 外置于 "cache unit"，命中需 20 周期（Sandy Bridge 7 周期，K10 仅 2-3 周期）
- 32nm SOI 工艺挑战：被迫切换 8T SRAM、削减 bitline、复制整数寄存器文件——均是工艺补偿措施
- 历史定位：Bulldozer 是 AMD 的"必要阵痛"，许多技术（PRF、FMA、先进分支预测器）后来在 Zen 中成功复活

## 链接到的概念

- [[computer-systems/bulldozer-microarchitecture]]
- [[computer-systems/netburst-microarchitecture]]
- [[computer-systems/electromigration-voltage-degradation]]

## 原文

- 链接：https://chipsandcheese.com/p/bulldozer-amds-crash-modernization-caching-and-conclusion
- 本地：`raw/articles/chipsandcheese.com/2023-01-24_bulldozer-amds-crash-modernization-caching-and-conclusion.md`
