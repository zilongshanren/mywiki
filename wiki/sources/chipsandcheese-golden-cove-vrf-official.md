---
tags: [source, computer-systems, cpu, intel, golden-cove, avx512, register-file, smt, sapphire-rapids]
date: 2026-04-27
sources: 1
---

# Golden Cove's Vector Register File: Checking with Official (SPR) Data（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 1 月的文章，用 Sapphire Rapids 官方幻灯片数据对此前 Golden Cove 向量寄存器文件微基准测量结果做交叉验证。

## 摘要

此前 Chips and Cheese 测量 Golden Cove 向量寄存器文件时，AVX-512 启用状态下测到 ~210 个 512-bit 槽和 ~295 个 256-bit 槽。若按架构惯例为 32 个体系结构寄存器预留退休状态，则总向量 RF 应为 327 条目（其中 242 为 512-bit 宽）。实测数略高于理论预留数，原因在于 Golden Cove 沿用了 Ice Lake 的机制：只有当 ZMM16–31 被实际使用时，才为那 16 个上半寄存器保留退休状态槽，其余情况可复用这些槽位来扩大推测窗口。整数 RF 方面，官方 SPR 幻灯片声称比 Sunny Cove 增加了 8 个整数寄存器（280→288），但微基准完全探测不到这 8 个条目的差异——说明额外 8 个寄存器被用于保存某种体系结构状态，并未扩大可见的推测容量。Load Queue 测量值（192 条目）也低于 Intel 官方公布的 240 条目，文章推测双方对"load queue"定义不同。

## 关键要点

- 向量 RF 实测值与 SPR 官方数据基本吻合：约 327 总条目，约 242 个 512-bit 宽槽
- 测量偏高的根因：Intel 仅在 ZMM16–31 被使用时才预留 16 个退休状态槽（粗粒度开关，非按位）
- AMD Zen 4 对比：无此开关机制，SMT 双线程时直接保留全部 32 个向量 RF 条目用于退休状态
- 整数 RF：SPR 官方 +8 条目（280→288），但推测窗口无任何改善（额外条目被用于 SMT 体系结构状态）
- Load Queue：微基准测 192 条目，Intel 官方称 240 条目；双方定义存在分歧
- Zen 架构 Load Queue 反向现象：AMD 官方称 72 条目，实测可跟踪 116 个飞行中 load（Zen 4 为 136）

## 链接到的概念

- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/avx512-cache-efficiency]]

## 原文

- 链接：https://chipsandcheese.com/p/golden-coves-vector-register-file-checking-with-official-spr-data
- 本地：`raw/articles/chipsandcheese.com/2023-01-15_golden-coves-vector-register-file-checking-with-official-spr.md`
