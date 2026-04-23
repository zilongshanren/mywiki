---
tags: [source, cpu, intel, alder-lake, golden-cove, 微架构]
date: 2026-04-19
sources: 1
---

# Popping the Hood on Golden Cove（Chester Lam / Chips and Cheese，2021-12-02）

[[chester-lam]] 在 Alder Lake 发售后做的 P-Core 深度拆解，以 Sunny Cove 为对照。

## 摘要

Golden Cove 在所有层面都做得"更宽更深"：ROB 从 352 → 512（+45%），uop cache 从 2.25K → 4K，BTB 翻到 12K 条目、三级结构、miss 惩罚仅 1 周期。L1i → decoder 带宽翻倍到 32 B/cycle，decoder 6-wide，ALU 增到 5 端口（x86 史上最多），AGU 达到 3 load + 2 store。FP 侧尤其强：2 周期 FP add @5 GHz+、vector RF 有 8 read + 3 write 口、L1D 可做 2×512-bit AVX-512 load/cycle。但**整数寄存器堆没扩**——Chester 推测是为了喂 5 条 ALU 要 10+ 个读口，RF 再扩代价过高；结果整数负载里 ROB 常先耗尽 integer RF。分支预测方向精度略逊 Zen 3，zero-bubble 可追踪分支数反从 Sunny Cove 的 256 回退到 128（为让 12K BTB 跑 5 GHz+ 的妥协）。Cache 所有层级延迟高于 Zen 3，但大 ROB 通过 [[littles-law-reorder-buffer|Little's Law]] 足以吸收。L1/L2 带宽怪兽级；DDR5 让 Alder Lake 内存带宽几乎翻倍于 Zen 3 DDR4。Chester 的总评是"Intel 把整数性能留给了 Sapphire Rapids"，FP/vector 侧则是近年最出色的 Intel 设计。

## 关键要点

- ROB +45% 是对 cache 高延迟的 Little's Law 式补偿
- 整数寄存器堆没扩——为 5 ALU 让路
- 12K BTB 三级结构、1 周期 miss 惩罚，但 zero-bubble capacity 回退
- FP add 2 周期 @5 GHz+，历史级水准
- uop cache 4K 条目但实测命中行为像 Skylake——大 L1i 带宽补位
- Move elimination 与 zeroing idiom elimination 两端满血：所有 zeroing 都能消掉

## 链接到的概念

- [[golden-cove-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[move-elimination-zeroing-idioms]]
- [[littles-law-reorder-buffer]]
- [[branch-predictor-design]]
- [[op-cache-decoded-uop-cache]]

## 原文

- 链接：<https://chipsandcheese.com/p/popping-the-hood-on-golden-cove>
- 本地：`raw/articles/chipsandcheese.com/2021-12-02_popping-the-hood-on-golden-cove.md`
