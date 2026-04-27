---
tags: [source, gpu, amd, rdna3, cache, compute]
date: 2026-04-27
sources: 1
---

# AMD's RX 7600: Small RDNA 3 Appears（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 6 月的文章，深入分析 AMD Navi 33（RX 7600）——RDNA 3 的低端单片设计与高端 chiplet 方案（Navi 31）的架构差异。

## 摘要

RX 7600 使用 Navi 33，一颗完全单片的 RDNA 3 GPU，制程为 TSMC 6nm（而非高端的 5nm），拥有 16 个 WGP、2 MB L2、32 MB Infinity Cache 与 128-bit 总线（288 GB/s）。与 Navi 31 的 chiplet 方案不同，Navi 33 省去了独立的内存控制器 die，节省了复杂度与成本。文章详细测量了 L0/L1/L2/Infinity Cache 的延迟和带宽，发现 Navi 33 相比 Navi 31 享有更低的 Infinity Cache 延迟（约低 58%），而该延迟优势部分补偿了其较小寄存器文件（128 KB/SIMD，而非 192 KB）带来的占用率损失。文章还修订了早先对 VOPD 双发射的误判：编译器寄存器分配对 VOPD 生效率影响很大，wave64 模式或手工汇编才能稳定触发双发射。

## 关键要点

- Navi 33 是单片设计，使用 TSMC 6nm（非 5nm），优先控制成本而非追求极限性能
- 小寄存器文件（128 KB/SIMD 对比 Navi 31 的 192 KB）降低 wave 占用率，尤其影响寄存器密集的 RT 着色器
- Navi 33 的 Infinity Cache 延迟比 Navi 31 低 ~58%，弥补了 chiplet 方案的延迟代价
- VOPD 双发射依赖编译器寄存器分配质量；wave64 模式或使用立即数输入可提高触发率
- RX 7600 VRAM 带宽（288 GB/s）远逊于 RTX 3060 Ti（256-bit 总线）
- 前端时钟策略与高端 RDNA 3 相反：Navi 33 前端频率略低于 shader 阵列，高端卡则相反

## 链接到的概念

- [[rendering/rdna3-architecture]]
- [[rendering/mcm-gpu-design]]
- [[computer-systems/gpu-memory-hierarchy-latency]]
- [[computer-systems/gcn-wave-occupancy]]
- [[computer-systems/op-cache-decoded-uop-cache]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-rx-7600-small-rdna-3-appears
- 本地：`raw/articles/chipsandcheese.com/2023-06-04_amds-rx-7600-small-rdna-3-appears.md`
