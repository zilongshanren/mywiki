---
tags: [source, cpu, intel, broadwell, edram, cache, vcache, history]
date: 2026-04-27
sources: 1
---

# Broadwell's eDRAM: VCache before VCache was Cool（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 11 月的历史技术深挖，通过实测还原 Broadwell Crystal Well eDRAM L4 缓存的性能特性，并将其与 AMD V-Cache 进行横向对比。

## 摘要

Broadwell 桌面版（2015 年）搭载独立的 77 mm² Crystal Well eDRAM die（22 nm），提供 128 MB 的 L4 缓存——比 AMD Ryzen 7 5800X3D（2022 年）早了近七年。Crystal Well 通过 OPIO 接口（独立读/写 64-bit 总线）连接 CPU die，理论带宽等效 DDR-3200，最大约 50 GB/s，延迟约 36.6 ns（140 cycle @ 3.8 GHz）。相比主内存 DRAM，Crystal Well 采用 128-bank 设计、6 array cycle 的极短 bank 恢复时间、独立读写总线，避免 DDR 的 bus turnaround 开销，在高负载下延迟稳定性远优于主内存。然而带宽上限低（单 OPIO 接口无法随核数扩展）、延迟对 CPU 来说偏高，决定了其仅适合作 L4 而非 L3。文章还探讨了 Skylake 改版将 eDRAM 控制器移至 System Agent 后的延迟退化，以及随着 DDR4/DDR5 带宽持续提升，eDRAM 的优势如何逐渐消失。

## 关键要点

- Crystal Well：22 nm，128 MB eDRAM，OPIO 接口带宽约 50 GB/s，延迟 ~140 cycle
- 128 bank + 独立读写总线 + 6-cycle bank 恢复，eDRAM 高负载延迟稳定性优于主内存
- Broadwell 将 eDRAM tag 嵌入 L3 切片（L3 因此从 8 MB 缩至 6 MB），tag 与 L3 并行检查，L4 命中不经过 ring bus
- Skylake 变体将 eDRAM 移至 System Agent：延迟大幅劣化，L4 命中需等 L3 miss 后串行检查 tag
- SPEC CPU2017 中仅少数工作负载（如 520.omnetpp）能利用 eDRAM 命中率优势战胜 Skylake
- 与 AMD V-Cache 对比：eDRAM 延迟 30+ ns vs TSV SRAM 约 1.6 ns 额外延迟，差距巨大

## 链接到的概念

- [[computer-systems/broadwell-edram-l4]]
- [[computer-systems/vcache-3d-die-stacking]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/broadwells-edram-vcache-before-vcache
- 本地：`raw/articles/chipsandcheese.com/2024-11-01_broadwells-edram-vcache-before-vcache-was-cool.md`
