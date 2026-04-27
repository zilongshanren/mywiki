---
tags: [source, computer-systems, arm, cpu, mobile]
date: 2026-04-27
sources: 1
---

# Arm's Cortex A510: Two Kids in a Trench Coat（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2023 年 10 月的文章，深度剖析 Arm Cortex-A510 小核微架构，重点分析合并核（merged core）共享资源设计。

## 摘要

文章基于搭载 Snapdragon 8+ Gen 1 的设备，系统测评 Cortex-A510 的分支预测、前端带宽、执行引擎、浮点/向量单元、L/S 单元及缓存层次。核心发现：A510 从 A55 的 2 宽升级为 3 宽，并引入双核共享 FPU、L2 缓存和 L2 TLB 的合并核配置。FPU 在实际负载中利用率低，共享设计合理；L2 TLB 共享则因顺序核对延迟极敏感而存在多线程代价。Snapdragon 8+ Gen 1 中 A510 实际时钟上限约 1.8 GHz，DRAM 延迟超过 300 ns。文章特别对比了 Bulldozer 的模块化方案，认为两者目标截然不同：A510 追求低功耗面积效率，Bulldozer 则在单线程竞争激烈的市场中以共享资源折损了性能。

## 关键要点

- 3 宽顺序，非阻塞 load 能力相比 A53 提升（可 overlap 12 指令 vs 8 指令）
- 合并核：两颗 A510 共享 FPU、L2 缓存、L2 TLB，节省面积但 L2 带宽不线性扩展
- 伪随机替换策略节省 LRU 位但可能降低命中率
- BTB：64 条目 L1 BTB（1 cycle）+ ~512 条目 L2 BTB（2 cycle），比 A55 翻倍
- 与 Bulldozer 相比：共享资源本身不是 Bulldozer 的失败原因，市场定位差异才是关键

## 链接到的概念

- [[computer-systems/cortex-a510-microarchitecture]]
- [[computer-systems/cortex-a710-microarchitecture]]
- [[computer-systems/bulldozer-microarchitecture]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-a510-two-kids-in-a-trench-coat
- 本地：`raw/articles/chipsandcheese.com/2023-10-02_arms-cortex-a510-two-kids-in-a-trench-coat.md`
