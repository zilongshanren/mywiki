---
tags: [source, 游戏架构, gameplay, 分层, actor, 持久化, cloudwu]
date: 2026-04-19
sources: 1
---

# Gameplay 上层架构笔记（云风的 BLOG）

[[cloudwu]] 发表于 2024 年 8 月的一篇设计总结，是他自己做独立游戏 demo 过程中边重构边提炼的 gameplay 分层蓝图。包含三层切分（数据模型 / 表现 / 交互）、数据模型内部的 Object / Actor 双类划分、持久化驱动的数据设计原则，以及立即模式 / 保留模式的对接策略。

## 摘要

上层逻辑（gameplay）分三块：**数据模型**是核心，判断标准是"不能有任何直接调用引擎的代码"——不碰图形、界面、时钟、控制输入、OS API（除必要文件 IO）；**表现层**维护大量派生状态，但存档时可以全部丢弃、读档时可以全部重建；**交互层**负责把原始输入翻译成 gameplay 语义的消息，不直接访问数据模型。数据模型内部再分**被动 Object + 自治 Actor**：Object 是按类别聚合的静态数据集合（id + typename 为共有属性），尽量无相互引用、尽量不提供 update；Actor 是消息驱动的状态机，关联一个或多个 Object 并读写它们。gameplay 不做并行（Actor 串行跑避免并发读写）。**持久化方案应优先设计**——不是功能价值，而是它会倒逼你把数据模型本身搞清楚；运行时表示与持久表示应分离，Actor 通常只需持久化"状态机当前状态名"。表现层对接走立即模式或保留模式，但数据模型绝不直接调渲染 API 也不持有 visual object。甚至 `save` / `load` 都应是发给 Actor 的消息，tick 末统一执行。

## 关键要点

- 三层分法的判断标准直接可验证（"有没有直接调引擎代码"）
- Object 被动 / Actor 自治，区分"状态"和"行为主体"
- gameplay 串行处理避免并发复杂度——不为"可能性能"付并发代价
- 持久化是数据模型设计的压力测试
- 运行时表示 ≠ 持久表示（hash 表 vs 顺序列表的例子）
- Actor 通常只需存状态机名字，其余运行时状态可重建
- save / load 作为消息 + tick 末执行，保证数据一致性
- 立即 vs 保留模式按引擎能力选择，混用是常态

## 链接到的概念

- [[gameplay-layering-object-actor]]
- [[immediate-vs-retained-mode]]
- [[save-load-driven-data-design]]
- [[worker-task-dispatch-priority]]
- [[multi-target-pathfinding]]
- [[id-based-lifetime-with-kill-flag]]
- [[ecs]]
- [[snapshot-diff-persistence]]

## 原文

- 链接：<https://blog.codingnow.com/2024/08/> （2024-08-24）
- 本地：`raw/articles/blog.codingnow.com/2024-08-24_yun-feng-de-blog.md`
