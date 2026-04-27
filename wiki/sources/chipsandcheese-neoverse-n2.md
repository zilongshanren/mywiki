---
tags: [source, cpu, arm, neoverse, server, microarchitecture]
date: 2026-04-27
sources: 1
---

# ARM's Neoverse N2: Cortex A710 for Servers（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 8 月的文章，基于 Alibaba Yitian 710 云实例对 Neoverse N2 进行微基准测试，并与 [[computer-systems/zen4-microarchitecture|Zen 4]] 及前代 [[computer-systems/neoverse-n1-microarchitecture|Neoverse N1]] 详细对比。

## 摘要

Neoverse N2 是 ARM 服务器核系列的第二代，继承自 [[computer-systems/cortex-a710-microarchitecture|Cortex-A710]] 移动核，通过更大缓存、更宽 TLB、48 位物理地址等改动适配服务器场景。N2 是 5-wide OOO 核，ROB 仅 160 条目（Zen 4 为 320），但调度器容量可观，整数侧竞争力尚可。N2 与 Zen 4 均于同年引入新向量扩展（SVE 与 AVX-512），但 ARM 的向量执行单元宽度未变，仍是两条 128-bit 管道，与 Zen 4 的 256-bit 路径有差距。在互联层面，ARM 的 CMN-700 mesh 导致 L3 延迟高达 35ns，与 Intel Xeon 相近但明显差于 AMD 的环形总线方案（Zen 3 约 15ns）。作者指出 N2 进步在正确方向但幅度保守，面对 Ampere Siryn 192 核、AMD Bergamo 128 核等挑战，ARM 须加快步伐。

## 关键要点

- N2 ROB 仅 160 条目，但调度器容量接近 Zen 4，整数吞吐匹配度尚可
- 64 KB L1 cache 是优势；L2 仍 1 MB / 13-14 周期，三年来未变
- CMN-700 mesh 互联导致 L3 延迟约 35ns，接近 Intel 但差于 AMD 环形总线
- TLB 覆盖面弱于 x86 竞争对手，L2 DTLB 仅 1280 条目 vs Zen 4 的 3072
- 向量/FP 侧依旧落后，执行端口布局与 N1 相同，只增加调度器容量
- DRAM 延迟 141ns，劣于同代 Sapphire Rapids（110ns），DDR5 迁移代价高

## 链接到的概念

- [[computer-systems/neoverse-n1-microarchitecture]]
- [[computer-systems/cortex-a710-microarchitecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/neoverse-n2-microarchitecture]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]
- [[computer-systems/numa-multi-socket-design]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-neoverse-n2-cortex-a710-for-servers
- 本地：`raw/articles/chipsandcheese.com/2023-08-18_arms-neoverse-n2-cortex-a710-for-servers.md`
