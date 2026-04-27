---
tags: [source, procedural-generation, wfc, constraint-solving, level-generation]
date: 2026-04-27
sources: 1
---

# Driven WaveFunctionCollapse（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 6 月的文章，介绍将 WFC 作为**受驱动的瓦片选择器**而非完整关卡生成器的设计模式。

## 摘要

[[game-development/wave-function-collapse]] 的典型弱点是大尺度结构单调、缺乏整体叙事感。本文提出"Driven WFC"的解法：先用任意方式（手工、其他算法）决定关卡的宏观结构，再把宏观决策转换为 WFC 的初始约束（对格子的候选瓦片集进行预过滤），最后用 WFC 完成局部细节的填充与拼接。Boris 指出这个思路本质上把 WFC 退化为一种"瓦片选择算法"，类似 Marching Cubes，但 WFC 能向更远的邻居看，使瓦片之间无缝衔接。典型案例是 Townscaper：用户绘制填充布局，每个格子的填充状态转换为顶点上的布尔值约束，再跑 WFC 变体生成最终网格。Marian42 的 White City 也用高度图作为粗粒度约束驱动 WFC，每 8 格才施加一个约束，从而保留 WFC 风格的同时控制大尺度形态。

## 关键要点

- Driven WFC：外部来源决定宏观结构，WFC 只负责局部瓦片选择与连接
- 实现极简：宏观决策转换为初始域过滤，无需改动 WFC 核心
- Townscaper 是该模式的典型实现
- 粗粒度约束（每 N 格一个）可在结构控制与生成自由度间取得平衡
- 可与无限分块生成结合，只需按 chunk 驱动 WFC

## 链接到的概念

- [[game-development/wave-function-collapse]]
- [[game-development/driven-wfc]]

## 原文

- 链接：https://www.boristhebrave.com/2021/06/06/driven-wavefunctioncollapse/
- 本地：`raw/articles/boristhebrave.com/2021-06-06_driven-wavefunctioncollapse.md`
