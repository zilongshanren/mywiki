---
tags: [source, game-development, procedural-generation, dungeon-generation, roguelite]
date: 2026-04-27
sources: 1
---

# Dungeon Generation in Binding of Isaac（Boris The Brave）

[[people/boris-the-brave]] 发表于 2020 年 9 月的文章，通过反编译原版 Flash 代码，还原了《以撒的结合》地牢生成算法的真实实现细节。

## 摘要

《以撒的结合》在 9×8 网格上生成地牢。核心流程分为三步：首先用**广度优先扩展**（BFS）在网格中放置房间——从中心出发，以 50% 概率向相邻格扩展，并拒绝已有两个以上邻居的格，确保生成树状（无环）结构；然后指定特殊房间（Boss 房永远在最远的死端，密室优先贴近三个以上已有房间的格）；最后从分级房间池（简单/中等/困难）随机选取房间内容。Rebirth 的贡献是引入 2×2、L 形等大型房间，通过修改"遍历出口而非方向"的循环方式实现。Boris 认为此算法以极少的代码实现了极好的效果，"floorplan 与内容分离"是关键设计原则。

## 关键要点

- 网格坐标编码技巧：行列合并为两位数（十位=y，个位=x），方向移动 ±10/±1
- BFS 扩展 + 邻居数量限制 = 自动产生树形无环结构
- Boss 房：取距起始最远的死端；密室：贴近≥3 个已有房间的格
- 大型房间（Rebirth）：遍历房间出口而非四方向，允许局部形成环
- 地牢布局与房间内容完全解耦，是可扩展的关键

## 链接到的概念

- [[game-development/procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/
- 本地：`raw/articles/boristhebrave.com/2020-09-12_dungeon-generation-in-binding-of-isaac.md`
