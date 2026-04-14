---
tags: [source, 独立游戏, 自研引擎, android, unity, 组件系统]
date: 2026-04-14
sources: 1
---

# Will of Flame（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 2014 年整理的个人项目页面，介绍他与 Antonio Hontoria 合作了两年的 side-scrolling 射击游戏《Will of Flame》。这篇不是技术深文，更像 portfolio 性质的项目档案；技术价值集中在"**纯 Java + OpenGL ES 从零手写的 Android 引擎**"这一段。

## 摘要

Will of Flame 是一款带重力枪机制的经典 run'n'gun 游戏：玩家用一束引力光束抓起敌人扔向场景里的陷阱（钟乳石、电鳗、水雷、螺旋桨）。游戏经历两次重构——最初是纯射击，后来变成"不能直接控制角色，只能用精神力移动敌人"的实验性玩法，因为操作过于复杂又改回常规射击。项目先以**从零手写的 Java Android 引擎**实现，后来为了跨平台迁到 **Unity + C#**，用到了 2D Toolkit、NGUI、Energy Bar Toolkit 等插件。Android 版曾在 HTC Desire、Galaxy II/III/Ace 上稳定跑 30 fps。IndieGogo 众筹失败后项目停摆。

## 关键要点

- 自研 Android 引擎是作为学习练习写的，是[[game-engine|组件式引擎]]的早期实践：图形、碰撞、drag、behavior、touch、animation 几个组件；
- 图形层在 **OpenGL ES** 上手写，使用 TexturePacker 做 spritesheet，大场景图使用"sprite dicing"切分后再拼；
- 碰撞层基于 **SAT（分离轴定理）** 实现，属于经典 2D 多边形 narrow-phase；
- 粒子系统支持火箭尾焰、水泡等；
- 场景可交互是玩法核心——敌人碰到道具会触发爆炸/电击等；
- 项目从 Java 自研引擎迁到 Unity 的理由在另一篇文章 [[sources/elopezr-java-vector-math|Java and Vector Math]] 里有更深入的反思；
- 关联工具：作者还写了配套的 [[sources/elopezr-wof-editors|Python/wxPython 级别编辑器]]。

## 链接到的概念

- [[game-engine]]
- [[component-entity-data-binding]]
- [[collision-detection-gjk-epa]]
- [[java-vector-math-limitations]]

## 原文

- 链接：https://www.elopezr.com/will-of-flame/
- 本地：`raw/articles/elopezr.com/2014-03-09_will-of-flame.md`
