---
tags: [source, chipsandcheese, cpu, startup, tachyum, prodigy, vliw, hpc, ai]
date: 2026-04-27
sources: 1
---

# Tachyum's Revised Prodigy Architecture（Chester Lam & Dr Ian Cutress / Chips and Cheese）

[[chester-lam]] 与 Dr Ian Cutress 发表于 2022 年 8 月的文章，分析 Tachyum 2022 版 Prodigy 架构相对于 2018 版的重大变化，并评估其在服务器、HPC 和 AI 市场的竞争力。

## 摘要

2022 版 Prodigy 放弃了 2018 版的 VLIW bundle 设计，改用 4/8 字节固定宽度指令的常规 ISA，并在硬件中实现依赖检查。核心从单次检查点扩展到多检查点的乱序执行方案。向量执行单元从 512-bit 加倍到 2 × 1024-bit。L1D 容量从 16 KB 扩到 64 KB，BTB 容量翻倍（仍与 L1i 耦合）。DDR 内存侧改用 16 控制器 DDR5-7200 方案（1024-bit 总线），放弃 HBM。文章作者认为 HPC/AI 潜力真实存在，但对 5.7 GHz 时钟目标持怀疑态度，对服务器市场前景也较为悲观。

## 关键要点

- 2022 版 Prodigy 本质上是另一个架构，与 2018 版无兼容性，分析需重新建立
- gshare 分支预测器（全局历史）因标准单元库限制无法升级为 TAGE，BTB 仍为耦合设计
- 虚拟 L3（空闲核心贡献 L2 容量）是创新但实现复杂度极高
- QEMU 模拟 x86/ARM 仍有 30-40% 性能损失（2018 估计 80%+ 有所改善）
- 10 级整数流水线对 5.7 GHz 目标过短；Neoverse N1（11 级）仅 3.3 GHz

## 链接到的概念

- [[tachyum-prodigy-architecture]]
- [[branch-predictor-design]]
- [[cache-power-efficiency]]

## 原文

- 链接：https://chipsandcheese.com/p/tachyums-revised-prodigy-architecture
- 本地：`raw/articles/chipsandcheese.com/2022-08-26_tachyums-revised-prodigy-architecture.md`
