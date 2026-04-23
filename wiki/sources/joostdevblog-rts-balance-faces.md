---
tags: [source, game-development, 游戏设计, 平衡性, rts]
date: 2026-04-19
sources: 1
---

# The many faces of balance in an RTS（Joost van Dongen，2011-01-13）

[[joost-van-dongen]] 2011 年 1 月发的文章，总结 Swords & Soldiers 开发过程里他从专职平衡组（Olivier、Jasper、Fabian、Tom）身上学到的「RTS 平衡不是一种而是七种」。

## 摘要

平衡组多次向他解释：大众说的「faction balance」只是冰山一角，RTS 里至少还要兼顾新手平衡、阵营内战术平衡、地图平衡、早晚期节奏平衡、趣味平衡、运气平衡。Ronimo 的工程实践包括：**故意不做新手平衡**（维京入门最易但精通最难，是艺术决策而非 bug）、**只针对一张代表性地图做严格平衡**（medium 1），**联机只上线经过验证的 4 张图**；同时承认一点点运气是对败者的心理补偿（Mario Kart 现象），完全移除并不合适。文章是一张 checklist，用来提醒：改一个数会同时扰动所有七维，完美解不存在。他预告下一个项目（后来是 Awesomenauts）平衡复杂度远高于 Swords & Soldiers，不确定能否 hold 住。

## 关键要点

- 「阵营平衡」只是七种平衡之一，剩下六种同等重要。
- 精通难度和入门难度可以（也应该）不一致。
- 多图平衡成本极高，实用做法是**只针对一张图严肃平衡**，其余图作风味。
- 纯运气带来的阵营平衡是**假平衡**（50%-50% 但全靠开局猜拳）。
- 强度高不等于好——要求「操作成功后玩家自觉做了件牛事」的战术才是真的好战术。

## 链接到的概念

- [[rts-balance-taxonomy]]
- [[determinism-vs-smart-ai-gameplay]]
- [[planning-over-rng-game-design]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/01/many-faces-of-balance-in-rts.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-01-13_the-many-faces-of-balance-in-an-rts.md`
