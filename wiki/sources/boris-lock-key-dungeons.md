---
tags: [source, game-development, level-design, procedural-generation, mission-graph]
date: 2026-04-27
sources: 1
---

# Lock and Key Dungeons（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 2 月的文章，系统分析"锁与钥匙"关卡设计模式及其分析工具。

## 摘要

"锁与钥匙"并不限于物理对象，而是泛指任何阻断玩家进度（锁）与解锁进度（钥匙）的游戏元素——道具、升级、密码、事件标志都属此类。文章区分硬性/软性要求（hard/soft lock），并引入**任务图（Mission Graph）**作为分析工具：将关卡中所有锁/钥匙关系抽象为有向图，忽略物理布局细节，仅保留逻辑依赖关系。任务图能快速揭示关卡的真实线性程度——许多表面复杂的迷宫实际上是严格线性的。文章还区分了任务图与流程图（Flow Chart）的适用场景，并指出 Mark Brown 的 Boss Keys 图是融合物理连接与锁钥关系的优秀可视化工具。最后指出任务图同样是程序化关卡生成的设计基础，为后续 Unexplored 分析埋下伏笔。

## 关键要点

- 锁钥模式无处不在：Zelda 道具、Metroidvania 升级、密码、事件标志均是变体
- 硬性锁：必须按设计路径解锁；软性锁：可绕过，速通社区偏爱
- 任务图（Mission Graph）= 依赖关系有向图，是关卡复杂度分析的核心工具
- 任务图可从游戏中提炼（分析），也可先画图再设计关卡（生成）
- 与物理地图叠加可同时看到探索量和逻辑路径

## 链接到的概念

- [[game-development/mission-graph]]
- [[game-development/procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/
- 本地：`raw/articles/boristhebrave.com/2021-02-27_lock-and-key-dungeons.md`
