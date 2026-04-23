---
tags: [source, chipsandcheese, cpu, 微架构, zen3, 后端瓶颈]
date: 2026-04-19
sources: 1
---

# Measuring Zen 3's Bottlenecks（George Cozma / Chips and Cheese）

[[george-cozma]] 2021 年 7 月发表于 [[chips-and-cheese]] 的文章，用 PMU 在 Cinebench R23、Civ VI（DX11/DX12）、3DMark Timespy、War Thunder、EU4、Linpack 六档 workload 上系统量化 Zen 3 派发停顿的来源。方法是抓 rename/allocate 两侧——"Op Queue Empty"（前端供不上）与 "Dispatch Stall"（后端吃不下）——再对后端细分每个资源池。结论进入本 wiki 的 [[dispatch-stall-breakdown]]。

## 摘要

六类 workload 都是后端绑定为主，但 War Thunder / EU4 的前端停顿也达 14–16%。后端池子里 ROB 满是最常见停顿因（8–20% 时间），这是健康信号——说明 AMD 把其它结构尺寸调到不会率先饱和。LDQ/STQ 各 2–5%，FP 寄存器文件仅在 Linpack 上突出（FP 高密度），FP 调度器 / FP flush recovery 几乎可忽略。EU4 是唯一一档 INT 调度器/寄存器文件也显著的负载。Taken Branch Buffer（推测用于 BPU 全局历史 checkpoint）最高 1.57%。分支预测 Zen 3 精度最差 97.29%（War Thunder），但作者强调误预测的真实代价被低估，因为一次误预测还会占用后端资源。解码器带宽不是问题——4 路解码，实测从未超 2 IPC。最后作者推断 Zen 4 大概率会继续做 BPU 精度、扩大 ROB/LDQ/STQ，并放大 L1/L2 缓存——这些推断在同年 8 月的 [[chipsandcheese-gigabyte-zen4-leak|Gigabyte 泄露]]中部分落地（L2 翻倍到 1 MB，L2 DTLB 扩到 3072）。

## 关键要点

- 所有 workload 都后端绑定为主；War Thunder / EU4 前端停顿 14.75–16.12%
- ROB 满停顿 8–20%，最常见；LDQ/STQ 各 2–5%
- Linpack 唯一 FP 寄存器文件停顿突出；EU4 唯一 INT 侧突出
- 分支预测 Zen 3 最差 97.29%，但误预测真实代价被图表低估
- 解码器带宽非瓶颈：4 路解码 vs 实测 ≤2 IPC
- L3 miss 少但游戏仍在意 → 铺垫 V-Cache 的意义
- 作者对 Zen 4 的三条预测：更好 BPU / 更大后端队列 / 更大 L1-L2

## 链接到的概念

- [[dispatch-stall-breakdown]]
- [[branch-predictor-design]]
- [[op-cache-decoded-uop-cache]]
- [[cpu-scheduler-design]]

## 原文

- 链接：https://chipsandcheese.com/p/measuring-zen-3s-bottlenecks
- 本地：`raw/articles/chipsandcheese.com/2021-07-23_measuring-zen-3s-bottlenecks.md`
