---
tags: [source, computer-systems, risc-v, t-head, alibaba, c910, xuantie, microarchitecture, out-of-order]
date: 2026-04-27
sources: 1
---

# Alibaba/T-HEAD's Xuantie C910（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 2 月的文章，对运行在 LicheePi 4A 单板机（TH1520 SoC）上的玄铁 C910 进行完整微架构剖析，并参考部分已开源的 RTL 代码。

## 摘要

C910 是阿里巴巴 T-HEAD 的第一款乱序 RISC-V 核心，3-wide、12 级流水线，工作在 1.85 GHz（TSMC 12nm）。文章从前端（64 KB L1i、bi-mode 分支预测器、16 entry 循环缓冲区）、乱序后端（192 entry ROB、但寄存器文件和调度器配置严重不足）、内存子系统（60 周期 L2 延迟、仅约 4.2 GB/s DRAM 带宽）到 CPU-GPU 延迟等方面逐一剖析。结论是 C910 在若干方面（非对齐访问处理、向量扩展 RVV 0.7.1 支持、核间延迟）优于同期 SiFive P550，但在最关键的"基本功"上失分严重：L2 既慢又小、DRAM 带宽极低，导致这个拥有 192 条目 ROB 的核心在实际工作负载中无法将乱序窗口填满，整体性能常被 P550 甚至同频的 Cortex A55 追平。

## 关键要点

- 3-wide OoO，12 级流水线，192 entry ROB，但整数调度器仅 16 项（P550 为 40 项）
- 64 KB L1i（2-way FIFO），预解码元数据缓存分支信息；16 entry 循环缓冲作为最小 trace cache
- bi-mode 分支预测器：1024 entry selection table + 2×16384 entry history table（约 17.3 KB）；同频对比 P550 更强
- L2 缓存延迟 60 周期，多核共享读带宽约 12.6 GB/s（4 核合计），极低
- DRAM 带宽约 4.2 GB/s（LPDDR4X-3733 实测），延迟 133.9 ns，尚可但带宽严重受限
- 向量扩展 RVV 0.7.1，双 FP 管线支持 128-bit 向量操作；T-HEAD 后续 C920 升至 RVV 1.0
- 核间传输延迟远优于 P550（P550 四核集群内延迟超 300 ns，C910 明显更好）
- 非对齐访问有硬件支持，性能代价极低（不超 16B/8B 对齐边界时几乎无惩罚）

## 链接到的概念

- [[computer-systems/xuantie-c910-microarchitecture]]
- [[computer-systems/sifive-p550-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/alibabat-heads-xuantie-c910
- 本地：`raw/articles/chipsandcheese.com/2025-02-04_alibaba-t-head-s-xuantie-c910.md`
