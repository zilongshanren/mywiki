---
tags: [source, rendering, 可微渲染, 自动微分, 优化, JAX]
date: 2026-04-27
sources: 1
---

# Learning to Differentiably Rasterize（Angelo Pesce / c0de517e）

[[angelo-pesce]] 发表于 2025 年 2 月的文章，记录了用 SDF 光线行进实现可微渲染器、并用其优化场景基元逼近的 hack week 实验。

## 摘要

文章以"Auto-Jorge"愿景（自动调优 Shader 参数）为背景，探索现代自动微分框架（JAX）在复杂图形程序上的适用性。核心贡献是提出以 SDF sphere tracing 作为"天然可微"光栅化器——固定步数迭代不含 control flow 间断，边缘处自然软化，无需额外设计软边。实验将 ShaderToy 中的 GLSL raymarcher 经 LLM 翻译为 Python/JAX，接入梯度下降优化球体/AABB 基元的位置与大小以逼近目标深度缓冲。文章还系统对比了 JAX 与 PyTorch 的设计差异，分析了局部最优问题，并展示遗传编程交叉和层次分割两种全局优化策略的显著效果。

## 关键要点

- SDF raymarcher 是比标准光栅化更"天然"的可微渲染路线
- JAX 对复杂程序比 PyTorch 快得多，但需注意 traced 数组不能用 Python `if`、循环展开会膨胀 IR
- 梯度下降本身是局部优化器，对多极小值问题必须配合全局策略（遗传编程 / 层次分割）
- 层次分割（从 1 个基元开始逐步分裂）效果远优于直接用目标数量初始化
- Gaussian Splatting 的做法（点云初始化 + 自适应 densification）是这些原则的工业级实践

## 链接到的概念

- [[differentiable-rendering]]
- [[automatic-differentiation]]
- [[neural-graphics-primitives]]
- [[gaussian-splatting-web]]
- [[raymarching-intro]]

## 原文

- 链接：https://c0de517e.com/019_autoinigo.htm
- 本地：`raw/articles/c0de517e.com/2025-02-10_learning-to-differentiably-rasterize-doing-things-my-way-a-k.md`
