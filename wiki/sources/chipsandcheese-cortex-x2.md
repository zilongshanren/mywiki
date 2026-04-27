---
tags: [source, computer-systems, arm, cpu, mobile, out-of-order]
date: 2026-04-27
sources: 1
---

# Cortex X2: Arm Aims High（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2023 年 10 月的文章，对 Cortex X2 做系统性微架构测评，测试平台为高通 Snapdragon 8+ Gen 1。

## 摘要

Cortex X2 是 A710 的放大版，Arm Cortex-X 系列第二代旗舰核。文章从分支预测、前端、OoO 引擎、FP/向量执行、内存子系统和带宽四个维度与 AMD Zen 4 及 Apple M1 做横向比较。核心结论：X2 的 ROB（288 条目）、四管道 FPU、2048 条目 L2 TLB 是相较 A710 的主要改进；整数调度容量与 Zen 4 接近；FP in-flight 能力不及 Zen 4；store forwarding 机制停留在"前 2010 年代"水平（仅支持有限的部分重叠转发）。Snapdragon 8+ Gen 1 的 6 MB L3 延迟偏高（~18 ns），DRAM 延迟 202 ns，这些平台瓶颈掩盖了 X2 核心架构的真实潜力。

## 关键要点

- 微操作缓存 3072 条目（大于 Intel Sunny Cove），5 宽解码，6 宽重命名
- 四管道 FPU：128-bit × 4，理论 FP32 吞吐与 Zen 4 的 256-bit × 2 相当
- Store forwarding 快路径 5 cycle，慢路径 10–11 cycle；Zen 4 慢路径更慢（19–20 cycle）
- 写流式（write streaming）模式：绕过 cache fill，L3 写带宽达 67 GB/s，DRAM 写带宽 41.2 GB/s
- 实际时钟 2.8 GHz（标称 3.187 GHz），55 ms 后达到该频率

## 链接到的概念

- [[computer-systems/cortex-x2-microarchitecture]]
- [[computer-systems/cortex-a710-microarchitecture]]
- [[computer-systems/neoverse-n2-microarchitecture]]
- [[computer-systems/non-scheduling-queue]]

## 原文

- 链接：https://chipsandcheese.com/p/cortex-x2-arm-aims-high
- 本地：`raw/articles/chipsandcheese.com/2023-10-27_cortex-x2-arm-aims-high.md`
