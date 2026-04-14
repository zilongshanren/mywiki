---
tags: [source, 游戏引擎, ecs, 组件, 解耦]
date: 2026-04-14
sources: 1
---

# Refactoring with components（Evan Todd / etodd.io）

[[people/evan-todd|Evan Todd]] 2011 年 2 月的一篇短文，讲他把自研 C# 游戏引擎重构到组件实体模型（component-entity），以及在过程中设计的一套**数据绑定**系统。

## 摘要

Todd 指出传统组件实体架构里一个常见的烦恼：组件之间为了读写彼此的数据，要么经过 ComponentManager 查找（慢），要么直接持有引用（耦合）。他选择了第三条路：让每个组件持有自己独立的数据字段（像 I/O 端口），在**组装 entity 的 factory 里**把不同组件的端口绑定在一起。例如 PhysicsComponent 的 Transform 可以绑到 ModelComponent 的 Transform，中间不需要任何硬引用。文中给的"玩家走路播放脚步声"的例子串起了 PlayerStateComponent、TimerComponent、SoundComponent、PositionComponent 四个组件，所有依赖全在 factory 里显式声明，组件自身完全解耦。Todd 明确提到想避免反射，所以这是个手写的强类型绑定系统。

## 关键要点

- 组件之间的硬引用是"换了层皮的 OOP"
- 把属性当成 I/O 端口、在 factory 里连线，实现 dataflow 式的组件组合
- 支持多输入组合、closure 做投影、action 作为端口类型
- 与今天 Unity DOTS 的 ECS 在哲学上不同：前者是 "entity 内部的数据流图"，后者是 "全局 System 查询 SoA"
- Todd 想"尽量不用反射"——是个编译期/强类型方案

## 链接到的概念

- [[component-entity-data-binding]]
- [[ecs]]
- [[dependencies]]
- [[classitis-in-games]]

## 原文

- 链接：https://etodd.io/2011/02/02/refactoring-with-components/
- 本地：`raw/articles/etodd.io/2011-02-02_refactoring-with-components.md`
