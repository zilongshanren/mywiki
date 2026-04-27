---
tags: [source, computer-systems, cpu, amd, zen5, microarchitecture, hot-chips, branch-predictor, scheduler]
date: 2026-04-27
sources: 1
---

# Discussing AMD's Zen 5 at Hot Chips 2024（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 9 月的文章，结合 Hot Chips 2024 AMD 正式报告与现场工程师侧谈，深入剖析 Zen 5 微架构的多个设计决策。

## 摘要

本文是对 AMD Zen 5 Hot Chips 2024 演讲及幕后工程师对话的综合报道。前端方面，AMD 工程师解释了为何双解码集群（dual decode clusters）无法为单线程服务：由于微操作队列必须有序，两路合流的串行代价使其划不来。微操作缓存的条目数虽从 Zen 4 的 6.75K 降至 6K，但通过提高关联度与允许单条目存储多个微操作，实测命中率反而更高。循环缓冲区（loop buffer）在 Zen 5 中未被重新加入，原因是这一功能本质上是功耗优化，而非 IPC 优化，工程资源不值得投入。后端方面，AMD 采用统一整数调度器以支持按年龄选发（age-order picks），此举与 Qualcomm Oryon 的分布式调度策略形成鲜明对比——两家在 Hot Chips 同一届发表了不同立场。FP/向量方面，每周期 4×512-bit 向量整数执行得到测试确认，而两周期向量整数加法延迟源于调度器内部的"慢区"（slow region），并非流水线级数增加所致。L1 数据缓存容量增加 50% 至 48 KB 但延迟保持 4 周期，L3 延迟降低约 3.5 周期。SPEC CPU2017 浮点测试 Zen 5 对 Zen 4 提升高达 29.4%（含 VCache 版则达 55.9%），整数侧提升相对温和。

## 关键要点

- 双解码集群各服务一个 SMT 线程；微操作队列的有序约束使其无法同时服务单线程
- 微操作缓存：6K 项，提高关联度 + 多微操作单条目存储，命中率优于 Zen 4 的 6.75K 版
- 循环缓冲区未加入：主要是功耗优化，工程投入-收益比不合算
- 统一整数调度器支持 age-order 选发；Qualcomm 分布式调度通过细粒化减少冲突实现近似效果
- FP 调度器存在"慢区"：队列满时对最老操作的 1-cycle 延迟操作施加 1 周期额外惩罚
- L1D：48 KB，4 周期延迟，两路 512-bit 加载 + 一路 512-bit 存储/周期
- 内存级并行：追踪中的 L1 miss 上限从 Zen 4 的 24 条增至约 124 条
- SPEC FP 对 Zen 4 提升 29.4%；SPEC INT 提升相对有限

## 链接到的概念

- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/cpu-scheduler-design]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/discussing-amds-zen-5-at-hot-chips-2024
- 本地：`raw/articles/chipsandcheese.com/2024-09-15_discussing-amds-zen-5-at-hot-chips-2024.md`
