---
tags: [source, 程序化生成, 进化算法, 图像生成, clip]
date: 2026-04-27
sources: 1
---

# Generative Generators（Boris The Brave）

[[boris-the-brave]] 发表于 2023 年 12 月的 ProcJam 2023 参赛实验，一句话描述：用 CLIP 相似度评分 + 进化算法自动调优一个纯参数化的程序化图像生成器。

## 摘要

Boris 为了在"不能使用 AI"的黑客松规则边界上做到极致，设计了一个类 GAN 架构：生成器本身是纯 JavaScript 参数化树形分形渲染器（无任何 ML 成分），外层用 Python wrapper 调用无头 Chrome 取图，然后用 [[evolutionary-programming|进化算法]] 搜索最优参数，打分使用预训练 CLIP 模型的余弦相似度（图像 embedding vs. 文本 caption）。由于生成器是不可微的黑盒，无法用梯度下降，进化算法每一轮从当前参数出发做随机扰动、评分、取最优。实验结果能在 150 步内把颜色和结构大致引导到目标文字描述（如 "oak tree"、"palm tree"、"coral"），但因生成器参数太少、图像质量差、CLIP 分布外失配等原因，效果有限。Boris 坦言主要贡献在于框架思路而非结果质量。

## 关键要点

- 生成器完全无 AI，仅靠 36 个参数控制颜色、分支角度、终止概率、线段粗细等
- 参数支持"从根到叶"插值，实现树干与树叶的渐变属性
- 评分函数：CLIP 图像 embedding 与文字 caption embedding 的余弦相似度
- 优化器为进化编程（不依赖梯度），批量评估候选参数后取最高分
- 主要局限：参数空间太小（缺乏多样性），图像质量差（CLIP 分布外），批量小（每代仅 20 张）
- 该思路具有可扩展性：换用 SpeedTree 等复杂生成器 + 更大算力，结果将大幅改善

## 链接到的概念

- [[game-development/generative-generators-clip-evo]]
- [[game-development/procedural-dungeon-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2023/12/03/generative-generators/
- 本地：`raw/articles/boristhebrave.com/2023-12-03_generative-generators.md`
