---
tags: [source, computer-systems, amd, zen4, loop-buffer, frontend, power]
date: 2026-04-27
sources: 1
---

# AMD Disables Zen 4's Loop Buffer（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 11 月的文章，记录并分析了 AMD 通过 AGESA 固件静默禁用 Zen 4 Loop Buffer 的事件。

## 摘要

Loop Buffer 是 CPU 前端的一个小型缓冲区，用于缓存已取出的指令，使短循环可以在关闭部分前端流水线（包括 op cache 和解码器）的情况下持续执行，从而节省功耗。Zen 4 是 AMD 高性能核中首款引入 Loop Buffer 的设计，PPR 文档显示其容量为 144 个微操作（SMT 开启时每线程 72）。CALL/RET 指令会导致循环无法被捕获。

作者将 ASRock B650 主板从 BIOS 1.21（AGESA 1.0.0.6）升级至 BIOS 3.10（AGESA 1.2.0.2a）后，通过性能计数器发现前端微操作来源中 Loop Buffer 项归零，即 AMD 在这一区间内静默禁用了该特性。SPEC CPU2017 整体分数差异不超过 1%，少数子测试（如 544.nab 用 Loop Buffer 覆盖约 25% 微操作流）甚至在禁用后微升，属于误差范围。禁用后 op cache 接管，前端供给几乎不变。

游戏测试（Cyberpunk 2077）发现一个难以解释的现象：在 non-VCache die 上禁用 Loop Buffer 后帧率出现约 5% 的下降，VCache die 则无明显差异。作者多次复测未能消除这一差异，但认为这可能源于固件版本间其他细微变动而非 Loop Buffer 本身。功耗测试因 AMD 功率建模在不同 BIOS 版本间可能存在方法论变化而结论不可靠。

AMD 禁用此功能最可能的原因是发现了硬件缺陷（类比 Intel 因 SMT 交互 bug 禁用 Skylake LSD），但官方从未公告。由于功能本身对性能影响极小（op cache 带宽已足够覆盖 6-wide 重命名级），且 AMD 从未在优化指南中提及 Loop Buffer，此禁用对普通用户几乎无感知。

## 关键要点

- Zen 4 Loop Buffer 容量 144 µop（SMT 时各 72），仅限不含 CALL/RET 的小循环
- AGESA 1.0.0.6 → 1.2.0.2a 之间 AMD 静默禁用，无任何公告
- SPEC CPU2017 性能差异 < 1%，op cache 带宽足以完全覆盖
- Cyberpunk 在 non-VCache die 有难以解释的 5% 帧率差，可能与固件其他变动有关
- 禁用原因推测为硬件 bug（对比 Intel Skylake LSD 因 SMT bug 被禁用的先例）
- 功耗影响未能可靠量化，AMD 功率计数器存在建模不确定性

## 链接到的概念

- [[op-cache-decoded-uop-cache]]
- [[zen4-microarchitecture]]
- [[vcache-3d-die-stacking]]
- [[branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/amd-disables-zen-4s-loop-buffer
- 本地：`raw/articles/chipsandcheese.com/2024-11-30_amd-disables-zen-4-s-loop-buffer.md`
