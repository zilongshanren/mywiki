---
tags: [游戏开发, unity, ecs, aposd]
date: 2026-04-05
sources: 2
---

# ECS 作为深模块

Unity DOTS 的 ECS（Entity Component System）是一个有趣的深度案例。

## 表面的「浅」

表面上看，ECS 是「浅」的：
- Entity 只是一个 ID
- Component 只是数据
- System 只是处理逻辑
- 三者分离

## 实际的深

实际上 ECS 框架隐藏了大量复杂性：
- **内存布局优化**：相同类型的 Component 连续存储（SOA 布局）。
- **作业系统的线程调度**：Job System 自动并行。
- **Chunk 的动态分配和碎片整理**。
- **查询系统的加速结构**。

从游戏逻辑开发者的视角看，这些全都不可见。你用简单的 `World.CreateEntity()` 和 `EntityManager.AddComponent()` 就能得到高性能的数据导向架构，背后的复杂性完全被框架吸收。

## 对比传统 OOP 架构

Ousterhout 的框架下，ECS 解决了传统 Unity OOP 开发中的复杂性：

- **[[change-amplification]]**：传统 Unity 里，`PlayerHealth` 被多处 `GetComponent<PlayerHealth>()` 访问，改接口要改多处。ECS 把数据（Component）和行为（System）分离，通过查询系统解耦。
- **[[cognitive-load]]**：传统 GameObject 上挂十几个 Component 互相调用，需要在脑子里重建调用图。ECS 的数据扁平、System 的依赖通过数据访问声明（读哪些 Component、写哪些），负荷更低。
- **[[unknown-unknowns]]**：传统的 Singleton 和事件是未知未知温床。ECS 强制显式声明所有数据访问，把隐式依赖变显式。

## 新引入的复杂性

ECS 本身引入了新的复杂性：
- 更陡的学习曲线
- 调试更难
- 思维模式需要转换

这说明设计总是有 trade-off，没有银弹。但方向正确：**把复杂性从隐式变为显式，从散射变为集中**。

## 相关

- [[deep-modules]]
- [[information-hiding]]
- [[dependencies]]——ECS 把依赖变成显式契约
- [[unknown-unknowns]]

## Sources

- [[sources/aposd-day02]]
- [[sources/aposd-day04]]
