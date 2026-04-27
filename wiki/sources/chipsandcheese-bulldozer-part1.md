---
tags: [source, computer-systems, cpu, amd, bulldozer, microarchitecture, frontend, ooo, smt]
date: 2026-04-27
sources: 1
---

# Bulldozer, AMD's Crash Modernization: Frontend and Execution Engine（Chester Lam, Jonas Deutz / Chips and Cheese）

[[people/chester-lam]] 等人发表于 2023 年 1 月的文章，深度剖析 AMD Bulldozer 微架构的前端与乱序执行引擎设计。

## 摘要

Bulldozer 是 AMD 在 2011 年为摆脱老旧的 Athlon/K10 架构所做的彻底重设计。其核心特色是"模块"（module）结构：每个模块包含共享的前端（fetch/decode）与 FPU，以及各线程独立的整数执行核和 load/store 单元。这种 CMT（Cluster Multithreading）设计意在以较小面积支持两条执行流，同时大幅提升 FPU 和前端利用率。但在单线程性能上，Bulldozer 严重落后于同期 Intel Sandy Bridge，乃至甚至不及其前辈 Phenom II。主要弱点包括：分支预测器虽容量更大但速度慢（L2 BTB 需 5 周期）；整数执行单元仅有 2 条 ALU（4-wide 前端但执行力薄弱）；物理寄存器文件（PRF）设计是进步，但 OoO buffer 按线程实际可用量被对半切分；load/store 单元鲁棒性提升但高延迟罚则代价更高。FPU 侧则是亮点：60 条目统一调度器、160 条目 FP RF、原生 FMA4 支持，单线程 FPU 资源比 Sandy Bridge 更充裕，但时钟目标在 32nm 工艺上难以达成。

## 关键要点

- 模块化 CMT 设计：前端和 FPU 两线程共享，整数核和 L/S 单元各自独立
- 分支预测器：BTB 容量提升但 L2 BTB 5 周期延迟，无法背靠背处理 taken 分支
- 乱序执行引擎：全面切换为 PRF 方案（抛弃旧 ROB+RRF），ROB 较 K10 扩大 77%
- 整数侧：40 条目统一调度器，仅 2 条 ALU，按线程可用 ROB 仅 128 项
- FPU 侧：60 条目调度器 + 160 条目 RF，FMA4 支持，256-bit AVX 解码为两条 128-bit micro-op
- Store forwarding 改善但失败惩罚高达 35–42 周期（vs K10 的 10–12 周期）
- Sandy Bridge 在几乎每个关键指标上均领先：BTB 速度、ALU 数量、store forwarding、L3 架构

## 链接到的概念

- [[computer-systems/bulldozer-microarchitecture]]
- [[computer-systems/netburst-microarchitecture]]
- [[computer-systems/non-scheduling-queue]]

## 原文

- 链接：https://chipsandcheese.com/p/bulldozer-amds-crash-modernization-frontend-and-execution-engine
- 本地：`raw/articles/chipsandcheese.com/2023-01-22_bulldozer-amds-crash-modernization-frontend-and-execution-en.md`
