---
tags: [source, chipsandcheese, cpu, 微架构, arm, neoverse-n1, zen2]
date: 2026-04-19
sources: 1
---

# Neoverse N1 vs Zen 2: ARM in Practice（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 8 月发表于 [[chips-and-cheese]] 的实战对比，接续 [[chipsandcheese-isa-doesnt-matter|ISA 无关论]]那篇从理论走到实测——把 Ampere Altra（Neoverse N1，4 核云实例）与 3950X（Zen 2，关 SMT、4 核）放到同一批 workload 上跑。结论进入 [[neoverse-n1-microarchitecture]]。

## 摘要

作者坦承 Zen 2 与 N1 设计目标不同——Zen 2 覆盖笔记本到超算，更深更宽更高频；N1 脱胎于 A76，面向功耗敏感服务器。因此重点不是谁赢绝对分数，而是 N1 是否按设计该有的水平发挥。测试覆盖 OpenSSL RSA2048（N1 惨败：3 GHz Zen 2 快 4 倍，连 FX-8350 都不如，作者判为架构硬伤）、7z 文件压缩（N1 同频仅落后 17.3%）、Gem5 编译（同频 N1 甚至快 Zen 2 1%）、libx264（Zen 2 同频快 41.6%）、libx265（Zen 2 同频快 ~9x，ISA 生态彻底拖后腿）、libaom-av1（Altra 几天跑不完 Zen 2 一小时的活）、Blender（Zen 2 同频快 34.7%）。微基准部分测得 N1 分支预测器走"快但不够准"的权衡：L1 BTB 快、模式识别能力弱于 Zen 2；寄存器文件估算 120 INT + 128 FP/SIMD。功耗上，按 ARM 官方数字（1–1.8 W/核 @ 2.6–3.1 GHz），N1 仍保有能效优势——除非涉及 libx265 这类生态惨败场景。

## 关键要点

- OpenSSL RSA2048：3 GHz Zen 2 快 4 倍，N1 三条 ALU 跑不过 FX-8350 两条
- 7z / 编译：N1 同频与 Zen 2 基本同代，编译甚至略胜
- libx264 / x265 / av1 / Blender：Zen 2 大幅领先，主因 AVX2 宽度 + 成熟汇编
- N1 分支预测：L1 BTB 快，pattern recognition 在 512+ 开始劣化
- 估算物理寄存器：N1 约 120 INT + 128 FP/SIMD
- ARM 官数 1–1.8 W/核 → N1 每瓦效率仍胜 Zen 2（非向量场景）
- 软件生态是实际瓶颈：libaom-av1 aarch64 无手写汇编 → 无法用

## 链接到的概念

- [[neoverse-n1-microarchitecture]]
- [[isa-implementation-not-architecture]]
- [[zen2-microarchitecture]]
- [[branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/neoverse-n1-vs-zen-2-arm-in-practice
- 本地：`raw/articles/chipsandcheese.com/2021-08-05_neoverse-n1-vs-zen-2-arm-in-practice.md`
