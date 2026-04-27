---
tags: [source, game-development, procedural-generation, dungeon-generation, graph-rewriting]
date: 2026-04-27
sources: 1
---

# Dungeon Generation in Unexplored（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 4 月的深度分析，解构 2017 年游戏《Unexplored》的程序化关卡生成系统——基于图重写的循环地牢生成器。

## 摘要

《Unexplored》的关卡生成系统由 Joris Dormans 设计，核心创新是**循环地牢生成（Cyclic Dungeon Generation）**：先在 5×5 网格上画一个大环（起始→目标），将环分为两段弧线，再从 24 种预定义"主循环类型"中选一种来规定这两段弧线的叙事结构（双路、单钥、Hub 等），然后逐步添加次级环和死端，最后将图节点扩展为实际瓦片地图。整个流程分三大阶段：**抽象布局**（图结构）→**内容决议**（biome/主题驱动的渐进细化，从抽象"障碍物"到具体敌人）→**图转瓦片**（格分辨率扩展 2×→5×，再用图重写规则绘制房间/走廊/地形）。"先抽象后具化"和"biome 驱动一致性"是贯穿全系统的设计原则。整套系统约 5000 条图重写规则，由 Ludoscope 工具支撑，单人开发可行。

## 关键要点

- 循环结构天然支持有意义的进度感和双路叙事，比树形结构更丰富
- 非终结符（Non-terminal symbol）：抽象占位节点延迟具体化，中间规则无需关心细节
- Biome/主题标注：早期决定大方向，后续规则按标注条件启用/禁用内容，保证关卡一致性
- 图→瓦片：两次分辨率翻倍 + 各节点类型专用规则，细化从粗到精
- 约 5000 条规则中大量是手工设计的特例，多样性来自规模而非魔法算法

## 链接到的概念

- [[game-development/procedural-dungeon-generation]]
- [[game-development/mission-graph]]

## 原文

- 链接：https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/
- 本地：`raw/articles/boristhebrave.com/2021-04-10_dungeon-generation-in-unexplored.md`
