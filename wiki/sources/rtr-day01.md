---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 1 —— 渲染管线不是流水线

RTR 学习推送第 1 天。

## 摘要

介绍渲染管线的**四阶段**模型（Application/Geometry/Rasterization/Pixel）以及"瓶颈驱动"视角——管线并行运行，被最慢阶段拖住。功能阶段与物理实现的区分。**IMR vs TBDR** 两种 GPU 架构。

## 关键要点

- 管线四阶段：Application（CPU）、Geometry（GPU）、Rasterization（GPU）、Pixel（GPU）。
- **瓶颈决定帧率**——并行阶段被最慢阶段拖住。
- 优化原则：找瓶颈，只优化瓶颈阶段。
- **功能阶段 ≠ 物理实现**。
- **IMR（Immediate Mode Rendering）**：桌面 GPU（NVIDIA/AMD）。
- **TBDR（Tile-Based Deferred Rendering）**：移动 GPU（Mali/Adreno/Apple）。
- 瓶颈识别：降一半分辨率，FPS 大幅提升说明 Pixel 是瓶颈。

## 链接到的概念

- [[rendering-pipeline]]
- [[bottleneck-analysis]]
- [[tbdr-vs-imr]]

## 原文

- 链接到：[[raw/articles/real time rendering/day1]]
