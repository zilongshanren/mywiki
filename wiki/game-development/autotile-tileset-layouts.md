---
tags: [procedural-generation, tileset, autotile, 2d]
date: 2026-04-19
sources: 1
---

# Autotile 切片布局：Marching Squares / Blob / Sub-blob / Micro-blob

Autotile 指玩家只刷「实/空」语义，程序根据邻域自动挑选正确贴图的一类 2D 地图生成技术。核心问题是：**需要多少张切片，才能覆盖所有可能出现的邻接情形**。不同方案在切片数量、表达力、美术工作量三者之间取不同的折中。

## Marching Squares（16 片）

以每个格点的四角是否为实体，取 0/1 拼 4 位二进制索引：

```
tile_index = topLeft + 2*topRight + 4*bottomLeft + 8*bottomRight
```

艺术家只需画 16 张切片，程序用简单查表。缺点是标记的是「角」而非「格子」，刷起来不直观；且 16 种形状很快就视觉疲劳。Tiled、tIDE 的默认 terrain tool 走这条路。

## Blob（47 实心 + 1 空 = 48 片）

直接枚举 8 邻域状态：上、下、左、右、四角共 8 位，理论上 256 种。但角邻居仅当两条相邻边都实心时才对切片形状有贡献，否则被边邻居吸收——所以实际唯一组合只有 47 个。Blob 给出比 Marching Squares 显著更丰富的边界变化，代价是艺术家要画 48 张、程序要维护 256→47 的查表。

## Sub-blob（20 子片 + 空）

观察每片的四个象限独立取值，发现单象限只有 5 种可能：**内弧、外弧、水平分割、竖直分割、实心**。于是每片可以由 4 个子象限组合拼装。20 子片即可覆盖全部 48 张 Blob 切片，美术量降到四分之一。RPG Maker VX 的 TileA2 走的就是这条路（「autotile」的事实标准含义）。代价是子象限之间的图案不一定严丝合缝，偶尔出现小的纹理接缝。

## Micro-blob（13 子片 + 空）

Boris 本人的命名。在 Sub-blob 的基础上进一步去掉可重用子片的冗余，最终只剩 13 + 1 = 14 张，比 Marching Squares 还少，但仍保留 Blob 级别的邻域表达力。代价是艺术家完全没法给不同象限定制差异花纹。截至原文 2013 年，作者不清楚有谁实际用这一布局。

## 如何选

- 强调工期短、切片少 → Marching Squares 或 Micro-blob
- 强调视觉丰富度、可以画更多 → Blob 或 Sub-blob
- 涉及多材质过渡、随机替代片、旋转 → 以上都只是基线，需在此之上做扩展

本文显式排除了旋转、多材质、随机替代的讨论，实际项目往往在 Blob/Sub-blob 之上叠一层 stamp/variant 系统。

## Sources

- [[sources/boristhebrave-tileset-roundup]]
