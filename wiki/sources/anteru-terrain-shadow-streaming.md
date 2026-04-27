---
tags: [source, 渲染, 阴影, 地形, 流式加载]
date: 2026-04-27
sources: 1
---

# High-Quality Shadows for Streaming Terrain Rendering（Anteru's blog / Eurographics 2015）

[[matthaeus-chajdas|Matthäus G. Chajdas]]、Florian Reichl、Christian Dick、Rüdiger Westermann 发表于 Eurographics 2015 Short Papers，提出在流式地形渲染中处理昼夜循环动态阴影的实用方案。

## 摘要

大规模地形渲染通常依赖光线投射 + 数据流式缓存（ray-casting with streaming cache）。动态阴影之所以困难，是因为阴影计算需要访问全局地形数据，这与流式缓存策略直接冲突——光源可能从很远处投射阴影到当前可见区域。

论文将阴影分为两类处理：**近阴影**（near-shadows）使用当前缓存内容进行实时光线追踪；**远阴影**（far-shadows）则预计算整个昼夜循环并以极紧凑的格式存储，每个高度图采样仅需约 3 bit。这一分离策略显著减少了数据访问量和运行时开销。

## 关键要点

- 近/远阴影分治：近阴影实时光追（利用已有缓存），远阴影预计算
- 预计算远阴影只需约 3 bit/高度图采样，存储极为紧凑
- 避免了阴影计算对全局地形流式缓存的破坏
- 适用于昼夜循环场景（太阳低仰角时远处投影问题最突出）

## 链接到的概念

- [[terrain-shadow-streaming]]
- [[planet-terrain-dem-pipeline]]
- [[terrain-virtual-node-texture]]

## 原文

- 链接：https://anteru.net/research/high-quality-shadows-for-streaming-terrain-rendering
- 本地：`raw/articles/anteru.net/2025-02-16_high-quality-shadows-for-streaming-terrain-rendering.md`
