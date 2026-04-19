---
tags: [source, rendering, sdf, shader, unity, urp]
date: 2026-04-19
sources: 1
---

# Procedural Pool Balls（Daniel Pokladek）

[[daniel-pokladek]] 发表于 2026 年 3 月的 Unity URP shader 教程，用 [[sdf-2d-primitives|2D SDF]] 从零开始程序化生成一整套风格的台球贴图——横向条纹、数字圆环背景、数字本身，全部由 shader 实时计算而非预制贴图。

## 摘要

作者从假期陪家人打台球时萌发的想法出发：能不能用 SDF 生成一套任何分辨率下都保持锐利的台球？教程同时给出 HLSL 代码与 ShaderGraph 节点图。核心技术三步走：（1）用 `length(uv.y - 0.5) - _Line_Thickness` 和 `smoothstep` 画出横向条纹；（2）用 `length(uv - center) - _Radius` 画圆形数字背景，并通过 `U * 2 + frac()` 让数字同时出现在球的正反面；（3）4×4 SDF atlas 存放 15 个数字和一个空位，通过 `fmod/floor` 计算 tile 偏移，用 `smoothstep(_Edge_Min, _Edge_Max, sample)` 得到锐利抗锯齿的数字边缘。作者还分享了几个工程细节：Unity UV 原点在左下 vs 贴图左上的修正（选择 shader 里补偿而不是改贴图）、用 `saturate(_Number)` 替代 if 分支避免 GPU branching、以及对 Ben Cloward 的 SDF 文本教程所做的小改进。

## 关键要点

- SDF + smoothstep 的"柔边 mask"是整个 shader 的统一基元——条纹、圆环、数字都是同一个模式。
- `U *= 2; U = frac(U)` 把一张贴图贴满球表面一圈的需求变成"两张贴满半圈"——数字同时出现在正反两面的常见做法。
- 4×4 SDF atlas 一张纹理解决 16 个数字，用整数属性 `_Number` 作为索引。
- Unity UV 在 shader 里修正而不是改贴图，是一个"记住这个坑"的工程习惯。
- `circleMask *= saturate(_Number)`：0 号球自动隐藏圆环，避免分支指令。

## 链接到的概念

- [[procedural-pool-ball-sdf]]
- [[sdf-number-atlas-text]]
- [[sdf-2d-primitives]]
- [[sdf-operations-shader]]

## 原文

- 链接：https://www.danielpokladek.me/posts/shaders/2026/pool-ball/
- 本地：`raw/articles/danielpokladek.me/2026-03-17_procedural-pool-balls.md`
