---
tags: [source, 程序化生成, 随机路径, 关节点, chiseling]
date: 2026-04-27
sources: 1
---

# Random Paths via Chiseling（Boris The Brave）

[[boris-the-brave]] 发表于 2018 年 4 月的文章，提出比 [[sources/boris-random-path-algorithm]] 更高效、更通用的随机路径生成算法，命名为"chiseling"（凿刻法）。

## 摘要

原先的算法从空房间填充格子直到不可继续，等效于找路径的补集，效率较低。本文提出反向思路：**从完整填充区域开始，逐一移除格子，直到只剩一条细路径**。被移除的格子不能是关节点（articulation point / cut-vertex），即不能是删掉后导致路径两端不连通的节点。Boris 使用基于 DFS 的快速关节点算法，并做了改进：只关注"分离端点"的关节点，而非任何使区域一分为二的关节点。重复该操作直到没有可移除格子（或提前停止以获得更胖路径）。算法适用于任何图结构，通过调整每个格子的选择概率可以引导路径形状。还支持固定端点数不限、无端点随机漫步等变体。

## 关键要点

- 核心步骤：随机选一个非关节点格子 → 移除 → 重复
- 关节点检测：基于 DFS 的 O(V+E) 算法，改造为只检测"端点分离"型关节点
- 算法适用于任意图，不限于网格（flexible graph support）
- 格子选择概率可调，控制路径偏好（例如偏靠墙壁或偏向中央）
- 支持多端点连接（路径需连通所有端点）
- 提前终止可生成较宽的通道而非极细路径
- Boris 注明 2022 年发现了更好的改进版（Chiseled Paths Revisited）

## 链接到的概念

- [[game-development/chiseling-random-paths]]
- [[game-development/dungeon-generation-algorithm]]

## 原文

- 链接：https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/
- 本地：`raw/articles/boristhebrave.com/2018-04-28_random-paths-via-chiseling.md`
