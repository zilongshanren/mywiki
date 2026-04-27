---
tags: [source, game-development, wfc, quantum-computing, procedural-generation]
date: 2026-04-27
sources: 1
---

# Quantum WaveFunctionCollapse（Boris The Brave）

[[people/boris-the-brave]] 发表于 2024 年 11 月的文章，评述 Raoul Heese 将 WFC 映射到真实量子硬件的研究论文。

## 摘要

文章介绍了 Heese 的论文《Quantum WaveFunctionCollapse》，该论文尝试将经典 WFC 算法翻译为量子电路并在 IBM 127 量子比特芯片（Eagle）上实际运行。量子 WFC 的核心思路是：用 q 个量子比特表示每个网格单元（segment），通过**初始化门**建立各单元的初始概率分布，再通过**控制门**在相邻单元之间施加邻接约束，最终对整个量子叠加态做一次测量，即同时获得一个符合所有约束的完整地图。Boris 指出，量子 WFC 实际上只利用了量子计算的**概率优势**（一次采样即得一个解），而非量子计算通常宣传的**指数级/平方根级算法加速**（量子干涉效应）——因此严格来说它并非真正的「量子加速」。现实层面，127 量子比特严重限制可解问题规模，量子噪声使结果可靠性低下，实验需重复 10000 次才能统计有效结果。Boris 的结论是：短期内量子 WFC 不会替代经典实现，但这项研究确认了经典 WFC 名字里的「波函数」确实有扎实的量子力学对应，令人满足。

## 关键要点

- 量子 WFC：用量子电路建模约束，一次测量采样一个合法地图
- 每个网格单元用 q 量子比特表示（2^q ≥ 瓦片数），N 个单元共需 N×q 量子比特
- 量子门分两类：**初始化门**（建立概率分布）和**控制门**（施加邻接约束）
- 本质是**概率优势**，而非量子干涉带来的算法级加速
- 127 量子比特严重限制：3×3 棋盘格只需 9 比特，4×10×8 瓦片就需要 120 比特
- 量子噪声导致实际结果可靠性低，论文中实验重复了 10000 次
- 混合量子-经典方案（Hybrid QFC）可降低量子比特需求
- 经典 WFC 只从前向传播约束；量子 WFC 也只做单向传播，略微更容易产生矛盾

## 链接到的概念

- [[game-development/wave-function-collapse]]
- [[game-development/arc-consistency]]

## 原文

- 链接：https://www.boristhebrave.com/2024/11/03/quantum-wavefunctioncollapse/
- 本地：`raw/articles/boristhebrave.com/2024-11-03_quantum-wavefunctioncollapse.md`
