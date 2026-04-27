---
tags: [source, procedural-generation, graphics, blender, celtic-knots]
date: 2026-04-27
sources: 1
---

# Celtic Knots（Boris The Brave）

[[people/boris-the-brave]] 发表于 2014 年 5 月的文章，介绍为 Blender 开发的凯尔特风格编结图案生成插件。

## 摘要

Boris 为 Blender 2.68a 编写了一个插件，能够根据用户提供的框架网格（framework mesh）自动生成三维贝塞尔曲线，输出具有"凯尔特"风格的编结装饰图案。凯尔特结是凯尔特及其他文化中常见的精细装饰纹样，特征是多条线条交替穿越彼此（over-under pattern）。该插件以参数化方式生成曲线，结果可在 Blender 中进一步修饰以得到更复杂的变体。文章同时提供了教程链接和作品画廊，是后续 1.0 版本（含斜纹生成）的基础工作。

## 关键要点

- 插件基于框架网格自动将边转换成编结曲线，over-under 交替关系由算法控制
- 输出为 3D 贝塞尔曲线，可在 Blender 中作后续编辑
- 插件并不尝试还原历史文物中所有复杂角度变体，设计目标是快速生成原型
- 2018 年的 1.0 版本（[[sources/boris-celtic-knots-twills]]）在此基础上增加了斜纹（twill）支持

## 链接到的概念

- [[game-development/celtic-knots]]

## 原文

- 链接：https://www.boristhebrave.com/2014/05/07/celtic-knots/
- 本地：`raw/articles/boristhebrave.com/2014-05-07_celtic-knots.md`
