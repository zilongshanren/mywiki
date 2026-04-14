---
tags: [source, 渲染, 环境光遮蔽, 光照贴图, 老游戏]
date: 2026-04-14
sources: 1
---

# Deus Ex: Occlusion（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年（后续两次更新）的 Game Art Tricks 短文，从《Deus Ex》（2000）墙角显眼的一圈暗影出发，讨论屏幕空间 AO 时代之前的**预烘焙角落遮蔽**手法。

## 摘要

Deus Ex 的墙角阴影又直又清晰，像是烘焙进 lightmap 或顶点色里的静态 AO。Simon 原本困惑「为什么这条线如此平直」；一位叫 *badsector* 的读者给出了关键线索：这其实是 **Unreal Engine 1 光照贴图器的 bug**——烘焙时多边形外部被当成黑色填入，后续 blur lightmap 时黑色渗进了可见区域的边缘。Deus Ex: Human Revolution 沿用了这种风格，把「bug 变 feature」；而 Sims 4 则采取另一条路，在 SSAO 之上再摆一层**手贴的 AO mesh 补丁**来给角落加暗。Simon 引用 Sean Barrett 的名言「AO is an abstraction, SSAO is a crude approximation of an abstraction」——这条贴片路线正是对这层抽象的另一条回路。

## 关键要点

- Deus Ex 的墙角 AO 不是运行时计算，而是烘焙或顶点色；其锐利边缘部分源自 UE1 lightmap baker 的边界填充 bug
- lightmap 烘焙时「UV 岛外部的像素该填什么」是一个容易被忽略的问题——填零等于给整条边界加暗影
- Sims 4 在屏幕空间 AO 之外额外放置自定义 AO mesh，用手贴补丁换角落的可控性
- 屏幕空间 AO 是「对抽象的粗近似」——艺术家有时更想要可控的、形状正确的暗影，哪怕用的是 2000 年的老办法

## 链接到的概念

- [[prebaked-corner-occlusion]]
- [[hbao-interleaved-sampling]]

## 原文

- 链接：https://simonschreibt.de/gat/deus-ex-occlusion/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-2.md`
