---
tags: [source, vertex-shader, 性能分析, nvidia, 固定功能单元]
date: 2026-04-19
sources: 1
---

# The Performance Impact of Vertex Shader Exports（Kostas / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2025 年 9 月 21 日，前一篇[[sources/interplay-gpu-utilisation-holistic|GPU 利用率总结]]提到 VS export 会成为瓶颈、这篇用 RTX 3080 mobile 做受控实验量化了具体代价与背后的硬件结构。

## 摘要

实验装置：渲染 250 实例 × 10 轮，每轮把 VS 导出的 float4 属性数量从 1 加到 10（除 position 外），VS 侧计算极便宜，PS 侧使用极便宜，用 clear depth 排除 overdraw 差异，PS 输出双 RT（模拟 G-buffer）。

N 卡数据流：VS 的输出先存进 SM 的 L1，一块专门分配叫 **ISBE**；Primitive Engine（PE）从 ISBE 读出做 culling / clipping，处理完的新顶点属性再写入 L1 里另一块叫 **TRAM** 的专门分配，供 PS 消费。一个 SM 分 16KB TRAM，每个 attribute component 每个三角形 12 字节（3 顶点 × sizeof(float)）——一个 float4 attribute 48 字节 / 三角形，10 个就 480 字节 / 三角形。所有这些中间存储都可能成为瓶颈：Nsight 里能看到 "Allocation stall"（容量不够）和 "Fill stall"（上游填不够快）。

结果：**1→10 个 float4 export，drawcall 成本几乎翻三倍**。Nsight GPU Trace 看，TRAM 分配从 1,405 字节 / SM 涨到 4,646 字节 / SM，TRAM fill stall 明显增多；VPC（做 cull / clip 的 PE 子单元）压力显著上升，L1↔L2 流量也显著增加（提示 VPC 用 L2 缓冲数据再回 L1 做 TRAM）。ISBE 分配本身不怎么变，但 VS warp 因 ISBE 容量不够被 stall 的比例随 export 数显著上升。结论：export 数增加给 PE + 中间存储同时施压、同时 stall VS 和 PS。

一个精彩反例：如果 PS **不使用** VS exports，drawcall 成本**完全不变**，TRAM 分配也不变——GPU 知道没人用、不再分配。是编译器剥离还是硬件感知不明（需 SASS 验证）。这说明"多导出但未用"的场景有自动优化。

跨厂商对比：AMD GCN 5.0 上，不管 PS 是否使用 exports，drawcall 成本都**保持一致**；且随 export 数增加的上升斜率远小于 N 卡。Radeon Profiler 不再支持 GCN，具体原因无从深查。这条非常重要——"VS export 是瓶颈"主要是 N 卡的观察。

其他微观发现：float 而非 float4 时成本增长远慢（ISBE / PE / TRAM 压力小）；同样的 TRAM 容量 8 个 float 约等于 2 个 float4，说明**粒度是 float 不是 float4**（不会 round up）；float 和 int 交错 export 没测到显著差别，这颗 GPU 不区分插值 / 非插值类型。

## 关键要点

- N 卡 VS→PS 数据流经 ISBE（L1 里 VS 输出缓存）→ PE（含 VPC 做 cull/clip）→ TRAM（L1 里 PS 输入缓存），三者都能成为瓶颈
- RTX 3080 mobile：1→10 float4 export 让 drawcall 成本**近 3 倍**
- PS 不用 VS exports → 分配和成本都不变，GPU 能感知不用就不分配
- AMD GCN 上 export 数影响远小于 N 卡，且 PS 不用的情况下也一样
- 分配粒度是 float 而非 float4（8 float ≈ 2 float4 的 TRAM 开销）
- VPC 可能用 L2 做中间缓冲，L1↔L2 流量随 export 数显著上涨
- 评论里作者补充：如果 PS/VS cost 增加，这些 stall 可能被隐藏——也即极简 PS 放大了 export 成本的可见性

## 链接到的概念

- [[vertex-shader-export-bottleneck]]
- [[gpu-utilisation-holistic-tuning]]
- [[vertex-shader-basics]]
- [[compact-vertex-format]]
- [[bottleneck-analysis]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/09/21/the-performance-impact-of-vertex-shader-exports/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-09-21_the-performance-impact-of-vertex-shader-exports.md`
