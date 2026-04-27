---
tags: [cpu, startup, vliw, architecture-analysis, server]
date: 2026-04-27
sources: 1
---

# Tachyum Prodigy 架构分析

Tachyum 是 2017 年成立的芯片初创公司，其 Prodigy "万能处理器" 声称在同一芯片上兼顾 CPU、GPU、AI 加速器三种角色，且性能超越 AMD EPYC、Intel Ponte Vecchio 和 NVIDIA H100。Chips and Cheese 于 2022 年对公开资料进行了深度技术审查，结论是：这些声明不可信。

## 架构特征

**VLIW 本质**：Prodigy 表面上被称为"4-wide OoO"，但其 CEO 明确表示架构基于 VLIW 原则，由编译器负责调度。4 束（bundle）× 2 微操作/束 = 最多 8 微操作/周期，但实际有效吞吐很可能远低于此。VLIW 在 DSP 等固定负载场景有效，在通用高性能计算中已被 Itanium 的失败彻底证伪。

**分支预测器落后一代**：采用 12-bit 全局历史的 skewed-Gshare 预测器——这是 2000 年代初期 Pentium 4 和 Athlon 64 用过的技术。现代竞品使用 TAGE 或感知器预测器，以相同存储预算取得更高精度。BTB 容量仅 1024 条目（Netburst 时代 4096 条目，Zen 3 更是数万条目），性能严重落后。

**缓存层级薄弱**：每核仅 64 KB L1D + 1 MB L2，以虚拟 L3（空闲核心贡献 L2 容量，类似 IBM Telum）替代独立 L3。对比 AMD Milan 的每核 4 MB L3，Prodigy 的缓存容量严重不足，难以喂饱其庞大的向量执行单元。

**向量执行单元夸张**：2022 版 Prodigy 拥有 2 × 1024-bit 向量 FMA，矩阵乘法单元达 2 × 2048-bit。单核向量算力极高，但对应的缓存带宽远不匹配，实际向量利用率存疑。

**计算带宽比严重失衡**：128 核 T16128 的 FP64 向量算力约 45 TFlops，DDR5 内存带宽约 921 GB/s，算存比超过 50:1。对比 AMD MI250X（~47 TFlops FP64，算存比约 15:1），Prodigy 的向量单元将长期处于带宽饥渴状态。

**功耗密度前所未有**：旗舰 SKU 标称 950W / 500mm²，热密度约 1.9 W/mm²，远超 NVIDIA H100 的 0.875 W/mm²，数据中心散热方案面临极大挑战。

## 软件生态缺失

Prodigy 运行 x86/ARM/RISC-V 二进制依赖 QEMU 模拟，导致单线程性能下降约 90%，多线程下降约 80%，SIMD 更是几乎完全失效。自有 ISA 与硬件执行单元高度绑定，未来换代（如从 2 FMA → 3 FMA）将导致软件二进制不兼容。软件生态从零开始，与 ARM 花费多年建立的生态相比毫无可比性。

## 时间线与执行力

- 2017 创立，预计 2020 量产 → 延期至 2021 → 延期至 2022 → 2022 年仅有 FPGA 仿真系统
- 从未完成流片，承诺"H1 2023 量产"对一家从未流片的初创公司极为乐观

## 总结

Prodigy 在纸面上将理想化指标最大化，但多个子系统相互掣肘：向量单元极宽但缓存喂不饱，功耗极高但散热难以实现，ISA 与硬件深度绑定但软件生态为零。技术路线的冒进程度与 NetBurst 的前车之鉴相似，区别在于 Intel 有资源和工程实力最终从 NetBurst 的教训中成长，而 Tachyum 面对的是 AMD MI300 和 NVIDIA Grace-Hopper 等成熟竞品。

## Sources

- [[sources/chipsandcheese-tachyum-claims]]
- [[sources/chipsandcheese-tachyum-revised]]
