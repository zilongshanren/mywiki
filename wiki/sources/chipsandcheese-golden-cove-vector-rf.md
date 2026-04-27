---
tags: [source, computer-systems, cpu, intel, golden-cove, avx512, register-file, smt]
date: 2026-04-27
sources: 1
---

# Golden Cove's Lopsided Vector Register File（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 12 月的文章，揭示 [[computer-systems/golden-cove-microarchitecture|Golden Cove]] 向量寄存器文件的非对称设计，以及 SMT watermark 分配机制。

## 摘要

自 Intel 引入 AVX-512 以来，向量寄存器物理上被拆为两半：低 256-bit 存放在靠近执行单元的主寄存器文件，高 256-bit 存放在对面的扩展区域。Golden Cove 在此基础上更进一步：扩展区域（512-bit 容量部分）的条目数少于低 256-bit 区域，形成"不对称寄存器文件"。微基准实测：Golden Cove 约有 295 个 256-bit 重命名槽，但仅约 210 个 512-bit 重命名槽。Golden Cove 的重命名器具备跟踪两个独立池的能力，并用启发式判断一条 256-bit 结果是否需要写入 512-bit 容量槽。SMT 场景下，Golden Cove 采用 watermark 机制（非固定对半分）：单线程繁忙时最多可用 221 个 FP 寄存器（512-bit 模式为 141），保证兄弟线程至少 130 个（512-bit 模式为 106）。对比 Zen 4：AMD 的 SMT 是完全竞争式共享，无 watermark，也无 512-bit 容量限制。

## 关键要点

- Golden Cove 向量 RF：~295 个 256-bit 槽 vs ~210 个 512-bit 槽（非对称）
- 交替写入 256-bit 和 512-bit 指令时，总容量达到最大（两个池都被充分利用）
- SMT watermark：一线程最多 221 FP / 141 AVX-512；最低保障 130 / 106
- 对比 Skylake：固定对半分；Ice Lake SP：已引入 watermark（Golden Cove 是第二代）
- Zen 4 无此不对称设计，SMT 完全竞争共享，两个 256-bit / 512-bit 容量相同
- Golden Cove 上 AVX-512 实际对大多数用户无法访问（量产芯片 fuse off），本文使用未 fuse off 的特殊 BIOS

## 链接到的概念

- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/avx512-cache-efficiency]]

## 原文

- 链接：https://chipsandcheese.com/p/golden-coves-lopsided-vector-register-file
- 本地：`raw/articles/chipsandcheese.com/2022-12-25_golden-coves-lopsided-vector-register-file.md`
