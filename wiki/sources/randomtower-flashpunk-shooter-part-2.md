---
tags: [source, game-engines, flash, actionscript, 教程]
date: 2026-04-19
sources: 1
---

# FlashPunk Hello World Shooter Part 2（Marte / Random Tower）

[[people/marte-randomtower|Marte]] 发表于 2010 年 2 月的 FlashPunk 教程续篇，延续半月前的 Hello World Shooter 示例，用迭代更新的方式补足一个最小可玩射击 Demo 的剩余功能。

## 摘要

作者在原 Demo 的基础上追加了四组功能：**血量系统**（hit point）、**多武器切换**（Z/X/C/V/B/N 键对应不同子弹类型）、**敌人爆炸反馈**、以及 **R 键重启 / Q 键触发敌方开火**的调试快捷键。Demo 部署在 GameJolt，源码附带下载，继续用 FlashDevelop 编译。文章本身是一篇进度更新，但集中体现出 FlashPunk 作为 Flash 2D 框架的两个易用性优势：(1) **基于字符串标签的碰撞类型**让多种投射物类别的互斥碰撞规则只需少量模板代码就能铺开；(2) Entity 的生命周期与 World 的耦合通过静态单例 `FP` 简化，便于热重启 / 快速迭代。作者同时指出代码"还不干净、不适合教学"，正好侧面说明 FlashPunk 的学习曲线允许原型先跑起来再重构。另附 FlashPunk 官方论坛讨论帖链接，指引读者到社区里找更系统的教程与代码示例。

## 关键要点

- 多武器键位（Z/X/C/V/B/N）展示 FlashPunk Entity 可组合多种 Projectile 子类
- 血量系统 + 爆炸反馈 = 最小"游戏感"的反馈闭环
- R 键 restart / Q 键 trigger enemy fire = 开发期的快捷调试钩
- GameJolt 部署 + 源码下载 = 2010 年 Flash 独立游戏的典型交付路径
- 作者自评"代码不够干净"——对应 [[game-engines/flashpunk-framework|FlashPunk]] 框架"原型先跑起来"的设计取向

## 链接到的概念

- [[game-engines/flashpunk-framework]]

## 原文

- 链接：https://randomtower.blogspot.com/2010/02/flashpunk-hello-world-shooter-part-2.html
- 本地：`raw/articles/randomtower.blogspot.com/2010-02-02_flashpunk-hello-world-shooter-part-2.md`
