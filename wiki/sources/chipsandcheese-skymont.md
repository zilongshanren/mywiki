---
tags: [source, computer-systems, intel, atom, e-core, skymont, lunar-lake]
date: 2026-04-27
sources: 1
---

# Intel Skymont 详解（Chester Lam & George Cozma / Chips and Cheese）

[[people/chester-lam]] 与 [[people/george-cozma]] 联合发表于 2024 年 6 月，基于 Intel 公开高清幻灯片与演讲音频对 Skymont E-Core 架构做全面解析。

## 摘要

Skymont 是 Lunar Lake 的 E-Core 架构，是 [[crestmont-microarchitecture|Crestmont]] 的继任者，也是 Intel Atom 系列迄今最激进的一次升级。前端由双簇扩展为三簇（各 3-wide），总解码吞吐升至 9 uop/cycle，微操作队列总容量 96 条目。后端全面扩容：ROB 从 256 升至 416，退役宽度达 16 uop/cycle（是入队 8 uop/cycle 的两倍），执行端口达 26 个。向量执行从 Crestmont 的弱向量跨越至 4×128-bit，FMA 延迟从 6 cycle 降至 4 cycle，并新增反常数（subnormal）快速路径。Skymont 新增"Nanocode"机制：将 gather 等高频微码指令本地化到每个解码簇，允许三簇并行处理不同的微码序列。L2 带宽翻倍（128 B/cycle），L2 TLB 扩至 4K 条目（超过 Redwood Cove 和 Zen 4）。Intel 声称 Skymont 性能/时钟接近 Redwood Cove P-Core。

## 关键要点

- 三簇解码（3×3-wide），扫描 96 B/cycle，总 uop 队列 96 条目
- "Nanocode"让各解码簇可并行处理高频微码指令（首例于 x86 Atom）
- 后端：ROB 416，26 个执行端口，退役 16 uop/cycle
- 向量：4×128-bit FP/INT，FMA 4 cycle（Crestmont 为 6 cycle）
- subnormal 添加快速路径（Crestmont 用微码，超过 280 cycle）
- L2 TLB 4K 条目，超过 P-Core；L2 带宽 128 B/cycle（Crestmont 64 B/cycle）
- 簇内缓存一致性不再依赖片外 fabric，改为 L2 直接处理核间转发
- 与 Arm Cortex X2 性能/时钟相当，但 Skymont 定位低功耗岛而非旗舰核

## 链接到的概念

- [[skymont-microarchitecture]]
- [[crestmont-microarchitecture]]
- [[clustered-decode-atom]]
- [[gracemont-microarchitecture]]
- [[golden-cove-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/intel-details-skymont
- 本地：`raw/articles/chipsandcheese.com/2024-06-15_intel-details-skymont.md`
