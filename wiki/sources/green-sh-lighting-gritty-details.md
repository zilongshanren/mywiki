---
tags: [source, 渲染, 球谐, 全局光照, PRT, PS2]
date: 2026-04-14
sources: 1
---

# Spherical Harmonic Lighting: The Gritty Details（Robin Green / Bases and Frames）

[[robin-green]] 于 2016 年在博客 Bases and Frames 上写的一篇「作者自述」式回顾，回忆了他 2002–2003 年在 Sony Computer Entertainment America R&D 实现 [[spherical-harmonics|球谐光照]]、并把成果写成 GDC 2003 同名 paper 的经过。这篇 paper 在「预计算辐射传输（PRT）」这一术语被正式提出**之前**就已经存在，是把 SH 光照从 Peter-Pike Sloan 的学术论文搬到主机游戏管线的关键教材。

## 摘要

Robin Green 收到 Peter-Pike Sloan *Fast, Arbitrary BRDF Shading for Low-Frequency Lighting Using Spherical Harmonics* 的 SIGGRAPH 预印本后，和经理打赌要在 SIGGRAPH 之前在 PS2 上跑出 SH 光照。他先在 Maple 里验证 SH 投影和逐级重建，再用自写的简单体素化光追（Gabor Nagy 的 Equinox 3D 提供的实时 ray tracer）烤 visibility。文章提到最初 ray tracer 的体素边界 bug 导致沙发底下出现棋盘阴影，修好后用来演示 SH vs. 点光对比，说服团队把工作推进到 GDC 2003。paper 本身署名风格「Gritty Details」——它早于 PRT 这个术语出现。

文章特别提到 paper 里存在一些**公式 bug**，最著名的是 SH 旋转部分——从 Ivanic 原始论文的复印件里辨识下标时出错，后来由 Lionhead 图形主程 Don Williamson 在自己项目里验证 Ivanic（实值）和 Choi（复值）两种旋转方法，确认 Ivanic 更快，对于低阶情况 ZYZ 分解仍然是最优解。

## 关键要点

- SH 光照在游戏主机上的首次完整实现发生在 PS2，而且早于「PRT」这个术语的流行。
- 制作难点不是数学，而是**获得水密 manifold 模型**和 visibility 烤制流水线的工程整合。
- ray tracer 早期 bug 会制造典型的体素网格 artifact（「棋盘阴影」），这是 [[bottleneck-analysis|bug 的直观识别]]的好例子。
- SH 旋转（rotation）的实用方法是 ZYZ 分解——即使有近似快速旋转提案，在低阶 SH 下 ZYZ 仍是冠军。
- Ivanic vs. Choi：前者从实值推，后者从复值推；Don Williamson 实现并 benchmark 后 Ivanic 胜出。
- paper 里承诺的「未来工作」从来没做——因为 SCEA R&D 立刻被 CELL 项目和 PSGL 锁死三年半。

## 链接到的概念

- [[spherical-harmonics]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2016/05/11/spherical-harmonic-lighting-the-gritty-details/
- 本地：`raw/articles/basesandframes.wordpress.com/2016-05-11_spherical-harmonic-lighting-the-gritty-details.md`
