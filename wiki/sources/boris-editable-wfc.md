---
tags: [source, procedural-generation, wfc, autotile, game-development]
date: 2026-04-27
sources: 1
---

# Editable WFC（Boris The Brave / BorisTheBrave.Com）

[[people/boris-the-brave]] 发表于 2022 年 4 月的文章，提出将 WFC 用作可交互地图编辑工具的技术方案。

## 摘要

Editable WFC 结合了 Autotile（用户主导编辑）与 WFC（约束自动修正）的优点：用户单击放置一块瓦片，算法自动传播约束并最小化对已有地图的改动。核心机制有三层：一是**脏格启发式**（Dirty Cell Heuristic）——只重新解算受影响的格子而非全图；二是**相似度启发式**（Similarity Heuristic）——选择与旧瓦片最接近的替代品来保留地图现有内容；三是**提前终止**——当脏格清零时立即停止，剩余格子直接复制旧地图。文章以 Townscaper 为参照，指出后者用"隐藏驱动层 + 确定性选择"的简化路线，而本文方案更通用但复杂；并给出了在 DeBroglie 库中配置 `Dirty` 选格器和 `ArrayPriority` 权重集的具体 API 说明。

## 关键要点

- 脏格启发式：约束扩散时标记需要重解的格子，避免全图重跑
- 相似度权重集：优先保留原有瓦片，次选邻接相似瓦片
- 提前终止：脏格为零即结束，大量格子可直接复用
- Townscaper 对比：确定性+隐藏驱动层 vs. 直接编辑瓦片层（更通用）
- 懒初始化数据结构：避免在大地图上为未触及格子付出初始化代价

## 链接到的概念

- [[wave-function-collapse]]
- [[autotile-tileset-layouts]]

## 原文

- 链接：https://www.boristhebrave.com/2022/04/25/editable-wfc/
- 本地：`raw/articles/boristhebrave.com/2022-04-25_editable-wfc.md`
