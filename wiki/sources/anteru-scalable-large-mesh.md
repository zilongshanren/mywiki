---
tags: [source, 渲染, LOD, 流式加载, 遮挡剔除, 大规模网格]
date: 2026-04-27
sources: 1
---

# Scalable Rendering for Very Large Meshes（anteru.net）

[[matthaeus-chajdas]] 发表于 2025 年 2 月的研究页，介绍亿级三角形多边形网格的实时渲染方案。

## 摘要

现有的大规模网格渲染技术往往需要专用硬件或软件光线追踪。本文提出**纯光栅化**的解决方案，支持数亿三角形网格的高质量抗锯齿渲染。关键技术是**紧凑的体素 LOD 简化**，并将流式加载、遮挡剔除、LOD 三者统一到单个光栅化管线中，无需单独的 pass。LOD 的生成速度快，即使面对最复杂的网格也适用。

## 关键要点

- **纯光栅化**：不依赖光线追踪，让超大网格在实时管线内跑起来，同时保持抗锯齿质量。
- **体素 LOD**：用基于体素的简化生成 LOD 级别，比传统网格简化更紧凑，生成速度也更快。
- **三合一管线**：流式加载（streaming）、遮挡剔除（occlusion culling）、LOD 切换在一个光栅化 pass 里完成，避免多 pass 同步开销。
- **自动调整**：渲染算法根据摄像机视角自动选 LOD 并裁掉不可见几何体（debug view 展示了从另一角度看时的 LOD 分布）。
- **与 [[nanite-reyes-comparison]] 的关系**：Nanite 同样解决超大网格渲染问题，但路线不同——Nanite 走 meshlet + 软件光栅 + 虚拟几何体，而本文走体素 LOD + 纯光栅；两者都试图把流式、剔除和 LOD 统一，但实现哲学差异显著。

## 链接到的概念

- [[voxel-lod-large-mesh]]
- [[nanite-reyes-comparison]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/research/scalable-rendering-for-very-large-meshes
- 本地：`raw/articles/anteru.net/2025-02-16_scalable-rendering-for-very-large-meshes.md`
