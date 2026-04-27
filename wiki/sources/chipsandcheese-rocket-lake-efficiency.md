---
tags: [source, computer-systems, cpu, intel, rocket-lake, power-efficiency, 14nm]
date: 2026-04-27
sources: 1
---

# Was Rocket Lake Power Efficient?（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 12 月的文章，系统分析 Rocket Lake（Intel 11代，Cypress Cove 核心）在不同功耗目标下的效率表现。

## 摘要

Rocket Lake 将 Sunny Cove（10nm 设计）反移植至 Intel 14nm 工艺，因此功耗恶名昭著。文章通过测量 libx264 和 7-Zip 在不同功耗档位下的性能，与同代 14nm CPU（Skylake、Kaby Lake）及 Golden Cove 横向对比，得出更细致的结论：在 30W 以上功耗区间，Rocket Lake 是同工艺中效率最高的方案，优于 Skylake 和 Kaby Lake；但低于 30W 时效率急剧下降，而 Golden Cove 在任意功耗下都全面领先。文章还假设性地探讨了"Rocket Lake + Goldmont Plus"混合架构的可行性，指出 Goldmont Plus 的功耗/性能曲线可以覆盖 Rocket Lake 无法高效运行的低功耗区间。

## 关键要点

- Rocket Lake 在 30W 以上是最高效的 14nm 设计，低频（2.5–3 GHz）区间与 Kaby Lake 相当
- 低于 30W 时效率骤降，是最大短板（无法缩减至低功耗）
- 股票时钟下，Rocket Lake 比 Skylake 快 71.5%，但完成任务耗能近 2 倍
- Goldmont Plus（14nm Atom）可覆盖 Rocket Lake 的低功耗盲区，假设性混合架构逻辑自洽
- Alder Lake 混合架构在 ISA 层面解决了 Rocket Lake 无法与 Atom 混用的问题（AVX-512 / AVX2 不对齐）
- 本文使用 package power（含 L3/ring bus/内存控制器），而非仅 core power

## 链接到的概念

- [[computer-systems/rocket-lake-cypress-cove]]
- [[computer-systems/sunny-cove-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/intel-hybrid-alder-lake]]
- [[computer-systems/dennard-scaling]]
- [[computer-systems/power-wall]]

## 原文

- 链接：https://chipsandcheese.com/p/was-rocket-lake-power-efficient
- 本地：`raw/articles/chipsandcheese.com/2022-12-17_was-rocket-lake-power-efficient.md`
