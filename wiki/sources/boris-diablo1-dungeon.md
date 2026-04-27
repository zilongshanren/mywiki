---
tags: [source, procedural-generation, dungeon-generation, game-development, diablo]
date: 2026-04-27
sources: 1
---

# Dungeon Generation in Diablo 1（Boris The Brave / BorisTheBrave.Com）

[[people/boris-the-brave]] 发表于 2019 年 7 月的逆向工程分析，通过 Devilution 项目还原 Diablo 1 的关卡生成算法。

## 摘要

Diablo 1 的四个章节（教堂/地穴/洞窟/地狱）各有独立的生成器，但共享若干基础设施：40×40 预地牢（Predungeon，纯可行走性 bool 数组）→ 瓦片化（Marching Squares 或自定义模式匹配）→ Miniset/Fixup/主题房间/楼梯修缮。预地牢阶段与视觉无关，只关心"哪里可走"，极大降低了设计复杂度。教堂用递归"萌芽"（Recursive Budding，L5roomGen）向两轴交替延伸矩形房间；地穴用递归细分（Recursive Subdivision，CreateRoom）生成孤立房间再连走廊；洞窟用小块随机边缘扩展配侵蚀（erosion）生成有机轮廓；地狱在教堂算法基础上做镜像。Miniset 是小型 find-and-replace 补丁，既修 bug 又添装饰；Fixup 是针对特定问题的专项代码。

## 关键要点

- 预地牢（Predungeon）+ 瓦片化两阶段：设计与视觉分离
- 递归萌芽（Budding）vs 递归细分（Subdivision）：两种完全不同的房间分布风格
- 侵蚀（Erosion）+ 随机边缘：将规则矩形变为有机洞窟外形
- Marching Squares：从二值预地牢生成实际墙壁瓦片
- Miniset = 局部 find-and-replace：修 bug、加变化、插预制内容，三用合一
- 连通性检查（Lockout）：生成失败则重试，是 roguelike 关卡生成的通用保底

## 链接到的概念

- [[dungeon-generation-algorithm]]
- [[autotile-tileset-layouts]]

## 原文

- 链接：https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/
- 本地：`raw/articles/boristhebrave.com/2019-07-14_dungeon-generation-in-diablo-1.md`
