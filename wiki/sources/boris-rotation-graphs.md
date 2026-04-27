---
tags: [source, game-development, graph, geometry, topology, mesh]
date: 2026-04-27
sources: 1
---

# Rotation Graphs（Boris The Brave）

[[people/boris-the-brave]] 发表于 2022 年 7 月的文章，介绍旋转图这一带方向感知的图数据结构，及其在游戏和几何处理中的应用。

## 摘要

旋转图在普通图的基础上为每个节点的出边添加顺序编号（0 到 d-1），从而引入"左转"和"右转"的概念，而无需任何坐标信息。文章通过旋转映射（rotation map）形式化了这一结构，并展示了三类典型应用：3D 网格的面拓扑表示（不依赖几何即可描述曲面运动）、游戏中房间到房间的跳转关系、以及双曲游戏 HyperRogue 的导航系统。Boris 在自己的 Celtic Knot Blender 插件和 Tessera WFC 扩展中都以旋转图为核心数据结构。文章还指出旋转图可视为半边数据结构（DCEL）的轻量近似。

## 关键要点

- 旋转图 = 普通图 + 出边有序编号（每个节点 0..d-1）
- 旋转映射：rotate(A, i) = (B, j)，j 是从 B 回到 A 的标签
- "坦克控制"导航：前进、左转、右转均无需坐标，只操作节点和标签
- 3D 网格面间转场时的旋转量可直接从边标签差读出
- 绕顶点环绕：反复"前进+顺时针一步"会回到起点，可用于重建对偶网格
- 限制：仅适用于可定向曲面；不可定向面需额外镜像标志位

## 链接到的概念

- [[game-development/rotation-graphs]]
- [[game-development/wave-function-collapse]]

## 原文

- 链接：https://www.boristhebrave.com/2022/07/31/rotation-graphs/
- 本地：`raw/articles/boristhebrave.com/2022-07-31_rotation-graphs.md`
