---
tags: [source, rendering, procedural-generation, mesh, marching-cubes]
date: 2026-04-27
sources: 1
---

# Marching Cubes Tutorial（Boris The Brave）

[[people/boris-the-brave]] 发表于 2018 年 4 月的图形技术教程，系统讲解 Marching Cubes 算法的原理与 2D/3D 实现。

## 摘要

Marching Cubes 是一种将标量场（scalar field）转化为多边形边界网格的经典算法，常用于破坏性地形、MRI 扫描可视化、metaballs 等场景。算法核心是将空间划分为均匀网格，对每个单元格的角点采样"内/外"状态（共 16 种组合），通过查找表确定该格内的边界线段（2D）或三角面（3D），逐格处理后拼合成完整网格。基本版本会产生 45° 斜线的锯齿感；**自适应版本**（adaptive marching cubes）利用标量函数的数值大小（而非仅内外布尔值）对边界顶点位置做线性插值，使结果更贴近真实曲面。文章附有 Python 实现参考。本文是三篇系列的第一篇，后续扩展到 3D 和 Dual Contouring。

## 关键要点

- 算法分三步：网格划分 → 查表确定格内边界 → 跨格拼合
- 16 种 2D 角状态对应不同边界线段；3D 扩展到 256 种（实际利用对称性简化）
- 自适应优化：用 `f(x)` 的值估算边缘交点，避免 45° 均匀分割
- 算法独立处理每个单元格，天然并行友好
- 局限：无法还原尖锐边角（sharp features），这是 Dual Contouring 的切入点

## 链接到的概念

- [[rendering/marching-cubes]]
- [[rendering/dual-contouring]]

## 原文

- 链接：https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/
- 本地：`raw/articles/boristhebrave.com/2018-04-15_marching-cubes-tutorial.md`
