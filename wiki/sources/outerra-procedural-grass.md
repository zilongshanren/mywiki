---
tags: [source, 渲染, 程序化, 草地, 几何着色器, LOD]
date: 2026-04-27
sources: 1
---

# Procedural Grass Rendering（Outerra Blog）

[[outerra-team]] 发表于 2012 年 5 月的文章，介绍 Outerra 行星引擎中两阶段程序化草地渲染方案。

## 摘要

Outerra 的草地渲染分为两个阶段，彼此解耦。第一阶段生成**草冠层（canopy）**：一张分辨率约 30 cm 的高度掩码，用 fractal pattern 表达草的分布稀密与高低变化；这张贴图同时兼作远景「矮植被信封」的程序化纹理，使得远处地形上的草与近处的草在视觉上保持连续。第二阶段用几何着色器在 canopy 数据驱动下**按需生成草叶**：每根草叶是 7 顶点 5 三角形的 triangle strip，带 3 段弯曲；对于矮草改用 V 形折叠来等效地翻倍视觉密度。最近处每个 canopy 像素生成 4 根草叶，每降一个 LOD 级别减半叶片数量、同时加倍宽度，维持视觉覆盖率。草叶的动画直接复用海浪纹理驱动，概念验证有效。

## 关键要点

- **双阶段解耦**：canopy 作为中间表示，同时服务近景草叶生成和远景地形纹理，避免 LOD 断层。
- **几何着色器生成叶片**：零预存储顶点；LOD 完全由 canopy 采样密度控制，无需多套网格资产。
- **V 形折叠技巧**：矮草把 3 段草叶折叠成 V 形，以相同顶点数换来约 2× 视觉密度。
- **动画即纹理采样**：用已有的波纹纹理驱动叶片偏移，工程成本接近零。
- fractal canopy 天然提供草地的空间变化，不需要手工绘制草地分布图。

## 链接到的概念

- [[procedural-grass-rendering]]
- [[outerra-team]]

## 原文

- 链接：https://outerra.blogspot.com/2012/05/procedural-grass-rendering.html
- 本地：`raw/articles/outerra.blogspot.com/2012-05-27_procedural-grass-rendering.md`
