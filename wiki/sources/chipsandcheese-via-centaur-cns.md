---
tags: [source, cpu, via, centaur, cns, x86, avx-512]
date: 2026-04-27
sources: 1
---

# VIA Part 4 – A Deep Dive into Centaur's Last CPU Core: CNS（George Cozma & Chester Lam / Chips and Cheese）

[[george-cozma]] 和 [[chester-lam]] 发表于 2022 年 3 月的文章，对 Centaur CHA 工程样片（2.2 GHz，8 核）做了全面的微架构实测，是首篇对 CNS 核心进行系统性 benchmark 拆解的公开分析。

## 摘要

文章从前端分支预测（方向预测、间接预测、BTB 层次）到后端执行单元（整数、向量/FP、AGU）、store forwarding、缓存/带宽、环形互连，逐层实测。CNS 的核心定位是"Haswell 级 IPC 的极度紧凑实现"，作为 CHA SoC 的计算核为 NCore ML 加速器提供支撑算力。文章指出 CNS 在向量侧（FP add 延迟、整数乘法并行度）实际优于 Haswell，但 BTB 较弱（与 L1i 强耦合）、L1D 延迟偏高、只有 2 个 AGU。整体判断：对于 2.2 GHz 的目标时钟和 Haswell 的对标，CNS 达到了设计目标，但面对 Skylake 乃至 Zen 2 已无竞争力。

## 关键要点

- 分支方向预测历史长度（24 级）超 Haswell（16 级），但间接预测 return stack 只有 7 条目，深调用树代价高
- BTB 与 L1i 强绑定，超出 32 KB 后 taken branch 从 2/cycle 降至 1 cycle 需 3 周期
- 向量执行：2×256-bit FP add/mul，FP add 延迟 3 周期（Haswell 4 周期且只有 1 条管道）；整数乘法 2 条管道（Haswell 1 条）
- AVX-512 实现代价最小化：mask 寄存器复用 GPR 物理寄存器堆，512-bit 指令拆 2 条 256-bit micro-op，不提升吞吐
- Store forwarding 健壮（完整包含型 7 周期），但 partial overlap 代价 21 周期
- L2 读带宽接近 64 B/cycle，超过同期 Intel 任意核心
- 跨路内存与多路实现详见 [[centaur-cha-dual-socket]] 后续分析
- NCore 集成动机：在有限 die 面积内提供服务器推理能力，弥补 CNS 核心数不足的劣势

## 链接到的概念

- [[centaur-cns-microarchitecture]]
- [[via-x86-isaiah-lujiazui]]
- [[golden-cove-microarchitecture]]
- [[dispatch-stall-breakdown]]

## 原文

- 链接：https://chipsandcheese.com/p/via-part-4-a-deep-dive-into-centaurs-last-cpu-core-cns
- 本地：`raw/articles/chipsandcheese.com/2022-03-23_via-part-4-a-deep-dive-into-centaurs-last-cpu-core-cns.md`
