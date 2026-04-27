---
tags: [source, 渲染, 头发, 体积渲染, 实时]
date: 2026-04-27
sources: 1
---

# Real-Time Hybrid Hair Rendering（Eurographics Symposium on Rendering 2019）

Erik Sven Vasconcelos Jansson、[[matthaeus-chajdas|Matthäus G. Chajdas]]、Jason Lacroix、Ingemar Ragnemalm 发表于 EGSR 2019 DL-only 及 Industry Track，提出将发丝光栅化与体积光线步进结合的完整实时头发渲染方案。

## 摘要

实时头发渲染面临两大挑战：复杂的各向异性着色模型，以及极高的发丝数量（人类头发超 10 万根，动物毛发常超百万）。以往方案要么用发丝（strand-based），要么用体积（volume-based），各有局限。本文将两种方法合并为一个**混合管线**：直接可见的发丝正面用光栅化渲染，遮挡区域及 LOD 退化部分用体积光线步进（ray-marching）处理；同一个体积表示还被复用于实时计算全局阴影和环境光遮蔽（AO）。

整个方案无需预处理，可作为现有渲染管线的直接替换（drop-in replacement）。

## 关键要点

- 发丝/体积混合：近处用光栅化，远/遮挡区域用 ray-marching，一份体积数据两用
- 体积同时承载全局阴影与 AO，实现"自阴影"效果
- 无预处理：适合动态头发（物理模拟、动画）
- 覆盖真实规模：136,320 根（人头）+ 961,280 根（熊）均验证

## 链接到的概念

- [[realtime-hair-hybrid-volume]]
- [[hybrid-hair-rendering]]
- [[hair-shader-anisotropic]]

## 原文

- 链接：https://anteru.net/research/realtime-hybrid-hair-rendering
- DOI：10.2312/sr.20191215
- 本地：`raw/articles/anteru.net/2025-02-16_real-time-hybrid-hair-rendering.md`
