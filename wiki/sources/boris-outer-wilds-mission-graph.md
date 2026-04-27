---
tags: [source, game-development, mission-graph, level-design, game-analysis]
date: 2026-04-27
sources: 1
---

# Outer Wilds Mission Graph（Boris The Brave）

[[people/boris-the-brave]] 发表于 2025 年 2 月的短文，用任务图分析法解剖《星际拓荒（Outer Wilds）》的叙事结构，量化「关键路径」上的真正必要节点。

## 摘要

Boris 在通关《星际拓荒》后，对游戏关键路径的稀疏程度感到惊讶——大多数地点提供的是背景叙事和好奇心驱动，而非推进进度的必要线索。为了量化这一印象，他绘制了全游戏的任务图：节点为游戏中的各主要地点/事件，有向边代表「A 提供了到达 B 所必需的信息」。分析结果显示，不足一半的地点真正出现在关键路径上。Ember Twin 的线索密度最高；Timber Hearth 和 Giant's Deep 几乎没有必要线索——Boris 认为这是刻意为之：作为起始星球和玩家视野内最显眼的星球，开发者知道玩家无论如何都会探索这两处。这个案例展示了任务图作为分析工具的威力：同一套设计可同时实现「关键路径极短（最后收尾必须一气呵成）」和「自由探索空间极大」，前者保证流程紧凑，后者提供发现的乐趣。

## 关键要点

- 全游戏任务图：不足半数地点处于关键路径上
- Ember Twin 线索密度最高；Timber Hearth / Giant's Deep 的必要线索极少
- 开发者刻意把「玩家必然会去的地方」从关键路径上解放出来，集中放自由探索内容
- 关键路径极短是有意设计：最终序列需要一气呵成，短路径降低记忆负担
- 任务图分析可有效量化「表面复杂」与「实际线性」之间的差距

## 链接到的概念

- [[game-development/mission-graph]]

## 原文

- 链接：https://www.boristhebrave.com/2025/02/25/outer-wilds-mission-graph/
- 本地：`raw/articles/boristhebrave.com/2025-02-25_outer-wilds-mission-graph.md`
