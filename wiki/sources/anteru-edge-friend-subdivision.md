---
tags: [source, 渲染, 几何处理, 细分曲面, gpu]
date: 2026-04-27
sources: 1
---

# Edge-Friend: Fast and Deterministic Catmull-Clark Subdivision Surfaces（Anteru's blog）

[[matthaeus-chajdas|Matthäus G. Chajdas]] 等发表的研究论文，介绍一种针对四边形网格的紧凑邻域数据结构 Edge-Friend，专为 GPU 上的实时 Catmull-Clark 细分曲面渲染而设计。

## 摘要

Catmull-Clark 细分曲面渲染的核心难点在于需要访问每条边的相邻四边形（邻域信息），而传统实现要么依赖硬件原子浮点加法，要么结构复杂难以并行。Edge-Friend 利用了一步细分后每个四边形可以唯一隐式关联两条边这一几何性质，使整个算法可以在**单个 compute shader kernel** 中完成，无需硬件原子浮点支持，且是完全确定性（deterministic）的。

数据结构本身紧凑，开销小；支持半光滑折缝（semi-smooth creases）、边界、动画与属性插值；拓扑变更时只需少量预处理，适合实时编辑与动画场景。

在 AMD Radeon RX 7900 XTX 上，对一个典型网格，算法可在 0.58ms 内生成并渲染 290 万三角形，整体吞吐量达数十亿三角形/秒量级。

## 关键要点

- 一步细分后两条边可隐式唯一关联到每个四边形，是算法能力的关键几何洞察
- 无需硬件原子浮点：只需最小同步，特别适合异步执行
- 单 compute shader 实现，简洁，便于嵌入现有渲染管线
- 支持折缝、边界、动画插值，覆盖主流生产需求
- 性能：290 万三角形生成 + 渲染仅 0.58ms（RX 7900 XTX）

## 链接到的概念

- [[catmull-clark-subdivision]]
- [[meshlets-and-mesh-shaders]]
- [[d3d12-work-graphs]]

## 原文

- 链接：https://anteru.net/research/edge-friend-fast-deterministic-catmull-clark-subdivision-surfaces
- 本地：`raw/articles/anteru.net/2025-02-16_edge-friend-fast-and-deterministic-catmull-clark-subdivision.md`
