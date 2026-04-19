---
tags: [source, procedural, fractal, l-system, vfx, unity]
date: 2026-04-19
sources: 1
---

# L 系统闪电效果（Ted Sie / 阿祥的开发日常）

[[ted-sie|Ted Sie]] 发表于 2020 年 4 月的文章，以分形闪电为例展示 L 系统在游戏 VFX 中的工程化应用。

## 摘要

在 [[l-system-fractals|L 系统基础]] 之上，作者给出分形闪电的两条核心规则：**中点偏移**（每次迭代在线段中点插入垂直偏移向量，形成锯齿主干，思路同一维 [[diamond-square-noise|Diamond-Square]]）与**随机分支**（在新中点以概率长出侧向短线段）。朴素分支会指数爆炸，作者用四条抑制策略收敛：概率性生成、限角、限单次分支数、限总分支数。工程落地部分：`GameObject.CreatePrimitive(Quad) + GPU Instancing` 造网格、交界补 Quad 填缝、按主干/分支层级分别用 `AnimationCurve` 控制粗细、用 `Gradient` 控制颜色。整套流程示范了 **生成规则 + 图形学包装** 的典型协作模式。

## 关键要点

- 闪电 = 中点偏移（骨架） + 随机分支（枝蔓）。
- 抑制分支爆炸需要工程化约束而非纯数学规则。
- 网格大小/颜色靠 AnimationCurve + Gradient 做数据驱动渐变。
- 参考资料：Drilian's House of Game Development "Lightning Bolts"、知乎关于移动端雷电效果的若干文章。

## 链接到的概念

- [[l-system-lightning-bolts]]
- [[l-system-fractals]]
- [[diamond-square-noise]]
- [[shaping-functions]]

## 原文

- 链接：https://tedsieblog.wordpress.com/2020/04/16/lindenmayer-system-a-case-study-of-lightning-bolts/
- 本地：`raw/articles/tedsieblog.wordpress.com/2020-04-16_lindenmayer-system-fen-xing-tu-xing-xue-yi-shan-dian-xiao-gu.md`
