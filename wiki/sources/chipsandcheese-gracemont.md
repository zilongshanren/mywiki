---
tags: [source, cpu, intel, alder-lake, gracemont, e-core, atom, 微架构]
date: 2026-04-19
sources: 1
---

# Gracemont: Revenge of the Atom Cores（Chester Lam / Chips and Cheese，2021-12-21）

[[chester-lam]] 对 Alder Lake E-Core 的深度拆解，与 Golden Cove 那篇配套看。

## 摘要

Gracemont 是 5-wide 乱序、reorder 深、近 4 GHz 的"中核"，绝不是 A55 式的背景核。前端无 uop cache，沿用 [[clustered-decode-atom|Tremont 双解码簇]] 方案，但新增自动集群切换解决长展开循环的退化问题；L1i 扩到 64 KB 补位。方向预测器几乎与 Golden Cove 同级，BTB 5K、zero-bubble 1024 条。后端 ROB 接近 Zen 3，但向量寄存器堆只 128-bit 宽、207 项共 3.3 KB（Golden Cove ≥10 KB）——256-bit AVX 拆两条 uop，在 libx264 里仍够用，仅 Y-Cruncher 类 >70% 256-bit write 会撑爆。整数侧 4 ALU + 分布式调度器。FP 用半统一 + 大 NSQ（[[non-scheduling-queue|非调度队列]]）撑起 91 条 FP/vec 容量。L1D 3 周期（比 Golden Cove 的 5 周期绝对时间还快），L2 四核共享 2 MB 17 周期；L3 借 Alder Lake 的 ring，但激活 E-Core 就让 ring 降频成 [[intel-hybrid-alder-lake|hybrid 首代毛病]]。RAPL 实测八核全开 libx264：Gracemont 5.72 W/core vs Golden Cove 21.05 W/core，IPC 1.72 vs 2.25——perf/W 明显优于 Golden Cove，这是 Intel 押 hybrid + hyperscale server 的经济根基。

## 关键要点

- 5-wide 乱序 + 双解码簇自动切换 + 64 KB L1i 补 uop cache 缺位
- 向量 RF 128-bit 宽以省面积，AVX 拆 2 uop；对大部分 workload 仍够用
- 分布式整数调度器 + 大 FP NSQ，借 AMD 思路降调度器功耗
- 移除 Atom 线的高延迟 vector integer multiplier，提升 128-bit 向量可用性
- 单核启动时 shared L2 + ring stop 吃很多电，需要多核分摊才能出效率
- 战略位置：hyperscale server、密度型云负载，对标 Neoverse N1 / Zen 4 Bergamo

## 链接到的概念

- [[gracemont-microarchitecture]]
- [[clustered-decode-atom]]
- [[non-scheduling-queue]]
- [[move-elimination-zeroing-idioms]]
- [[intel-hybrid-alder-lake]]
- [[tremont-microarchitecture]]
- [[littles-law-reorder-buffer]]
- [[neoverse-n1-microarchitecture]]

## 原文

- 链接：<https://chipsandcheese.com/p/gracemont-revenge-of-the-atom-cores>
- 本地：`raw/articles/chipsandcheese.com/2021-12-21_gracemont-revenge-of-the-atom-cores.md`
