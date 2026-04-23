---
tags: [source, chipsandcheese, cpu, 微架构, zen2, op-cache]
date: 2026-04-19
sources: 1
---

# How Zen 2's Op Cache Affects Performance（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 7 月发表于 [[chips-and-cheese]] 的文章，用一枚未公开的 MSR 位（0xC0011021 bit 5）强制关闭 Zen 2 的 [[op-cache-decoded-uop-cache|op cache]]，再通过 PMU 对比关闭前后的性能与功耗，定量回答"op cache 到底值多少性能 / 值多少能耗"。

## 摘要

测试平台 3950X（固定 3.5 GHz，关闭 boost），覆盖 Cinebench、3DPM v2.1、Y-Cruncher、Vray、代码编译、CPU-Z 六类 workload。Op cache 命中率差异巨大——CPU-Z / 3DPM 超 90%，CBR 50–60%，编译 / Vray 更低。关闭 op cache 后 Cinebench 与 3DPM 性能下降 >10%，且核功耗反升（因前端喂得更饱、后端更忙），反推出解码器自身功耗很小。通过 CPU-Z 单线程场景（op cache 开关下分数不变）隔离测得解码器约 0.24 W（~4% 核功耗）。结论：op cache 是典型的 "always win" 设计——性能最高 >10% 提升，同时总是省电。ARM/Intel 的 op cache 虽容量更小，趋势一致。

## 关键要点

- Zen 2 op cache = 4k 条目，Zen 1 = 2k，Intel DSB = 1536，Cortex-A77 = 1.5k
- Intel 宣传 80% / ARM 宣传 85% 命中率普遍乐观，实测随 workload 大幅波动
- CBR、3DPM 关闭 op cache → 性能 ↓10%+，核功耗 ↑（执行单元被喂得更足）
- Vray、编译 → 关闭 op cache 几乎感受不到，前端本非瓶颈
- 解码器核功耗占比 ~4%（估 0.24 W），package 功耗 <1%
- Intel 把 LSD（loop buffer）单独计数，MS（microcode sequencer）不走 op cache
- AMD / Intel / ARM 都用 op cache → x86 "decode tax" 说法站不住

## 链接到的概念

- [[op-cache-decoded-uop-cache]]
- [[zen2-microarchitecture]]
- [[branch-predictor-design]]
- [[isa-implementation-not-architecture]]

## 原文

- 链接：https://chipsandcheese.com/p/how-zen-2s-op-cache-affects-performance
- 本地：`raw/articles/chipsandcheese.com/2021-07-03_how-zen-2s-op-cache-affects-performance.md`
