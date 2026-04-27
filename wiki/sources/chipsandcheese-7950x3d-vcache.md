---
tags: [source, cpu, amd, zen4, vcache, 3d堆叠, 缓存]
date: 2026-04-27
sources: 1
---

# AMD's 7950X3D: Zen 4 Gets VCache（Chips and Cheese）

[[people/chester-lam|Chester Lam]] 于 2023 年 4 月发表的文章，分析 AMD Ryzen 9 7950X3D 上 Zen 4 配合 3D V-Cache 的效果，通过性能计数器量化 VCache 在不同游戏和工作负载下的 L3 命中率与 IPC 收益。

## 摘要

7950X3D 双 CCD 设计中仅一枚搭载 VCache（96 MB L3），另一枚维持标准 32 MB，提供了难得的对照实验机会。VCache CCD 时钟频率约低 7%（~5.2 GHz vs ~5.5 GHz+）。文章通过关闭 Boost 锁定 4.2 GHz 隔离频率变量，测量 L3 命中率与 IPC 差异。结果显示：VCache 在高 L3 miss 率的场景（COD Black Ops Cold War +47% 命中率、+19% IPC；7-Zip +29% 命中率、+9.75% IPC）收益显著，但在低 miss 率场景（DCS）可能因 L3 延迟微增（4 cycle）而略亏。文章还将 VCache 与 Intel 的 EDRAM L4（Haswell/Skylake）对比，说明 TSV 堆叠 SRAM 相对 EDRAM 在延迟和带宽上的全面优势。

## 关键要点

- VCache 将 L3 从 32 MB 扩展到 96 MB，通过 TSV 堆叠 die 实现
- VCache 额外增加约 4 cycle 的 L3 延迟（约 1.6 ns），绑定到时钟差距后实际感知不大
- L3 带宽差异仅来自时钟差异，VCache 本身不改变带宽架构
- EDRAM L4（Broadwell/Skylake）延迟 >30 ns、带宽仅 50 GB/s，远不如 VCache
- AMD 默认调度策略将普通应用置于高频 CCD，VCache 需手动绑定 affinity 才能生效
- Zen 4 较大的 L2（1 MB）有助于缓冲 VCache 的少量延迟惩罚

## 链接到的概念

- [[computer-systems/vcache-3d-die-stacking]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]
- [[computer-systems/memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-7950x3d-zen-4-gets-vcache
- 本地：`raw/articles/chipsandcheese.com/2023-04-23_amds-7950x3d-zen-4-gets-vcache.md`
