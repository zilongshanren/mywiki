---
tags: [source, 游戏开发, AI, 转向行为, Siggraph]
date: 2026-04-27
sources: 1
---

# Steering Behaviors – Siggraph 2000（Robin Green / Bases and Frames）

[[robin-green]] 发表于 2016 年 5 月的回顾文章，记述他在 Bullfrog Productions 参与制作 *Dungeon Keeper 2* 与 *Theme Park World* 时实现 Craig Reynolds 转向行为算法的经历，以及受 Craig 邀请在 Siggraph 2000 上做 tutorial 的过程。

## 摘要

Craig Reynolds 的转向行为（Steering Behaviors）概念因为群体动画（Boids/flocking）于 1998 年获得奥斯卡科学技术奖，Reynolds 本人随后把它作为杠杆争取到 Siggraph 2000 整整一天的 Tutorial 时段。Robin Green 在 Bullfrog 时已经根据 Reynolds 的在线资料独立实现了大部分行为，并在此基础上扩展，加入了非静态地形中的 flocking 处理，以及若干新行为。核心实现使用 16-bit 定点数和增量 Voronoi 三角化做寻路，出自 Ian Shaw 之手，为原版 PlayStation 的运算速度而优化（最终 Bullfrog 未将该版本发布）。Robin 坦言，这批思路现在看来有些「质朴」——尤其是缺乏跨时间混合多个行为权重的连贯方法。Siggraph 2000 展示后不久，Robin 被 SCEA 聘用，与 Craig Reynolds 同在旧金山湾区工作。

## 关键要点

- Craig Reynolds 的 Boids 概念是「群体动画」这一类算法的来源，转向行为是其在游戏 AI 中的直接延伸。
- 生产环境的实现细节（定点数、增量 Voronoi 寻路）与「论文描述」有显著差距——早期主机的实际限制决定了具体方案。
- 行为混合（blending between behaviors over time）在 2000 年代初没有成熟方案，是当时遗留的技术空白。
- 这是游戏开发者正式进入 Siggraph 学术圈的早期案例之一。

## 链接到的概念

- [[steering-behaviors]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2016/05/13/steering-behaviors-siggraph-2000/
- 本地：`raw/articles/basesandframes.wordpress.com/2016-05-13_steering-behaviors-siggraph-2000.md`
