---
tags: [procedural-generation, game-development, dungeon-generation, algorithm, bsp]
date: 2026-04-27
sources: 1
---

# 递归细分（Recursive Subdivision / BSP）

递归细分又称**二叉空间划分（Binary Space Partitioning, BSP）**，是程序化生成领域最经典的算法之一：从一个大矩形出发，每次随机选择水平或垂直方向将其一分为二，递归重复，最终得到一棵嵌套矩形的划分树。

常见应用场景包括城市路网生成、[[dungeon-generation-algorithm|Roguelike 地牢]]（每个叶节点放一个房间，节点间连走廊），以及 Treemapping 数据可视化。

## 基础变体的局限

朴素实现只产生矩形，并且有两个明显"破绽"：

1. 最早的划分横跨整个区域，视觉上显眼；
2. 所有分割线均为直线，缺乏有机感。

## 常见改进方案

### 多边形化

将起始形状从矩形换为**任意凸多边形**，每次切割产生两个更小的凸多边形。凸性保证每次切割后的子区域仍然可以继续递归切割，消除矩形带来的规律感。

### 弯折切割（Bent Subdivision）

Oleg Dolya（奥列格·多利亚，Townscaper 作者）提出在每条切割线上增加**一个弯折（kink）**，既打破长直线的视觉突兀，又允许切割线以垂直方式接触边界，模拟真实街道的不规则走向。

### 随机游走切割

Jamis Buck 展示了用**随机细胞增长**替代直线切割的方式，生成更自然的迷宫分割。分割路径本身就是随机路径，而非预设的直线，形成更有机的边界。

### 十字形切割（Diablo 式）

[[boris-diablo1-dungeon|Diablo 1]] 的地下室关卡采用了一种固定模式：先将区域分为一个中央方块和四个环绕区域，共 5 份。优点是：切割线不会太长，中央区域与外围区域的不对称性天然产生密度梯度（中心更密集），接近真实城市/地牢的感觉。

### 网格细分（Grid Subdivision）

Pokemon Mystery Dungeon 采用均匀网格划分，但赋予每个格子不同的处理规则：完全空旷、仅有走廊穿过、或随机合并相邻格子，从而在规整结构上制造变化。

### 不均等深度（Variable Depth）

递归时不强制所有分支到达相同深度，允许部分区域保持更大，产生非均匀密度感。

## 相关

- [[dungeon-generation-algorithm]] — Roguelike 地牢生成的宏观综述
- [[procedural-dungeon-generation]] — 更广泛的程序化地牢生成技术
- [[wave-function-collapse]] — 另一类约束式程序化生成方案

## Sources

- [[sources/boris-recursive-subdivision]]
