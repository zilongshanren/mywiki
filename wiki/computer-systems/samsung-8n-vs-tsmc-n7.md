---
tags: [process-node, samsung, tsmc, ampere, rdna2, 能效]
date: 2026-04-19
sources: 1
---

# Samsung 8N vs TSMC N7：Ampere 的低能效不全是 node 的锅

2020 年 Ampere 发布后的主流叙事是"Nvidia 被 Samsung 8N 拖累，如果上 TSMC N7，Ampere 能效会全面反超 RDNA2"。Jeremy Tingle / Chips and Cheese 2021 年 6 月的文章逐条拆解这一说法：Samsung 8N 确有差距但不构成代差，Ampere 的能效瓶颈更多出在架构与 GDDR6X 选型，不是 node。

## 8N 到底是什么

8N 是 Samsung 8LPU 的定制变种，而 8LPU 本身是在 8LPP 的基础上用 uLVT 库进一步提升 HPC 性能的非 EUV 节点。Samsung 的 node 规划偏"渐进"：11LPP 用 10nm BEOL 把 14nm 产品的密度推近 10nm；8LPU 则把 10nm 推近自家准备上 EUV 的 7nm。8LPU 和 TSMC N7 不是同一级，但"整整落后半代"也不准确。

手机 SoC 的对照是目前最有说服力的 apples-to-apples：Samsung Exynos 9820（8LPU）和华为 Kirin 980（N7）使用几乎相同的 ARM Mali G76 GPU，GFXBench Manhattan 3.1 下 Exynos 的 perf/watt 甚至略胜（且 Exynos 系列本身不以性能见长）。这暗示 8LPU 与 N7 在"同架构移植"上的能效差距小于一般认知。

## Nvidia A100 反向证据

A100 用 TSMC N7，密度比同节点的 AMD Navi 10 高 50% 以上。但 AMD 的 MI100（同样 N7）再反超 A100 密度，说明两家的物理设计能力相当——Nvidia 的密度优势是"低频 HPC 设计"带来的，而非 Samsung 不给力。消费级 Ampere 为了拉高时钟牺牲了密度，和当年 [[gcn-wave-occupancy|GCN]] 的 Fiji 面对 Maxwell 一样。

## 时钟不等于 node

自 GCN 以来 Nvidia 在相近节点上始终能跑更高时钟（Fiji 1.1 GHz vs GM200 1.3 GHz；Polaris 1.25 GHz vs Pascal 1.83 GHz）。如果仅归因 node，一旦 Nvidia 上 TSMC N7 应该能轻松 2.3–2.5 GHz——但 RDNA2 反超靠的不是 node，是 AMD 两件事：

- **DTCO（design technology co-optimization）**：Maxwell 在 28nm 上靠晶体管级协同把 28nm 吃出接近 20nm 的表现，现在 AMD 在 N7 上用到第三代（Vega20 / Navi10 / Navi21），积累的 path optimization 经验比 Nvidia 多
- **CPU 团队迁移**：Zen 的高频设计经验（Infinity Cache 的 SRAM 设计直接来自 EPYC L3）让 GPU 团队吃到红利

这与 [[ampere-warp-stall-utilization]] 里 Ampere 的架构级问题（FP/INT 合并 pipe、核心数过多导致 occupancy 不足）互相印证。

## GDDR6X 的功耗代价

RTX 3070 Ti 与 3070 核心几乎相同，只换了 GDDR6X，TDP 高了 70 W——PAM4 信号对 memory controller 功耗的额外代价。AMD 在 RDNA2 上选择了不同的平衡：不上新一代内存技术，而是用 Infinity Cache（估 6.144 B transistor、135 mm²、约占 Navi21 总面积 25%），用 SRAM 换外部带宽功耗。TSMC N7 的 SRAM 密度优势让这笔交易合算，AMD 同时在 Zen 2 里也用过这招（见 [[cpu-performance-formula]]）。

## 历史对照：2009 年 GT200B

Nvidia 65nm 的 GT200 对 AMD 55nm 的 RV770 已略逊；半年后 Nvidia 把 GT200 die-shrink 成 55nm 的 GT200B 发布 GTX 285，但只拿到 5% 性能 + 10% 能效改善——die shrink 旧架构远不如为新节点重新设计。"如果 Ampere 搬到 N7 就能赢"是同一种想法，大概率结果也差不多。

## Sources

- [[sources/chipsandcheese-ampere-samsung-process]]
