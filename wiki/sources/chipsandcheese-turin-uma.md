---
tags: [source, hardware, amd, epyc, numa, memory, server]
date: 2026-04-27
sources: 1
---

# Evaluating Uniform Memory Access Mode on AMD's Turin（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 11 月的文章，在搭载双路 EPYC 9575F（Turin Zen 5）的 Verda 实例上测试 NPS0（Uniform Memory Access）模式的实际代价与收益。

## 摘要

NPS0 是 AMD 服务器 NUMA 的特殊模式，将双路系统对软件呈现为单一统一内存体（类比桌面系统的扁平内存），目的是降低 NUMA-aware 编程的复杂度。测试系统运行双路 EPYC 9575F（各 64 核，Zen 5），共 24 个内存控制器全部参与均匀分发。

代价明显：DRAM 延迟超过 220 ns，比 NPS1 模式的 EPYC 9355P 高出近 90 ns——相较旧世代（Broadwell 双路 NPS0 仅多约 29 ns），现代 SoC 的 NPS0 延迟惩罚更重，原因在于更长的互联路径。带宽虽有提升，但延迟优势要到负载接近 400 GB/s 时才开始显现。

SPEC CPU2017 单线程跑分意外持平：9575F 更高的 5 GHz 主频能补偿延迟损失；但高 DRAM 访问率的子测试（502.gcc、505.mcf、520.omnetpp、549.fotonik3d）明显落后，缓存命中率高的子测试（548.exchange2、538.imagick）反而受益于频率。

结论：现代服务器 NPS0 不值得使用——延迟惩罚太高、带宽收益对 NUMA-unaware 代码微乎其微，且随核心和内存控制器数量增加将继续恶化。

## 关键要点

- NPS0：双路系统统一暴露为单一 NUMA 节点，均匀分发至 24 内存控制器
- DRAM 延迟 >220 ns，NPS0 vs NPS1 差约 90 ns（旧代 Broadwell 仅约 29 ns）
- 带宽提升需 ~400 GB/s 以上负载才能抵消延迟代价
- SPEC CPU2017 整体接近，但内存敏感型子测试显著受损
- 每 CCD 带宽（GMI-Wide）在不同 NPS 模式下几乎不变

## 链接到的概念

- [[numa-multi-socket-design]]
- [[zen5-epyc-server]]
- [[spec-cpu2017-methodology]]

## 原文

- 链接：https://chipsandcheese.com/p/evaluating-uniform-memory-access
- 本地：`raw/articles/chipsandcheese.com/2025-11-26_evaluating-uniform-memory-access-mode-on-amd-s-turin-ft-verd.md`
