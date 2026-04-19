---
tags: [source, 度量, 公式, UI]
date: 2026-04-19
sources: 1
---

# A Formula for Overall System Load（Adam Sawicki）

[[adam-sawicki]] 2026 年 2 月发表的 math puzzle 文章，接着他 2022 年写的[内存碎片度量](https://asawicki.info/news_1757_a_metric_for_memory_fragmentation)同一套路——设计一条能把多个子系统 0…1 的负载合成"整体负载"的公式，并配交互 demo 让读者拖滑块体验。

## 摘要

问题抽象：N 个子系统，每个有 0…1 的负载值，怎么合成一个整体值？列出三条需求（单调、任一到 1 整体到 1、每个输入都可见），依次检验 AVERAGE、MAX、"inverse product"（`1 − ∏(1 − xᵢ)`）、以及最终采用的 "AVERAGE + inverse product 50/50 混合"。最后附交互 demo。结论：**先把需求写成条件，再去选公式**，别反过来。

## 关键要点

- `AVERAGE`：违反"任一到 1 整体到 1"
- `MAX`：违反"每个输入都可见"
- **Inverse product** `1 − ∏(1 − xᵢ)`：三条都满足，但对低输入过度悲观
- 与 `AVERAGE` 50/50 混合：三条满足且低输入不吓人
- 方法论：**交互式 demo > 静态图表**——拖滑块能暴露极端值行为
- 适用场景远超系统监控：CI 健康度、团队健康度、游戏 HUD 整体状态

## 链接到的概念

- [[system-load-formula]]
- [[adam-sawicki]]

## 原文

- 链接：<https://asawicki.info/news_1799_a_formula_for_overall_system_load>
- 本地：`raw/articles/asawicki.info/2026-02-26_a-formula-for-overall-system-load.md`
