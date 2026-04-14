---
tags: [source, gpu, gcn, 性能优化, shader]
date: 2026-04-14
sources: 1
---

# GCN – two ways of latency hiding and wave occupancy（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 3 月的 GDC 后续技术博客，针对 AMD **GCN（Graphics Core Next）** 架构上的「shader 占用率（wave occupancy）何时才重要」给出系统答案。与 Michal Drobot 共同总结的经验，是 Xbox One / PS4 时代主机 shader 调优最常被引用的一手材料之一。

## 摘要

文章以 GCN 的 `s_waitcnt` 指令为切入点，把 GPU 隐藏内存延迟的手段分成两条互相冲突的路径。**第一条**是在 wave 内让编译器展开循环、预取大量样本到 VGPR、把 ALU 插在 texture fetch 之后——代价是寄存器占用爆炸、占用率降低；**第二条**是 CU 上挂更多 wave，当一个 wave 卡在 `s_waitcnt` 时切到别的 wave 跑——代价是每个 wave 可用的 VGPR 上限更紧。两条路方向相反：前者要「低 occupancy + 多 unroll」，后者要「低寄存器 + 高 occupancy」。作者以老式 Poisson DOF 为例展示编译器默认的展开选择——大量 VGPR、低 occupancy、但所有 `s_waitcnt` 都被大量独立 ALU 顶过去了，实际没有等待，即便强行压回循环、提升 occupancy，性能反而下降（cache thrashing + 纹理单元上限）。反面例子是带 data-dependent flow control 的 shader——循环依赖 fetch 结果、分支依赖 BRDF 类型，这类没办法在单 wave 内拉开 fetch 和 use 的距离，**只有高 wave occupancy 能救**，因此必须把 VGPR 用量压到极低。AC4 上的 SSR 和 POM 属于后者。文章给出一套经验法则：简单多样本后效用「高 unroll + 低 occupancy」，现代 next-gen 算法（ray tracing、ray marching、indirection tables、BRDF 分支、forward+ 光源分支、data-dependent flow control）用「高 occupancy + 低寄存器」。

## 关键要点

- **两种延迟隐藏路径是对偶的**：per-wave ILP（unroll + 寄存器）和 per-CU TLP（occupancy + wave 切换）。
- **`s_waitcnt vmcnt(n)`** 是 GCN 上真正产生 stall 的指令——要看 ISA disasm 才能判断 fetch 和 use 之间是否有足够 ALU 把它顶过去。
- **VGPR = wave 寿命 × 同时存活值**：循环展开把 fetch 提前会延长寄存器寿命，压缩 occupancy。
- **Occupancy 不是越高越好**：带宽饱和 / 纹理单元饱和 / L1 cache 4-way 16KB 极小的场景里，高 occupancy 反而 cache thrashing 掉性能。
- **何时必须拼 occupancy**：data-dependent flow control、dependent texture reads、多层 indirection、BRDF / 光源类型分支——也就是任何没法把 fetch 拉离 use 的 shader。
- **[[hbao-interleaved-sampling|HBAO 式后效]] 倾向前者，[[hybrid-raytracing-pipeline|ray tracing / ray marching]] 倾向后者**。
- **常量 cache（LGKM_CNT）通常不是瓶颈**：constant buffer 有独立的 scalar cache，延迟低；真正要盯的是 VMCNT。
- **一般原则**：高级图形程序员也必须读 ISA。

## 链接到的概念

- [[gcn-wave-occupancy]]
- [[gpu-latency-hiding]]
- [[latency-vs-throughput]]
- [[register-spilling-avoidance]]
- [[cache-friendliness]]
- [[cuda-memory-hierarchy]]
- [[screenspace-reflections]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/03/27/gcn-two-ways-of-latency-hiding-and-wave-occupancy/
- 本地：`raw/articles/bartwronski.com/2014-03-27_gcn-two-ways-of-latency-hiding-and-wave-occupancy.md`
