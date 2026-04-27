---
tags: [source, game-development, game-jam, unity, post-mortem]
date: 2026-04-27
sources: 1
---

# Lucky Fluke Post Mortem（Boris The Brave）

[[boris-the-brave]] 发表于 2020 年 7 月的文章，复盘 48 小时 Game Jam 作品 *Lucky Fluke* 的开发经验。

## 摘要

Boris 与两位合作者（美术师 Praeto、音效/作曲 jhicks）在 Game Jam 中完成了 2D 射击游戏 *Lucky Fluke*。全程约 15 分钟就做出了核心机制原型，Unity 的工作流使多人协作（代码 / 美术 / 音效分工）顺畅推进。文章总结了三个主要教训：一、Unity 上手极快，Google 能解决绝大多数技术困难；二、Jam 游戏与常规游戏的目标截然不同——评审时间极短，游戏必须像"一把锤子砸脸"，立即展示核心 Hook；三、缺少专职的游戏设计师导致关卡设计薄弱，游戏难度偏高、高潮内容藏在后期关卡导致大多数评审看不到。核心结论是：做完一个小游戏比多年磨大作更有成就感。

## 关键要点

- Unity 2D 工作流对多人分工天然友好，程序员 / 美术 / 音效可并行无缝交接
- 技术难点（jiggle bones、全屏支持、sprite sort order、FMOD）均靠社区搜索解决
- Jam 评审覆盖量大，每款游戏平均时间极短，设计重点应是零门槛 + 立即可见核心创意
- "Next Level" 按钮是跳过关卡设计不均衡和隐藏 bug 的实用技巧
- 游戏设计经验的缺失（无专职设计师）是该作品的最大短板

## 链接到的概念

- [[indie-game-dev-rhythm]]
- [[easy-to-learn-hard-to-master]]

## 原文

- 链接：https://www.boristhebrave.com/2020/07/18/lucky-fluke-post-mortem/
- 本地：`raw/articles/boristhebrave.com/2020-07-18_lucky-fluke-post-mortem.md`
