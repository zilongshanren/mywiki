---
tags: [source, 程序化生成, 随机路径, 地图生成]
date: 2026-04-27
sources: 1
---

# Random Path Algorithm（Boris The Brave）

[[boris-the-brave]] 发表于 2017 年 7 月的短文，介绍一种生成有机随机路径的简单算法。

## 摘要

这篇文章非常简短，是一个技术速写。Boris 发现在程序化房间生成技术的基础上可以直接用于路径生成：从空房间出发，随机往里填充格子，直到无法继续填充为止（即再填就会导致房间不连通）。剩余的未填充区域自然形成一条弯曲的路径。文章配有交互 Demo，支持设置锚点让路径必须经过特定位置。这一思路在 2018 年演变为更系统的"chiseling"算法（参见 [[sources/boris-random-paths-chiseling]]）。

## 关键要点

- 算法：从填满的格子开始，随机移除非关节点（articulation points）之外的格子
- 结果路径有机自然，弯曲而不规则
- 支持锚点约束：特定格子必须在路径上
- 是"chiseling"算法的前身

## 链接到的概念

- [[game-development/chiseling-random-paths]]

## 原文

- 链接：https://www.boristhebrave.com/2017/07/15/random-path-algorithm/
- 本地：`raw/articles/boristhebrave.com/2017-07-15_random-path-algorithm.md`
