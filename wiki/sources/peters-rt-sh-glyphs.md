---
tags: [source, 渲染, 球谐, 光线追踪, 科学可视化, 多项式求根]
date: 2026-04-27
sources: 1
---

# Ray Tracing Spherical Harmonics Glyphs（Christoph Peters et al. / VMV 2023）

[[christoph-peters]]、Tark Patel、Will Usher、Chris R. Johnson 发表于 VMV 2023（Vision, Modeling, and Visualization）的论文，获大会荣誉提名奖（前三名之一，共 26 篇投稿）。

## 摘要

球谐字形（SH glyph）是高角分辨率扩散成像（HARDI）数据可视化的标准手段——从单位球出发，将表面各点按 SH 基函数线性组合的函数值缩放，从而得到一个展示方向分布函数（ODF）的三维字形。

本文提出用**光线追踪**高效渲染这类字形的方法：将光线-字形求交问题化归为一个多项式的根查找，多项式阶数为 $2k+2$（其中 $k$ 是 SH 的最高偶次带）。通过高效且数值稳定的多项式求根，找出光线与字形的所有交点；同时推导出法向量的简洁公式，并计算近似严格的轴对齐包围盒（AABB）以加速遍历。与之前工作相比：更快、更灵活、更准确；且因求出全部交点，可支持复杂着色与不确定性可视化。

## 关键要点

- SH glyph 光线求交等价于求解 $2k+2$ 次多项式
- 数值稳定的完整根查找，支持所有光线方向（含凹陷字形）
- 法向量由代数公式直接推导，无需数值微分
- 紧密 AABB 计算进一步减少空射线开销
- 应用场景：神经纤维束追踪结果可视化、diffusion MRI

## 链接到的概念

- [[spherical-harmonics]]
- [[sh-glyphs-ray-tracing]]
- [[polynomial-root-finding-gpu]]

## 原文

- 链接：https://doi.org/10.2312/vmv.20231223
- 本地：`raw/articles/momentsingraphics.de/2023-12-23_ray-tracing-spherical-harmonics-glyphs.md`
