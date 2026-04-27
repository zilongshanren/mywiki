---
tags: [source, 程序化生成, 铺砖, 非周期铺砖, sylves]
date: 2026-04-27
sources: 1
---

# Substitution Tilings（Boris The Brave）

[[boris-the-brave]] 发表于 2024 年 11 月的技术文章，介绍他为 Sylves 库实现替换铺砖（substitution tilings）的工程方案。

## 摘要

替换铺砖是生成非周期铺砖（aperiodic tiling）的经典方法：从单块砖开始，交替执行"切分"（dissect）和"放大"（inflate）两步，最终铺满无限平面。经典例子包括 Penrose 菱形铺砖和椅子铺砖（chair tiling）。Boris 为了让它适合游戏中高效使用，引入了**惰性无限树**结构——砖块被组织成无限树形层级，每次 inflate 等于向上走一级，每次 dissect 等于向下展开子节点，这与他之前文章中的 [[infinite-quadtrees-fractal-coords]] 思路高度一致。任意砖块可用"从根到叶的路径"编码为单个整数，实现 O(log n) 的按坐标取砖（cell picking）和区域查询（range query）。区域查询使用"水龙头"（spigot）算法：沿树向上收集兄弟节点集合，再对每个节点做深优先子树搜索，最终覆盖整个查询区域而不遍历全树。

## 关键要点

- **替换规则**：不同铺砖类型的切分/放大规则不同，Penrose 菱形有两种砖（胖/细菱形），放大因子为黄金比 `(1+√5)/2`（无理数）
- **惰性树**：指数级增长的铺砖数量通过树结构按需展开，不需预先生成全部砖块
- **砖块编码**：路径以整数表示（如 4 叉树用 base-4 编码），作为砖块的唯一标识
- **Spigot 算法**：区域搜索核心，以对数步数定位候选子树再深优先展开，避免无界递归
- **方向修正**：朴素替换规则会导致单方向生长（出现"空白区域"），Boris 通过倍增替换规则轮流使用来保证四面向外扩展
- 当前实现大多数操作达到对数或常数（带缓存）时间复杂度；Sylves 的砖块输入工作仍需完善

## 链接到的概念

- [[game-development/substitution-tilings]]
- [[game-development/infinite-quadtrees-fractal-coords]]
- [[game-development/infinite-random-rhombus-tilings]]

## 原文

- 链接：https://www.boristhebrave.com/2024/11/30/substitution-tilings/
- 本地：`raw/articles/boristhebrave.com/2024-11-30_substitution-tilings.md`
