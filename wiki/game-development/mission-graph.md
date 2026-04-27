---
tags: [game-development, level-design, procedural-generation, lock-and-key, mission-graph]
date: 2026-04-27
sources: 2
---

# 任务图（Mission Graph）

任务图是关卡设计分析与生成的核心抽象工具。它将游戏关卡中所有**锁与钥匙**的依赖关系抽象为有向图——"如果 A 是 B 的前提条件，则画一条从 A 到 B 的箭头"——并完全忽略物理布局细节。

## 锁与钥匙的广义定义

"锁"泛指阻断玩家进度的任何元素，"钥匙"泛指解锁进度的任何元素，不必是物理对象：
- **道具**（Zelda 炸弹、钩爪）
- **升级**（Metroidvania 双跳）
- **密码/对话选项**
- **事件标志**（隐藏变量触发的状态变化）
- **软性门（Beef Gate）**：高难怪物阻路，技术高超的玩家可绕过

## 任务图的用途

**分析（从游戏到图）**：将已有关卡提炼为任务图，可直观看出真实的选择空间。许多表面复杂的迷宫，任务图一画，发现实际是严格线性的。

**设计（从图到游戏）**：先画任务图草图，确定高层次流程和节点依赖，再填充具体房间和内容。修改依赖关系在图上极为廉价，比改完整关卡容易得多。

**生成（程序化）**：[[procedural-dungeon-generation]] 中，先生成任务图（抽象逻辑结构），再将图节点映射到物理空间，是"先抽象后具化"原则的典型应用。《Unexplored》的循环地牢生成本质上就是在操作任务图。

## 相关可视化工具

Mark Brown 的 **Boss Keys** 图在任务图基础上叠加了物理连通信息，能同时展示逻辑依赖和实际探索/回溯路径，是该领域最佳可视化之一。

## 相关

- [[procedural-dungeon-generation]] — 程序化关卡生成如何利用任务图
- [[sources/boris-lock-key-dungeons]]
- [[sources/boris-unexplored-dungeon]]
- [[sources/boris-outer-wilds-mission-graph]] — 《星际拓荒》任务图实例分析：不足半数地点在关键路径上

## Sources

- [[sources/boris-lock-key-dungeons]]
- [[sources/boris-unexplored-dungeon]]
- [[sources/boris-outer-wilds-mission-graph]]
