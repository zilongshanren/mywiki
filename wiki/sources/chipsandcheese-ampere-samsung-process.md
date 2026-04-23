---
tags: [source, chipsandcheese, process-node, samsung, tsmc, ampere, rdna2]
date: 2026-04-19
sources: 1
---

# Nvidia's Ampere & Process Technology: Sunk by Samsung?（Jeremy Tingle / Chips and Cheese）

[[jeremy-tingle]] 2021 年 6 月的长文，回应流行叙事"Ampere 能效低是因为被 Samsung 8N 拖累"。

## 摘要

作者把 Samsung 8N 还原为 8LPU 的变种——8LPU 本身是在 8LPP 上用 uLVT 库提升 HPC 性能、并作为 EUV 之前的最佳非 EUV 节点。用三组证据反驳"8N 低于 N7 一整代"：(1) Samsung Exynos 9820（8LPU）与华为 Kirin 980（N7）用几乎相同的 Mali G76 GPU，GFXBench perf/watt Exynos 反而略胜；(2) A100 和 MI100 同样 N7，AMD 密度反超 Nvidia，说明两家物理设计能力相当；(3) Pascal 分两头代工——GP107（Samsung 14LPP）与 GP106（TSMC N16）在 GTX 1050 Ti / 1060 上表现接近，证明 Samsung HPC 节点并非不堪。

Ampere 能效问题真正的原因：(a) 架构层面 FP/INT pipe 合并后核心数过大导致 occupancy 与负载均衡下滑（见 [[ampere-warp-stall-utilization]]）；(b) GDDR6X 的 PAM4 信号带来显著功耗（RTX 3070 Ti 仅换 GDDR6X 就比 3070 高 70 W TDP）；(c) AMD 在 N7 上积累三代经验 + Zen CPU 团队的高频设计反哺（Infinity Cache 直接复用 EPYC L3 的 SRAM 设计）。历史对照：2009 年 Nvidia 把 GT200 die shrink 到 55nm（GT200B）仅得 +5% 性能 +10% 能效，证明节点搬迁不能修复架构问题。

## 关键要点

- Samsung 8N ≠ 旧 10nm，是 8LPU 定制变种，与 N7 差距小于坊间认知
- Mali G76 同 GPU 在 8LPU vs N7 上 perf/watt 相近
- A100/MI100 同 N7 下 AMD 密度反超 Nvidia
- RTX 3070 Ti 的 70 W TDP 增量主要来自 GDDR6X PAM4
- RDNA2 时钟优势源自 DTCO + Zen CPU 团队的高频设计经验
- Infinity Cache 复用 EPYC L3 设计，135 mm² 占 Navi21 25% 面积
- GT200 die shrink (65→55nm) 只得 +5% 性能，旧架构移植到新节点收益有限

## 链接到的概念

- [[samsung-8n-vs-tsmc-n7]]
- [[ampere-warp-stall-utilization]]
- [[gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/nvidias-ampere-process-technology-sunk-by-samsung
- 本地：`raw/articles/chipsandcheese.com/2021-06-22_nvidias-ampere-process-technology-sunk-by-samsung.md`
