---
tags: [source, 渲染, PS2, 过程式几何, VU, 主机硬件]
date: 2026-04-14
sources: 1
---

# Procedural Rendering on PS2（Robin Green / Bases and Frames）

[[robin-green]] 2016 年回顾其 GDC 2001 演讲 *Procedural Rendering on PS2* 的起源。这是一份介绍 PS2 内部结构、推广 SCEA 新造的 VU（Vector Unit）程序编译工具链和 DMA chain dump 工具的 tutorial，demo 主题借用了 William Latham 和 Stephen Todd 1990 年代在 IBM 英国研究中心做的「Lifeforms」——过程式生成的有机形态，后来由 Latham 在 TED 上回顾。

## 摘要

Robin 需要一个**视觉震撼但生成简单**的 demo 来展示「一帧内过程式生成的几何量可以超过 PS2 主内存的容量」这一卖点——他讨厌过程式地形和大粒子系统这些老套路，所以选择了 Latham 的 Lifeforms：把形状从基本图元开始按几何变换树（rotate、sweep、horn 等）叠加成有机形态，参数随机化后得到一个「物种」的序列。Todd & Latham 1992 年的书 *Evolutionary Art and Computers* 对生成规则有「时而极度详细、时而敷衍挥手」的奇特写法。

presentation 分两段：

1. **前半**：怎么生成这些 Lifeforms——树状几何变换栈如何随机组合。
2. **后半**：怎么在 PS2 上高效实现——用新工具链把几何变换推到 VU 上跑，用 DMA chain 喂 GS。

其中**旋转插值**需要评估指数/幂函数，而 VU **没有好的 transcendental 库**——这个问题直接把 Robin 推上了第二年 GDC 2002 的 [[faster-math-functions|*Faster Math Functions*]] tutorial 之路。

Robin 在演讲现场不得不做了一句「随机生成的有机形态偶尔会出现过于生殖形态的图形，请各位观众见谅」的免责声明。他的另一个观察是：「当你能以 60fps 实时生成 Latham 当年要花几天渲染的那种艺术时，它就不再是艺术了」——一种关于算力/速度对艺术性损耗的忧伤小笔记。

## 关键要点

- PS2 时代过程式几何的卖点：生成量可以超过内存容量——给主机图形的小内存打开一扇窗。
- 这次 demo 直接导致了 Robin 钻研 VU 上的 [[faster-math-functions|transcendental 函数高速实现]]——两篇 tutorial 是因果相连的。
- Latham/Todd 的 Lifeforms 的生成规则写在 1992 年的 *Evolutionary Art and Computers* 里，以详略混乱出名。
- 主机编译工具链（VU 程序编译器、DMA chain dump 工具）是 SCEA R&D 的早期工程交付物，Robin 的演讲是对外发布通道之一。
- 「60 fps 的 procedural art 不再是艺术」：一种关于计算速度对艺术稀缺性的损耗的非技术观察。

## 链接到的概念

- [[procedural-rendering-ps2]]
- [[faster-math-functions]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2016/07/25/procedural-rendering-on-ps2/
- 本地：`raw/articles/basesandframes.wordpress.com/2016-07-25_procedural-rendering-on-ps2.md`
