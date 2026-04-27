---
tags: [cpu, 缓存, 仿真, ibm, telum, v-cache, zen3, champsim]
date: 2026-04-19
sources: 1
---

# 缓存容量 vs 延迟：IBM 256 MB L3 与 AMD V-Cache 的取舍

2021 年 Hot Chips，IBM Telum 秀出 **256 MB L3**（5 GHz 下 ~12 ns / 60 cycle 平均延迟），把"缓存是不是该往大里堆"的讨论带回台面。同期 AMD 的 3D V-Cache 把 Zen 3 的 L3 从 32 MB 拉到 96 MB。Chester Lam 用 ChampSim 做了 350 条 trace 的仿真，结论很清晰：**大缓存并非单调优，一切取决于 workload 的 working set 与延迟敏感度**。

## 仿真结果的三类行为

基线：Zen 3 风格的 32 MB L3，46 cycle 延迟。对照：

- **IBM 风格 256 MB L3 @ 60 cycle**：部分 trace IPC 大涨（working set 超出 32 MB 时拯救），但**大多数 trace 在 32 MB 命中率已高**——这部分 trace 被额外 14 cycle 延迟直接惩罚，**IPC 下滑 ~10%** 并不罕见。
- **96 MB V-Cache 乐观版（46 cycle，零延迟惩罚）**：几乎全面正收益，坏情况没有实质回归。
- **96 MB V-Cache 悲观版（52 cycle，+6 cycle）**：大多数受益 trace 少量打折，受损 trace 不超过 5%，整体可接受。

## 游戏是缓存增量的甜点

Chester 没法给游戏抓 trace（抓了要被反作弊 ban），但可以在 3950X 上用 PMU 测 L3 MPKI，再把真实游戏点标到仿真曲线上。结论：

- 游戏的 L3 MPKI（在 16 MB L3 上的 miss 率）恰好位于 **96 MB 配置最占优**的区间；
- 256 MB IBM 式大缓存要等 MPKI 超过 20（很多服务器/数据库场景）才显优势；
- 非游戏基准（部分 Qualcomm 服务器 trace）即便给 96 MB 免费大缓存，也几乎不涨；它们真正要的是**更快、而不是更大**的 L3。

## 为什么 IBM 和 AMD 选了不同方向

- **IBM Z15/Z14** 早在 2019/2017 就分别用过 128/256 MB 大 L3——但 IBM 对准大内存足迹、延迟不敏感的企业负载。
- **AMD** 面对笔记本/桌面/服务器/游戏的混合负载，模拟结果告诉它"快 32 MB + 按需堆 96 MB"是更合理的双路线产品策略。
- **Genoa** 的泄漏 PPR 里没有 32 MB 以上的 L3 配置，说明非 V-Cache 版本仍保留小 L3。

AMD 也明确表示 V-Cache **延迟影响很小**——Chester 估算大概只额外 +2 cycle 左右，属于乐观场景。V-Cache 不是「纯升级」，而是承认"**一刀切的 L3 大小已经做不下去**"，让客户在游戏/数据库/HPC 之间自己挑。

## 方法论提示

仿真用 ChampSim + SRRIP 替换策略，每条 trace 跑 10 亿指令 / 2000 万预热。作者坦承样本有限——trace 来自 ML 预取比赛、Qualcomm 价值预测比赛以及 Daniel Jimenez 的基准集，不是按 workload 均匀抽样。结论方向可靠，**相对幅度不适合较真**。

## 参见

- [[zen2-microarchitecture]]
- [[gpu-memory-hierarchy-latency]]
- [[memory-hierarchy]]
- [[cache-friendliness]]
- [[op-cache-decoded-uop-cache]]

## Sources

- [[sources/chipsandcheese-ibm-l3-v-cache-future]]
- [[sources/chipsandcheese-7950x3d-vcache]]
