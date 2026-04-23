---
tags: [source, chipsandcheese, gpu, 能效, power, ampere, rdna, turing]
date: 2026-04-19
sources: 1
---

# Analyzing Video Card Efficiency, Part I – Power（Serebit / Chips and Cheese）

[[serebit]] 2021 年 9 月发表于 [[chips-and-cheese]] 的 GPU 能效横测首篇，系统比较 Vega 20 / Turing RTX+GTX / RDNA1 / Ampere / RDNA2 在 1080p / 1440p / 2160p 三档的每瓦帧数。本站没有实测条件，数据源是 TechPowerUp 与 Tom's Hardware 两套公开评测的几何平均。

## 摘要

作者定义效率指标为 Frames per Joule（FPS/Watt），在三档分辨率上逐架构点评：**Radeon VII** 在所有分辨率贴底（0.456 f/J @ 1080p）；**Turing RTX** 集中在 0.61 f/J 附近，RTX 2080 Super 与 2070 属于把 die 推过头的例外；**GTX 1660 Ti** 因 shader 多、频率低反而是 Turing 能效王座（0.701 f/J）；**RDNA1** 5500 XT 吃亏、5700 登顶（0.671 f/J）；**Ampere** 的 GDDR6X 型号（3080/3080 Ti/3090）在 1080p 贴底，GDDR6 版（3070/3060 Ti）飙到 0.738 f/J 当时榜首——说明 Ampere 能效差的锅是 GDDR6X 而不是架构；**RDNA2** 最稳，6800 是综合头名，6600 XT 在 1080p 登顶但 4K 因 128-bit 总线 + 32 MB L3 崩盘。GTX 1660 与 1660 Super 除 VRAM 无差（GDDR5 vs GDDR6），仅换显存就把能效从 0.63 推到 0.674，定量展示显存带宽瓶颈的隐形能耗税。作者提醒 Ampere 在 4K 终于跑出架构应有效率（shader 占用率够饱），因此**分辨率换档就会重排架构能效**——只报一个平均数字是误导。

## 关键要点

- FPS/Joule 是唯一能跨架构比较的相对指标，但分辨率敏感
- GDDR6X 在 1080p 是显性能耗负担，在 4K 才翻盘
- GTX 1660 vs 1660 Super：显存换 GDDR6 就 +7% 能效
- 128-bit 总线 + 32 MB L3 的 6600 XT 是 4K 崩盘案例
- RDNA2 代表 AMD 近年首个架构上真有能效优势的一代
- 数据用两家大站几何平均而非自测，样本偏差需注意

## 链接到的概念

- [[gpu-efficiency-fps-per-joule]]
- [[samsung-8n-vs-tsmc-n7]]
- [[ampere-warp-stall-utilization]]
- [[rdna1-overclocking-navi10]]

## 原文

- 链接：https://chipsandcheese.com/p/analyzing-video-card-efficiency-part-i-power
- 本地：`raw/articles/chipsandcheese.com/2021-09-09_analyzing-video-card-efficiency-part-i-power.md`
