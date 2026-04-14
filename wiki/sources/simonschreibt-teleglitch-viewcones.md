---
tags: [source, 渲染, 视野阴影, 风格化, 2d]
date: 2026-04-14
sources: 1
---

# Teleglitch: Viewcones（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年 1 月的短文，从《Teleglitch》那种俯视 2D 像素视野阴影开始，讨论这家独立开发团队是如何在**不写任何 raycast 代码**的前提下把「玩家看不见的区域」盖黑的。

## 摘要

Simon 起初以为 Teleglitch 是在墙上「垂直向上拉黑墙」，后来被读者和开发者纠正：真相更便宜——他们把每堵墙从玩家位置**径向外推**一大段，用黑色四边形填充外推范围。这样以顶视角看去就像每堵墙后面拖着一条漫长的黑影，刚好对应视野阴影。文章里也对比了《Nox》（raycast 做「视锥」）和《Diablo 2》（每个物件自带一张可拉伸的 shadow map、无需 3D 几何）两种不同的实现路径。评论区里玩家抱怨外推方法「一眼能看破」——黑墙的 3D 质感偶尔会露出来，且阴影会随着玩家移动而不自然地流动；但这也正是这个 trick 的特征：它不是真的可见性计算，只是**用光栅化把看不见的区域盖黑**。

## 关键要点

- Teleglitch 用「沿玩家-墙面径向外推的黑色几何」伪造视野阴影，不做 raycast
- 外推方向是水平径向，不是垂直向上——Simon 一开始理解错了
- 黑几何**逻辑上长度无限**，只靠视口裁剪成有限形状；需要有限长度时可以用遮挡物高度作为外推距离
- Diablo 2 用**每物件一张可拉伸的 shadow map**达成几乎相同的效果，完全不需要 3D 几何
- 视觉破绽：黑色 3D 墙体有时会露出侧面厚度，「once you see it you can't unsee it」

## 链接到的概念

- [[extruded-wall-shadow-viewcone]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/teleglitch-viewcones/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-7.md`
