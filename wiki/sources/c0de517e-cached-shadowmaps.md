---
tags: [source, 渲染, 阴影, gpu, 优化]
date: 2026-04-14
sources: 1
---

# Service Update: Cached Shadowmaps（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 8 月的一篇「service update」，主要是指向 Mike Day 在 SIGGRAPH 2012 上发表的 cascaded shadowmap 缓存实现，并顺带补完了自己 2011 年那篇「bad idea sketch」背后的故事与失败实验。

## 摘要

Pesce 在 2011 年曾在博客上半开玩笑地写过一个想法：对于 cascaded shadow maps 的远级联，不必每帧重绘，而是**分帧更新**（例如 5 层里每帧只更新第一层和剩余 4 层里的 2 层）。这个想法来自他观察 Crysis 2 在动的时候的行为。他们团队当时正在优化一款游戏的 GPU，发现阴影生成很昂贵，尝试过两个版本的缓存方案：

1. **分帧更新远级联**——动态投射者会走进自己的旧阴影，视觉上露馅。
2. **改为缓存静态投射者**，每帧只重绘动态的——理论上更对，但他们的 shadowmap 尺寸下阴影生成时间已经有一半花在 bandwidth / resolve 上，所以**没带来净收益**。

这使他放弃继续实验，但一直好奇换个硬件世代或 shadowmap 尺寸会不会翻盘。2012 年 Mike Day（Insomniac Games，paper 由 Mike Acton 代为展示）公开了一个非常详细的工程实现，把这个想法完整补齐：**在 UV 和深度上都做重投影**，然后把动态投射者 splat 到重投影后的缓存上。Pesce 写这篇「service update」就是为了把读者指向 Mike Day 的那份 paper。

## 关键要点

- **Cached CSM 的核心动机**是远级联的时间相干性高、每帧重绘几乎是重复劳动。
- **两种缓存粒度**：分帧更新 vs 区分静态/动态投射者；前者容易露馅，后者更通用但依赖 shadowmap 尺寸。
- **瓶颈结构决定优化收益**：当阴影生成已经 bandwidth-bound 时，缓存静态几何只省了算术，没省 bandwidth，净收益可能为 0。这是 [[bottleneck-analysis]] 的经典现场演练。
- **Mike Day 的方案**：在 UV + depth 双重投影，之后 splat 动态投射者。这是后来主流实现的范式，也是 Pesce 原始 sketch 的完整化。
- **没走完的路**：Pesce 还考虑过用 stencil 标记每区域的 z-near/z-far 范围（仅 360/PS3 可行）、以及各种 bandwidth 相关的 hack，但因为 worst case 不变而放弃。
- 这篇文章本身不是系统教程，而是一则「指向别人的成果 + 分享失败实验」的小笔记，风格正是 Pesce 博客的典型：公开半成品想法、不介意被别人补完。

## 链接到的概念

- [[cached-shadowmaps]]
- [[angelo-pesce]]
- [[bottleneck-analysis]]
- [[rendering-pipeline]]
- [[culling]]
- [[stencil-buffer]]

## 原文

- 链接：http://c0de517e.blogspot.com/2012/08/service-update-cached-shadowmaps.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-08-18_service-update-cached-shadowmaps.md`
- 相关工作：Mike Day, *CSM Scrolling*, SIGGRAPH 2012（Insomniac Games）
- 前篇：Pesce, *Bad ideas don't require much explanation*, 2011-09
