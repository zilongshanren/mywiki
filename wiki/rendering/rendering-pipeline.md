---
tags: [渲染, 核心概念, real-time-rendering]
date: 2026-04-05
sources: 2
---

# 渲染管线（Rendering Pipeline）

实时渲染的**四阶段**模型，每一阶段由不同处理器承担不同角色。

## 四阶段

| 阶段 | 位置 | 职责 |
|---|---|---|
| **Application** | CPU | 决策——渲染什么、怎么渲染 |
| **Geometry Processing** | GPU | 顶点变换、投影、剪裁 |
| **Rasterization** | GPU | 从三角形到 fragment |
| **Pixel Processing** | GPU | fragment shader + merging（深度/模板/混合） |

## 它不是流水线——它是瓶颈驱动的并行系统

> "The pipeline stages execute in parallel, but they are stalled until the slowest stage has finished its task."

虽然叫 pipeline，它其实是**并行**运行的——各阶段同时在处理不同帧/批次的数据。**整体帧率被最慢阶段拖住**。

三明治工厂类比：三个工人分别需要 20s/30s/20s 处理一个三明治；整体速度被 30s 那位决定。优化另两位是浪费。

## 瓶颈识别

- **降低分辨率一半**：如果 FPS 大幅提升 → Pixel Processing 是瓶颈。
- **如果 FPS 几乎不变** → CPU 或 Geometry 是瓶颈。

进一步识别看 [[bottleneck-analysis]]。

## 功能阶段 vs 物理实现

教科书阶段图是**功能分层**，不代表物理硬件——现代 GPU 内部的 unified shader architecture 让 vertex/fragment shader 共享同一堆 ALU 核。[[tbdr-vs-imr|TBDR 架构]]更是完全重新排列了执行顺序。

## 每一阶段的详解

- [[draw-call]]、[[culling]]、[[batching]]（Application 阶段）
- [[mvp-transform]]、[[coordinate-spaces]]、[[z-buffer]]（Geometry Processing）
- [[rasterization]]、[[aliasing]]、[[msaa-ssaa]]（Rasterization）
- [[pineda-edge-rasterization]]、[[hierarchical-rasterization]]、[[triangle-setup]]（光栅化硬件实现）
- [[fragment-shader]]、[[early-z-late-z]]、[[alpha-blending]]（Pixel Processing）

## 相关

- [[bottleneck-analysis]]
- [[tbdr-vs-imr]]
- [[overdraw]]
- [[unity-procedural-mesh]] —— 用 Unity Mesh API 从零喂 vertex/index buffer 的最小例子
- [[metal-api-overview]] —— Metal 如何用显式对象图把这条管线落到 iOS
- [[cametal-layer-drawable]] —— iOS 上 swapchain 的落地形式

## Sources

- [[sources/rtr-day01]]
- [[sources/rtr-day06]]
