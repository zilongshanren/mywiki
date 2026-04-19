---
tags: [source, ecs, 架构, svelto]
date: 2026-04-19
sources: 1
---

# Entity Component System abstraction layers and modules encapsulation（Sebastiano Mandalà / Seba's Lab）

[[sebastiano-mandala]] 2022 年 3 月的长文，是他 *Entity Component System Code Design* 系列的压轴篇，把 OOP 世界里 Robert Martin 的 *Inversion of Control Layer*、Granularity、Stability 等原则移植到 ECS 设计之上。

## 摘要

作者从"框架 vs 用户代码是非黑即白"的游戏引擎现状切入，指出 Unity Monobehaviour 完全由框架驱动、用户不能自己写框架层的结构让更专门化的 IoC 无处落地；IoC 容器类工具（ZenInject、StrangeIoC）则走另一个极端——让所有对象互相知道，最终得到意大利面代码。ECS 天然适合分层，因为 component 充当 OOP 里的 interface、system 充当策略模式的调度方。Mandalà 主张用 assembly / dll / asmdef 做强制边界，层与层之间**只允许单向依赖**（循环依赖在 asmdef 上直接不编译），高层提供通用 component / system / group tag，低层通过 ExtendibleEntityDescriptor 组合自己的 entity。他以 Svelto.MiniExample 7（Stride Turrets）为例演示拆分：Transformable / SimplePhysic / StrideAbstraction / Player / Bullet / Enemy / Game 七个 context，每个是独立静态 `Compose()` 入口，engine 全部 `internal`。

## 关键要点

- ECS 代码组织的顶层原则：**依赖倒置 + Hollywood Principle + Granularity + Stability**
- assembly 是唯一靠谱的封装机制，asmdef 单向依赖是"天然护栏"
- 高层 engine 用 `FindGroups<T>()`（不预设 group），低层 engine 用 group compound tag（显式 group）
- Composition root 只在最外层 Game 层出现，每一 context 只负责把自己的 engine 注册进 EnginesRoot
- engine 一律 `internal`，用 Add callback 或 descriptor extension 跨层交互
- "Early abstraction is the root of all evil"——先让代码能跑，共享行为浮现后再重新打包

## 链接到的概念

- [[ecs-abstraction-layers]]
- [[svelto-ecs]]
- [[sebastiano-mandala]]

## 原文

- 链接：https://www.sebaslab.com/ecs-abstraction-layers-and-modules-encapsulation/
- 本地：`raw/articles/sebaslab.com/2022-03-20_entity-component-system-abstraction-layers-and-modules-encap.md`
