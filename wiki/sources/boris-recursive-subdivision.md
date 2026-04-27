---
tags: [source, game-development, procedural-generation, dungeon-generation, bsp]
date: 2026-04-27
sources: 1
---

# Recursive Subdivision Variants（Boris The Brave）

[[boris-the-brave]] 发表于 2021 年 8 月的文章，系统梳理递归细分（Binary Space Partitioning）用于程序化生成的各种改进变体。

## 摘要

递归细分是程序化生成的经典技术：从矩形出发，递归地二分，产生嵌套矩形树，可用于城市路网、迷宫、[[dungeon-generation-algorithm|Roguelike 地牢]]和 Treemapping。文章列举了若干克服朴素实现局限性（只产生矩形、早期分割线过长过显眼）的变体：

- **多边形化**：以凸多边形替代矩形，消除矩形感。
- **弯折切割**：Oleg Dolya 在切割线上加入一个弯折，使长切割线变得不规则，符合有机感城市布局。
- **随机游走切割**：Jamis Buck 用随机细胞增长替代直线切割，适合迷宫中需要避免"瓶颈"的场景。
- **十字形切割（Diablo 式）**：一个中央方块加四角，5 个区域；切割线短，中心密度高，非常自然。
- **网格细分**：Pokemon Mystery Dungeon 方式，均匀网格但每格规则不同（空/走廊/合并）。
- **不均等深度**：不强制递归到相同深度，允许部分区域保留更大空间。

## 关键要点

- 朴素递归细分的两个"破绽"：只有矩形，最早的切割线横跨全区域
- 弯折切割和随机游走是解决"破绽二"最实用的方案
- Diablo 式十字切割简单高效，且自然产生"中心密集、边缘稀疏"的密度梯度
- 不均等深度可引入大小房间的对比感
- 四边形/多边形系统的等价物是 Voronoi 分区

## 链接到的概念

- [[recursive-subdivision]]
- [[dungeon-generation-algorithm]]
- [[procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2021/08/14/recursive-subdivision-variants/
- 本地：`raw/articles/boristhebrave.com/2021-08-14_recursive-subdivision-variants.md`
