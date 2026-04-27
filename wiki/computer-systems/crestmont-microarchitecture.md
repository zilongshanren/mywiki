---
tags: [cpu, 微架构, intel, atom, e-core, crestmont, meteor-lake]
date: 2026-04-27
sources: 1
---

# Crestmont 微架构

Crestmont 是 Intel 为 Meteor Lake 设计的 E-Core 微架构，于 2023 年底随 Core Ultra 系列发布。它同时承担两个物理角色：主 CPU tile 上的主 E-Core，以及 SoC tile 上的低功耗 LPE-Core（Low Power E-Core）。Crestmont 继承自 [[gracemont-microarchitecture|Gracemont]]，是对后者的渐进式改进而非颠覆性重设计。

## 前端

Crestmont 沿用了 [[clustered-decode-atom|集簇解码]] 架构，双簇各可解码 3 uop/cycle，合计 6 uop/cycle。重命名器宽度升至 6 uop/cycle（Gracemont 为 5 uop/cycle），从而能充分利用前端吞吐。分支预测器 BTB 从 5120 扩至 6144 条目，预测器扫描宽度从 32 B/cycle 大幅提升至 128 B/cycle，支持更长的分支历史模式（最长模式相较 Gracemont 更长）。

## 后端与执行

后端结构基本与 Gracemont 相同：ROB 大小、寄存器堆、Load/Store 队列均未变化。浮点调度器条目小幅增加，FP 除法器延迟从约 10 cycle 降至 5 cycle。整数 SIMD 路径维持 128-bit 宽度，不支持 AVX-512。

## 内存子系统

L2 TLB 从 2048 条目扩至 3072（6-way 相联），L2 缓存仍为 2 MB 的簇共享设计，L3 缓存由 Meteor Lake ring bus 与 P-Core 共享（24 MB）。L3 带宽约 10–12 B/core/cycle，与 Gracemont 相比无明显改善。LPE-Core 版本不连接共享 L3，以 2 MB L2 作为 LLC，因此在工作集超出 L2 后性能急剧下降。

## LPE-Core 对比主 E-Core

两者使用相同 Crestmont 架构，但 LPE-Core 的频率上限仅约 2.5 GHz，且不在 ring bus 上，无法共享 L3。其内存延迟和带宽均显著更差，更适合轻量后台任务而非计算密集型负载。

## 在 Atom 演化中的定位

Crestmont 出现在 Tremont→Gracemont 之后超过两年，但改进幅度远小于之前任何一代跨越。作者认为原因在于 Meteor Lake 本身已经是一次工程超载：芯片粒化（TSMC + Intel 混合制造）、废弃 Sandy Bridge 沿用超十年的环形总线架构、新 NPU、新 iGPU（[[xe-lpg-igpu-architecture|Xe LPG]]）——在这个工程风险极高的周期内，CPU 架构改动相对保守。Crestmont 的继任者 [[skymont-microarchitecture|Skymont]] 则在 Lunar Lake 上做出了远更激进的升级。

## Sources

- [[sources/chipsandcheese-crestmont]]
