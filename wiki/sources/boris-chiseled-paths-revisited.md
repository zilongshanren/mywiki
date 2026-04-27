---
tags: [source, game-development, procedural-generation, pathfinding, random-paths, graph-algorithms]
date: 2026-04-27
sources: 1
---

# Chiseled Paths Revisited（Boris The Brave）

[[people/boris-the-brave]] 发表于 2022 年 3 月的文章，是凿刻法随机路径算法的第三次迭代，找到了兼顾**快速**与**实现简单**的方案。

## 摘要

凿刻法（Chiseling）在 2017 年提出、2018 年优化，但两个版本都在性能或实现复杂度上存在不足。本文提出核心改进：引入**见证路径（witness）**——一条已知可通的路径，在每轮迭代中充当"跳过关节点检测"的快捷条件。若随机选中的格子不在 witness 上，可直接移除，无需任何连通性检测；只有选中 witness 上的格子时才重新寻路。由于大多数时候选中的格子不在 witness 上，关节点检测的调用频率大幅降低，算法效率显著提升且代码量极小。

## 关键要点

- **见证路径优化**：维护一条已知通路；非 witness 格子可无条件移除，节省大量寻路开销
- **终止条件**：所有格子最终被标记为 Blocked 或 Forced（关节点），没有 Open 格子即终止
- **见证路径不影响分布**：可用任意寻路算法（Dijkstra、A*、BFS 均可），最终路径分布不变
- **可调弯曲度**：让 find_path 随机选取最短路径，并给 witness 上的格子赋予权重 w，w=0 得最短路，w>1 得更弯曲的路径
- **多端点扩展**：find_path 返回连通所有端点的路径集合即可，无需改动主循环结构

## 链接到的概念

- [[game-development/chiseling-random-paths]]
- [[a-star-pathfinding]]
- [[game-development/dungeon-generation-algorithm]]

## 原文

- 链接：https://www.boristhebrave.com/2022/03/20/chiseled-paths-revisited/
- 本地：`raw/articles/boristhebrave.com/2022-03-20_chiseled-paths-revisited.md`
