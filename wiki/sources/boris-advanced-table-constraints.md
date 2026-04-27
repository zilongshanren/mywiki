---
tags: [source, constraint-solving, algorithms, game-development, wfc]
date: 2026-04-27
sources: 1
---

# Advanced Table Constraints（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 8 月的文章，系统梳理 [[game-development/arc-consistency]] 算法家族之外的广义弧相容（Generalized Arc Consistency，GAC）算法前沿进展。

## 摘要

文章以 AC-5 通用框架为切入点，介绍了从 AC-3/AC-4 演进到 GAC2001、GAC3rm、STR2、STR3、MDDc 等一系列表约束算法的核心思路。核心议题是多变量约束（而非仅限于二元弧）的高效处理：算法按粗粒度/细粒度（coarse/fine）以及是否使用动态表、索引、压缩分类，并讨论了回溯场景下可逆数据结构（Sparse Set、trailing）的设计取舍。作者最终坦言此领域文献分散且术语混乱，并指出自己的 DeBroglie 库在回顾后存在一些设计决策遗憾，STR3 是最值得集成的新算法。

## 关键要点

- AC-5 是框架而非具体算法，通过替换 `Initialize`、`ArcCons`、`LocalArcCons` 三个抽象操作可派生 AC-3/AC-4 等算法
- 粗粒度算法每次重扫全部值，细粒度算法利用"被删除的具体值"信息增量更新，二者各有优劣
- 回溯场景需要**可逆数据结构**：Sparse Set 用数组+大小指针实现 O(1) 删除与 O(1) 回溯，无需复制
- STR2 将 Sparse Set 引入表约束，动态淘汰失效元组；STR3 进一步结合 AC6 样式的"最小有效元组"与 watched literals，达到路径最优过滤
- MDD（多值决策图）是另一条压缩路线，以合并子树的 trie 存储约束

## 链接到的概念

- [[game-development/arc-consistency]]
- [[game-development/advanced-table-constraints]]
- [[game-development/constraint-based-tile-generators]]
- [[game-development/debroglie-wfc-library]]

## 原文

- 链接：https://www.boristhebrave.com/2021/08/30/advanced-table-constraints/
- 本地：`raw/articles/boristhebrave.com/2021-08-30_advanced-table-constraints.md`
