---
tags: [source, game-development, wfc, procedural-generation, constraint-solving]
date: 2026-04-27
sources: 1
---

# Constraint-Based Tile Generators（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 10 月的文章，系统梳理 WFC 与 Model Synthesis 所属「基于约束的瓦片生成器」大家族的各维度变体。

## 摘要

文章将 WaveFunctionCollapse（WFC）与 Model Synthesis（MS）归纳为「约束驱动瓦片生成器」这一更广义类别，并从五个独立维度分析可定制化的方向。**约束模型**方面，分 Adjacency（邻接模型，Wang tiles）与 Overlapping（重叠模型，N×N 窗口匹配）两种；**约束来源**方面，分样本推导（直接从样本地图提取）、手工标签（每条边贴标签）、像素/顶点相似度（自动识别视觉连续性）三种；**求解器**方面，可用 Arc Consistency（AC-3 / AC-4）、专业 SMT/ASP 求解器（Z3、Clingo），也可自定义；**格子启发**方面，线性扫描（MS）与最小熵（WFC）是两个主流选项；**矛盾处理**方面，有重启、回溯、分块重启、Modifying in Blocks 等策略。文章还指出约束系统可应用于多种网格拓扑（方格、六边形、三角格、Townscaper 的不规则格），以及像素、游戏对象等不同"瓦片"类型。最终总结：WFC 和 MS 只是这个大空间里的两个具体点，探索更多组合是一个值得发掘的设计空间。

## 关键要点

- WFC / MS 是「约束驱动瓦片生成器」的子集，五个维度均可独立替换
- **Adjacency 模型**速度快但只捕捉 1 格邻近相关性；**Overlapping 模型**更强但更慢
- 样本推导直觉好但容易过拟合；手工标签更可控但需要理解后果
- 求解器核心是弧相容（AC-3 / AC-4），专业求解器（Z3 / Clingo）功能更强但侵入性大
- 格子选择启发：**线性扫描**（MS）vs **最小熵**（WFC），后者经验上效果更好
- 矛盾处理选项：重启 / 回溯 / 分块 / CDCL，难度与可靠性各异
- 网格拓扑（方格 / 六边形 / 不规则）可自由替换

## 链接到的概念

- [[game-development/wave-function-collapse]]
- [[game-development/arc-consistency]]
- [[game-development/constraint-based-tile-generators]]

## 原文

- 链接：https://www.boristhebrave.com/2021/10/31/constraint-based-tile-generators/
- 本地：`raw/articles/boristhebrave.com/2021-10-31_constraint-based-tile-generators.md`
