---
tags: [source, 游戏引擎, game-engine-architecture]
date: 2026-04-05
sources: 1
---

# Game Engine Architecture Day 1 —— 引擎是什么

Game Engine Architecture (Jason Gregory) 学习推送第 1 天。

## 摘要

从三个角度回答「引擎为什么存在」：**运行时基础设施**、**工具/管线**、**商业风险管理**。引擎与游戏的边界是模糊且动态的。**数据驱动架构**是真正引擎 vs 游戏专用软件的分水岭。**软实时**特征。

## 关键要点

- 引擎存在的根本原因是**生存**——每个游戏都需要同样的几千行渲染、动画、物理、音频、I/O、输入、内存管理代码。
- 引擎/游戏边界动态——好工程师持续把可复用的"游戏代码"提升为"引擎代码"。
- **分层原则**：上层依赖下层，反向是死刑。
- **数据驱动**：渲染任意 Entity via component query（引擎）vs 硬编码 Orc rendering（游戏）。
- **软实时**：时间约束但允许偶尔违反（与硬实时如起搏器不同）。
- **基于智能体的模拟**：游戏世界由独立 Entity 构成。
- **Unity vs Unreal 哲学**：Unity 最大灵活性（GameObject+Component 组合，代价是 GetComponent 和 cache 局部性差）；Unreal 框架式（内建网络/序列化/生命周期，代价是编译时间和学习曲线）。
- **DOTS/ECS**：用 SoA 解决 AoS cache 问题。

## 链接到的概念

- [[game-engine]]
- [[data-driven-architecture]]
- [[soft-real-time]]
- [[engine-layering]]
- [[unity-vs-unreal]]

## 原文

- 链接到：[[raw/articles/game engine architecture/day01]]
