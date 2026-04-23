---
tags: [source, chipsandcheese, cpu, 微架构, x86, zhaoxin, lujiazui, avx]
date: 2026-04-19
sources: 1
---

# The Weird and Wacky World of VIA Part 2: Zhaoxin's Lujiazui（George Cozma + Chester Lam / Chips and Cheese）

[[george-cozma]] 与 [[chester-lam]] 2021 年 9 月发表于 [[chips-and-cheese]] 的两部曲第二集，深挖 2013 年兆芯与上海市政府合资后演化出的 Lujiazui 核。Lujiazui 经历 Zhangjiang（Isaiah II 加国密 SM3/SM4）→ Wudaokou（IPC +25%）→ Lujiazui（工艺 HLMC 28nm → TSMC 16nm，时钟 +50%）三代，作者指出命名"50% 提升"里一半是工艺。

## 摘要

Lujiazui 的改动方向与 Isaiah 完全相反——**把大核砍窄**。解码 3-wide → 2-wide，ROB 65 → 48，退回 P6 式 ROB+RRF（整数与 256-bit AVX 共享寄存器文件），L1D 64 KB → 32 KB，4 核共享 4 MB L2（类似 Zen 1/2 APU 布局），IMC 上 die 取代 FSB。分支预测加了 16 项 L0 BTB（零气泡 taken，类似 Zen 2），但主 BTB 仍 4096 项 + 2 气泡，方向预测器从 Isaiah 几乎没改；return stack L1 只 2 项、L2 延迟 13–16 周期，深嵌套堪比 Haswell 栈溢出。AVX 实现只够"声称支持"：256-bit 指令拆成两条 128-bit 微操作吃双 ROB 槽，还额外加延迟；ROB 小、RF 共享导致 256-bit AVX 场景 reordering 容量腰斩；AVX2 的 FMA 直接 fault，但 256-bit 整数加法意外能用。不做 memory dependence prediction——load 不能越过地址未知的 store（Core 2 2006 年就有）。Lujiazui 目的明确：为了塞 8 核放弃单核宽度换面积和功耗。作者结论——Nano 是假装低功耗的大核；Lujiazui 是假装大核的低功耗核，真正对标应是 Jaguar / Goldmont。

## 关键要点

- 解码 2-wide、ROB 48、P6 式 ROB+RRF 是明显退步
- L0 BTB + 主 BTB 双级是 Zen 2 启发的现代设计
- L2 return stack 13–16 周期延迟，深嵌套 = 灾难
- 256-bit AVX 拆分 + 延迟惩罚 + 寄存器共享 = 实用中应避免
- AVX2 FMA fault，256-bit 整数加法意外能跑
- 无 memory dependence prediction，属 2005 年前的设计
- 25% 十年 IPC 涨幅追不上 Intel/AMD；对标 Jaguar/Goldmont 才公允

## 链接到的概念

- [[via-x86-isaiah-lujiazui]]
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]
- [[zen2-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/the-weird-and-wacky-world-of-via-part-2-zhaoxins-not-quite-electric-boogaloo
- 本地：`raw/articles/chipsandcheese.com/2021-09-22_the-weird-and-wacky-world-of-via-part-2-zhaoxins-not-quite-e.md`
