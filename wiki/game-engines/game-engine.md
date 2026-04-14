---
tags: [游戏引擎, gea, 核心概念]
date: 2026-04-05
sources: 2
---

# 游戏引擎（Game Engine）

Jason Gregory 在 *Game Engine Architecture* 中从三个角度回答"引擎是什么"：

1. **运行时基础设施**：一个分层系统，提供渲染、动画、物理、音频、资源管理、场景管理、输入、脚本等核心服务，夹在游戏逻辑层与平台抽象层之间。
2. **工具/管线**：美术资产导出、关卡编辑、构建、部署——这些工具本身就是引擎的一部分。
3. **商业风险管理策略**：自研 vs 商业 vs 开源，每个选择对应不同的技术债与商业风险。

## 为什么引擎存在

**引擎存在的根本原因是生存**——每个游戏都需要同样的几千行渲染、动画、物理、音频、I/O、输入、内存管理代码。跨项目复用不是可选的。

## 引擎与游戏的边界

**边界是模糊且动态的**。好的工程师持续把可复用的"游戏代码"提升为"引擎代码"：

- 硬编码的"Orc rendering" → 可复用的"按 Component 渲染 Entity"。
- 专用的资源加载 → 通用资源系统。
- 一次性的 UI 布局 → 通用 UI 框架。

这正是 [[data-driven-architecture|数据驱动架构]]的内核。

## 引擎是什么游戏？

Gregory 对游戏的定义：**软实时的、交互式的、基于智能体的计算机模拟**。每个词都限定了引擎的必然设计：

- [[soft-real-time|软实时]] → 帧预算
- 交互 → 低延迟输入
- 基于智能体 → ECS / GameObject
- 计算机模拟 → 数学近似而非科学精确

## 相关

- [[data-driven-architecture]]
- [[soft-real-time]]
- [[engine-layering]]
- [[unity-vs-unreal]]
- [[engine-evolution]]
- [[game-physics-engine]] —— 引擎 middleware 层的标配之一，约束式刚体物理流水线

## Sources

- [[sources/gea-day01]]
- [[sources/gea-day02]]
