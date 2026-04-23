---
tags: [source, game-engines, flash, actionscript, 框架设计, 碰撞检测]
date: 2026-04-19
sources: 1
---

# Flashpunk — 框架代码评审（Marte / Random Tower）

[[people/marte-randomtower|Marte]] 发表于 2010 年 1 月的文章，对 ActionScript 3 游戏框架 FlashPunk（v0.73）的源代码做逐类评析，指出其架构优劣。

## 摘要

作者以有 AS3 开发经验的独立开发者视角审视 FlashPunk 的主要类：Core.as 将逻辑与渲染分离值得肯定，但绘制方法混入其中破坏职责单一性；Entity.as 提供了网格碰撞加速（Grid.as）和按类型筛选碰撞的良好设计，但将碰撞逻辑直接嵌入基础 Entity 类导致耦合；World.as 同时扮演容器和工具集，与 MVC 分离原则相悖；Actor.as 与 Acrobat.as 将变换能力直接继承在类树中而非组合注入；TileMap 与 Grid 可联动形成视觉+碰撞双层瓦片地图。文章同时批评框架缺少 release notes、正式 Bug Tracker 和调试控制台，认为这些工具支持是框架成熟的重要标志。作者总体判断 FlashPunk 有良好的出发点，文档和工具链是进一步突破的关键。

## 关键要点

- Core.as 更新/渲染分离符合 KISS 原则，但绘制方法混入污染职责
- Entity.as 碰撞系统：暴力遍历 + Grid 网格加速 + 类型标签分组，设计完整
- Collision Mask 支持表明框架作者有实际游戏开发经验
- World.as 职责混乱（容器 + 工具集），非 MVC 友好
- 缺少 release notes 和 Bug Tracker 是框架走向社区的障碍
- TileMap.as + Grid.as 可以联动，形成视觉与碰撞双层地图

## 链接到的概念

- [[game-engines/flashpunk-framework]]

## 原文

- 链接：https://randomtower.blogspot.com/2010/01/flashpunk-seems-to-be-jung-good.html
- 本地：`raw/articles/randomtower.blogspot.com/2010-01-13_flashpunk.md`
