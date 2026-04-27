---
tags: [source, cpu, intel, lion-cove, 游戏负载, 微架构]
date: 2026-04-27
sources: 1
---

# Intel's Lion Cove P-Core and Gaming Workloads（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 7 月的文章，聚焦 Arrow Lake 平台 Lion Cove P-Core 在实际游戏负载（COD Cold War、Palworld、Cyberpunk 2077）下的微架构表现，使用性能计数器做 top-down 分析。

## 摘要

文章通过 Intel VTune top-down 方法论将 pipeline 停顿分解为前端延迟、前端带宽、后端内存延迟、后端核心约束和 bad speculation 五类。结论是 Lion Cove 游戏负载主要受后端内存延迟拖累，同时前端延迟也有相当损失。与 Zen 5 的对比揭示出两款架构"互补的弱点"：Lion Cove 前端强（L1i 64 KB、12K entry BTB）但 L3/DRAM 延迟偏高；Zen 5 则后端内存延迟相对有限，但前端延迟更突出。

## 关键要点

- 游戏是典型低 IPC 负载（3 款游戏 IPC 均远低于 4），frontend latency + backend memory latency 合计占大多数无用 pipeline slot
- L1.5（192 KB）在 Palworld 中命中率贡献显著，可把部分 L2 命中加速为 L1.5 命中
- L2 累计命中率（含 L1.5）：75–86%，大多数 L1 miss 不会离开 core
- L3 和 DRAM 访问虽少但代价极高，是性能主要瓶颈
- Arrow Lake 互连复杂化（chiplet 化）引入的额外 L3/DRAM 延迟是已知弱点
- 分支预测准确率极高，BTB 命中率良好（BAClears 影响小）；mispredicts 虽偶发，但暴露前端于 L2+ 指令延迟时代价高
- Lion Cove 每次恢复正常退役时平均连续退役 28 条 micro-op，呈间歇性"爆发"模式

## 链接到的概念

- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/op-cache-decoded-uop-cache]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-lion-cove-p-core-and-gaming
- 本地：`raw/articles/chipsandcheese.com/2025-07-06_intels-lion-cove-p-core-and-gaming-workloads.md`
