---
tags: [source, 软件设计, 重构, x-plane]
date: 2026-04-19
sources: 1
---

# When To Rewrite（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月的文章，补完 Joel Spolsky 的「永远别重写」论，把焦点从「重写不划算」推到「大重写必然失败的组织动力学」，并给出可执行的替代：[[incremental-rearchitecting|增量重构]]。

## 摘要

Supnik 把典型大重写项目拆成一段剧本：1.0 由 A 级小团队写出，脏代码他们知道为什么脏；产品赚钱后扩招 B 级开发者做特性，代码质量下降但管理层只看代理指标（bug 数、KLOC）无法识别；决定大重写后团队拆两半，重写组在没发版压力下必然过度架构，市场部把所有愿望清单挂上蓝图，真正让 1.0 赚钱的小特性反而进不去，最终新代码发版当天就被团队自己称为「烂」。文章核心主张是**增量重构**：每做一个新特性前先做一次行为中性的底层重写，让代码变成刚好承载该特性的形状。时机原则：「在你真的会因旧架构损失生产力的前一刻重构，但一定要在 100% 确定必须重构之后」——既别早做（付复杂度税）也别拖到失控。

## 关键要点

- 大重写的失败根源是组织动力学，不是技术难度。
- 管理层缺少测量代码健康度的工具——只有代理指标时无法区分「B 队效率低」和「代码腐烂」。
- 增量重构的正确节奏：先重构刚好要用到的模块，不要为六个月后的特性现在就动手。
- 不要重构永不会改动的模块——只增加测试面不产生价值。
- 与 YAGNI 同源（见 [[future-proofing-tests]]）：默认不做，满足具体条件才做。

## 链接到的概念

- [[incremental-rearchitecting]]
- [[continuous-design]]
- [[strategic-programming]]
- [[tactical-programming]]
- [[future-proofing-tests]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/01/when-to-rewrite.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-02_when-to-rewrite.md`
