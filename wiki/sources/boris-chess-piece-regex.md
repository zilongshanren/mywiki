---
tags: [source, 程序化生成, 棋盘游戏, 正则表达式, 图论]
date: 2026-04-27
sources: 1
---

# Defining Chess Piece Moves Using Regular Expressions（Boris The Brave）

[[people/boris-the-brave]] 发表于 2022 年 10 月的文章，探讨用正则表达式在旋转图路径上定义国际象棋棋子走法，使规则能够泛化到任意网格拓扑。

## 摘要

国际象棋棋子走法通常以笛卡尔坐标硬编码，一旦换成六边形或三角形棋盘便需完全重写。Boris 将棋盘抽象为[[game-development/rotation-graphs|旋转图]]，把棋子运动简化为三种基本操作：前进（F）、左转（L）、右转（R）。任意走法序列即为这三个字符构成的路径字符串，而一类走法（如车的横竖滑行）则对应一条正则表达式。车的走法写作 `/L*(F$)+/`，马的走法写作 `/L*FF(L|R)F$/`，主教两种斜走分支共同覆盖了不同网格拓扑的对角线变体。文章还讨论了如何用有限状态机枚举所有合法落点：将正则式转为 FSM 后做深度优先搜索，用 `(cell, direction, FSM state)` 三元组检测回路，避免无限循环。

## 关键要点

- 旋转图将棋盘拓扑与坐标系解耦，F/L/R 三字符足以表达任意网格上的有向移动
- 正则表达式描述的是一类路径集合（即正则语言），恰好对应一类棋子走法
- `$` 符号用于标注"检查当前格是否被占"的引擎钩子，处理阻挡与吃子
- 合法落点枚举通过将正则式化为 FSM + DFS 实现，以三元组状态避免无限路径
- 规则自动适用于六边形棋盘、三方棋盘等异形网格，象的斜线在六边形上会因路径方向不同而分裂

## 链接到的概念

- [[game-development/rotation-graphs]]
- [[game-development/chess-move-regex]]

## 原文

- 链接：https://www.boristhebrave.com/2022/10/22/defining-chess-piece-moves-using-regular-expressions/
- 本地：`raw/articles/boristhebrave.com/2022-10-22_defining-chess-piece-moves-using-regular-expressions.md`
