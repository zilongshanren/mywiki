---
tags: [source, chipsandcheese, cpu, 缓存, v-cache, telum, ibm, 仿真]
date: 2026-04-19
sources: 1
---

# Do IBM's Giant L3 and V-Cache Represent the Future?（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 9 月发表于 [[chips-and-cheese]] 的 ChampSim 仿真专题。IBM Hot Chips 2021 展示 Telum 的 256 MB L3（5 GHz 下 12 ns ≈ 60 cycle 平均延迟），同期 AMD 宣布 3D V-Cache 给 Zen 3 加到 96 MB——"缓存是不是越大越好？"作者跑 350 条 trace 给答案。

## 摘要

基线是 Zen 3 风格的 32 MB L3（46 cycle）。仿真两类：**IBM 式 256 MB @ 60 cycle** —— 在大 working set trace 上 IPC 大涨，但 32 MB 已高命中的 trace 因 14 cycle 额外延迟 IPC 损失 ~10%，属于得不偿失；**V-Cache 式 96 MB** 跑两档——乐观 46 cycle（零延迟惩罚）几乎全面正收益；悲观 52 cycle（+6 cycle，对应历史 L3 扩容的惩罚曲线）对部分 trace 有 5% 内损失，但受益 trace 大多保留。游戏 trace 拿不到（反作弊），作者退而求其次：在 3950X 上 PMU 测 L3 MPKI，把真实游戏点标到仿真曲线，发现游戏 MPKI 落在 **96 MB 配置最占优**的区间，256 MB 要等 MPKI > 20 才体现价值。部分 Qualcomm 服务器 trace 即便给 96 MB 免费 L3 也几乎不涨，它们真正要的是更快而非更大。结论——V-Cache 不是纯升级，而是承认"一刀切 L3 大小已经做不下去"，让客户按 workload 选型。IBM 的选择是另一个垂直极端（只管大内存足迹），AMD 覆盖面更广所以不能照搬。

## 关键要点

- 256 MB + 60 cycle 延迟对 32 MB 已命中的 trace 反扣 10% IPC
- 96 MB + 46 cycle（乐观）近乎全面正收益
- 96 MB + 52 cycle（悲观）多数受益 trace 仍保留
- 游戏 L3 MPKI 落在 96 MB 最占优区间，不需要 256 MB
- 部分服务器 trace 给 96 MB 免费 L3 也不涨
- AMD 内部大概率会做 V-Cache 与非 V-Cache 双产品线
- IBM Z15 2019 已用 256 MB L3，AMD 不跟进是策略差异而非落后
- 仿真样本来自 ML 预取与 Qualcomm 价值预测比赛，非均匀抽样

## 链接到的概念

- [[cache-size-vs-latency-tradeoff]]
- [[zen2-microarchitecture]]
- [[gpu-memory-hierarchy-latency]]
- [[memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/do-ibms-giant-l3-and-v-cache-represent-the-future
- 本地：`raw/articles/chipsandcheese.com/2021-09-29_do-ibms-giant-l3-and-v-cache-represent-the-future.md`
