---
tags: [source, rendering, art-direction, color-theory, lighting]
date: 2026-04-19
sources: 1
---

# Coloured light in Proun（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 11 月发表的文章，接上一周的「lighting in Proun」技术篇，这周讲**艺术选择**：Proun 每条赛道用一对对比色作为 sun / skylight 的颜色。

## 摘要

常规 3D 艺术配置是暖黄日 + 冷蓝天——模拟真实大气，阴影偏蓝 / 受光偏黄、不会死黑，契合 van Dongen 高中美术老师那句「阴影永远不要用纯黑」。Proun 第一赛道走这条。第二赛道走到反直觉——**青 / 蓝日 + 橙天**，依然在对比色轴上；第三赛道更野——**绿 / 蓝日 + 粉天**。他自认不懂色彩理论，但发现只要两色对比合理，**几何用纯饱和色（Kandinsky / Mondriaan 式）、灯光承担微妙色渐变**的组合就能站得住。核心启示：3D 场景是虚构的，灯光配色完全不需要贴真实日光——当纯色几何的平面构图单独不够立体时，对比色灯光带来的微妙色渡才是画面「活」的原因。

## 关键要点

- 常规配置：暖黄日 + 冷蓝天 → 阴影偏蓝、受光偏黄（Proun 赛道一）
- 赛道二：青 / 蓝日 + 橙天（对比色，反直觉但和谐）
- 赛道三：绿 / 蓝日 + 粉天（更极端但仍在色环对比轴）
- 规则：只要两色对比合理，不必贴真实日光
- 纯饱和几何（Kandinsky / Mondriaan）需要对比色灯光提供色渡，否则平
- 可行前提：[[lightmap-baking-workflow]] 允许自由迭代配色（离线）

## 链接到的概念

- [[colored-sky-sun-lighting]]
- [[lightmap-baking-workflow]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/11/coloured-light-in-proun.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-11-27_coloured-light-in-proun.md`
