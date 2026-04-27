---
tags: [source, 程序化生成, 空间索引, 分形坐标, 无限网格]
date: 2026-04-27
sources: 1
---

# Infinite Quadtrees – Fractal Coordinates（Boris The Brave）

[[boris-the-brave]] 发表于 2023 年 1 月的技术文章，介绍 Peter Mawhorter 论文中"分形坐标"（Fractal Coordinates）的思路及其在无限程序化生成中的应用。

## 摘要

标准四叉树必须预先确定根节点的边界，无法自然扩展到无限平面。Boris 介绍了 Mawhorter 的解法：把四叉树重新理解为覆盖全平面的**多级格网集合**——第 0 级是 1×1 的标准方格，第 1 级是 2×2，第 h 级是 2^h × 2^h，每块用 `(h, x, y)` 三元组唯一标识，称为"分形坐标"。由于任意级格网都能无限延伸，空间不再需要边界。更重要的改进是**交替坐标系**：按偶/奇级别交替地把子节点放在父节点的右上/左下，使得对任意有限区域都能找到一个单一的包含正方形（无论区域有多大），且相邻格子总能在有限级别找到共同祖先。这一性质极大简化了形状存储和空间查询。文章还介绍了 Mawhorter 用该坐标系设计无限迷宫的方法：迷宫线条只靠近格子边缘，所以有限区域只需有限多个大格子的贡献，整体迷宫仍能保证任意两点连通。

## 关键要点

- 分形坐标 `(h, x, y)`：级别 h 决定格子尺寸 `2^h`，x/y 决定位置
- 交替系统：偶数级用右移，奇数级用左移，保证任意有限矩形有唯一包含正方形
- 对比普通四叉树：不用预定根边界，形状不重复存储，查询更简单
- 应用：zoomable 地图存储、无限迷宫生成、[[game-development/substitution-tilings]] 中的惰性树基础
- 实验性应用：Boris 将此思路用于 Box2D 扩展（超大地形）以及后来的替换铺砖惰性树

## 链接到的概念

- [[game-development/infinite-quadtrees-fractal-coords]]
- [[game-development/substitution-tilings]]
- [[game-development/infinite-random-rhombus-tilings]]

## 原文

- 链接：https://www.boristhebrave.com/2023/01/28/infinite-quadtrees-fractal-coordinates/
- 本地：`raw/articles/boristhebrave.com/2023-01-28_infinite-quadtrees-fractal-coordinates.md`
