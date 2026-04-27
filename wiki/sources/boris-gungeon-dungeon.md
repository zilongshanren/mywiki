---
tags: [source, procedural-generation, dungeon-generation, game-development, roguelike]
date: 2026-04-27
sources: 1
---

# Dungeon Generation in Enter The Gungeon（Boris The Brave / BorisTheBrave.Com）

[[people/boris-the-brave]] 发表于 2019 年 7 月的逆向工程分析，揭示 Enter The Gungeon 关卡生成的图结构 + 布局两阶段方案。

## 摘要

Gungeon 关卡生成的核心洞见是**先在图结构（Graph）层面定好节奏，再做空间布局**。每个关卡从一组预设的 Flow 文件之一开始，Flow 是有向图，节点是房间类型（普通战斗/商店/奖励/Boss），边是连接关系，已明确指定哪里有单向通道和循环路径。Flow 经过节点注入（Injection）增删可选房间后，分解为若干 Composite（循环子图 + 树形子图），每个 Composite 独立做空间布局，最后拼装为完整地图。循环 Composite 的布局算法从两端交替延伸，末端用寻路补一段走廊闭合。这一设计保证了"Boss 房离入口合理距离""单向奖励循环""战斗与休息节奏"等人工设计意图被自动保留，同时给随机性留出足够空间。

## 关键要点

- Flow 文件（预设有向图）= 人工设计意图的载体，随机性在此之下才发生
- 节点注入（Injection）：条件触发的房间插入，秘密房/监狱/特殊活动等均用此机制
- Composite 拆分：最小循环优先切出，确保循环布局先于线性布局
- 循环布局从两端交替延伸，末段寻路闭合：兼顾紧凑性与连通性
- 与 Diablo 1 的共同启示：先抽象图/预地牢，后具体空间，是关卡生成的有效范式

## 链接到的概念

- [[dungeon-generation-algorithm]]
- [[a-star-pathfinding]]

## 原文

- 链接：https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/
- 本地：`raw/articles/boristhebrave.com/2019-07-28_dungeon-generation-in-enter-the-gungeon.md`
