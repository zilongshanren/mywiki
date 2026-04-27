---
tags: [source, game-development, procedural-generation, graph-algorithms, traversability]
date: 2026-04-27
sources: 1
---

# Fast Traversal Queries of Procedurally Generated Rooms（Boris The Brave）

[[people/boris-the-brave]] 发表于 2017 年 7 月的文章，讨论如何在程序化生成关卡中**高效判断放置障碍物后路径是否仍然连通**。

## 摘要

关卡生成中常见需求：随机放置障碍物的同时，保证入口与出口始终可达。朴素做法是每次放置后做一次洪泛（flood fill）——但对大地图、多候选位置来说开销极高。Boris 提出以**持久化不相交集（Persistent Disjoint-Set）**为核心的预计算方案：将地图按列预切成扫描条带（slice），分别向左/向右预计算好连通信息；测试某个位置时，只需合并障碍物左右两侧已有的连通状态，再对障碍物所占的小列做增量合并，最后检查入口/出口是否同集即可。大量候选位置只需做一次预计算，单次查询的代价从 O(N) 降到接近 O(1)。

## 关键要点

- **不相交集（Union-Find）** 比洪泛更灵活：可以按任意顺序合并，便于按列预计算并复用结果
- **持久化数据结构**让多个扫描条带对象共享已处理的重叠数据，内存开销极低
- 算法的核心思路：将地图分为"障碍物之外"（预计算完毕）和"障碍物附近的小列"（实时合并）两部分
- 可扩展到任意形状的障碍物，只需找到对应的左右边界条带即可

## 链接到的概念

- [[game-development/traversability-checking]]
- [[game-development/dungeon-generation-algorithm]]
- [[game-development/procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2017/07/08/fast-traversal-queries-of-procedurally-generated-rooms/
- 本地：`raw/articles/boristhebrave.com/2017-07-08_fast-traversal-queries-of-procedurally-generated-rooms.md`
