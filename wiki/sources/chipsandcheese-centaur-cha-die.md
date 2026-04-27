---
tags: [source, cpu, centaur, die, avx-512, 密度, 面积]
date: 2026-04-27
sources: 1
---

# Examining Centaur CHA's Die and Implementation Goals（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 4 月的文章，分析 Centaur CHA SoC 的 die 面积分布，并将 CNS 与 Haswell-E、AMD Zeppelin（Zen 1）、Intel Coffee Lake 在设计哲学层面做横向比较，讨论 Centaur 如何用"密度优先"原则在有限面积内塞下 8 核 + ML 加速器。

## 摘要

CHA（TSMC 16nm，194 mm²）中，8 个 CNS 核+L3 仅占约三分之一 die 面积，NCore 占等量，IO/互连占其余。Haswell-E（Intel 22nm，355 mm²）在核数和 IO 规模相似的前提下，核+L3 占约 50%。密度差异的来源：CNS 针对低时钟（2.5 GHz）设计、使用高密度 cell library；AVX-512 以最小面积方案实现（mask 寄存器共享 GPR 物理堆，不加宽执行单元）；IPC 目标保守（Haswell 对标），避免出于边际 IPC 收益而膨胀 ROB/scheduler。ChampSim 仿真显示即使是 Golden Cove 的高延迟 L3 场景，ROB 超过 ~200 条目后收益快速递减，验证了 Centaur 保守 ROB 选择的合理性。

## 关键要点

- CNS+L3 仅占 CHA die 三分之一，NCore 占等量——设计以 ML 加速器优先，CPU 为辅
- 密度策略三要素：低时钟目标 + 最小面积 AVX-512 实现 + 保守 ROB sizing
- AVX-512 实现与 Skylake-X 对比：Skylake-X 加宽至 512-bit 执行单元（最大吞吐），CNS 维持 256-bit + 拆两条 micro-op（最小面积），各有适用场景
- Y-Cruncher（高 AVX-512 密度）：CNS 可与 Zen 1 持平，在重向量 compute 上体现 ISA 优势
- 7-Zip（重分支）：CNS 落后 Zen 1 和 Haswell，印证分支预测器是短板
- 结论：CNS 证明了在有限资源下实现强向量执行能力的可行性；Centaur 百人团队在末代 TSMC 节点上完成了高密度 SoC 设计

## 链接到的概念

- [[centaur-cns-microarchitecture]]
- [[dispatch-stall-breakdown]]
- [[littles-law-reorder-buffer]]
- [[gracemont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/examining-centaur-chas-die-and-implementation-goals
- 本地：`raw/articles/chipsandcheese.com/2022-04-30_examining-centaur-chas-die-and-implementation-goals.md`
