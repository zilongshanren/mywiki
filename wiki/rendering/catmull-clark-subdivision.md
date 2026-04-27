---
tags: [渲染, 几何处理, 细分曲面, gpu, compute-shader]
date: 2026-04-27
sources: 1
---

# Catmull-Clark 细分曲面（实时 GPU 实现）

Catmull-Clark 细分曲面是工业界标准的平滑曲面表示，广泛用于离线影视渲染（OpenSubdiv、RenderMan）。在**实时 GPU 管线**中实现它的核心难点是：每条边需要访问相邻四边形的邻域信息，而 GPU 并行模型对全局邻域访问极不友好。

## 传统实现的障碍

经典的逐顶点细分规则（Catmull-Clark weights）需要收集相邻顶点与面，这意味着多个线程可能同时读写同一个顶点。传统做法依赖**硬件原子浮点加法**（如 CUDA `atomicAdd`、DX12 InterlockedAdd）来汇聚相邻贡献，但这引入了不确定性（浮点加法不满足交换律在 IEEE 意义下）和硬件依赖。

## Edge-Friend 数据结构

[[matthaeus-chajdas|Chajdas]] 等提出的 **Edge-Friend** 方案利用了一步细分后一个几何性质：

> 一步细分后，每个原始四边形可以唯一、隐式地关联到两条边。

这一观察允许把邻域信息以**紧凑、无冲突**的方式预编码到数据结构里，使整个细分算法能在**单个 compute shader kernel** 内完成，不需要原子浮点、不需要多 pass 同步，结果是完全确定性的。

具体特性：
- 支持半光滑折缝（semi-smooth creases）、边界、动画与属性插值
- 拓扑变更时预处理量极小，适合实时编辑和骨骼动画
- 异步执行友好（最小同步屏障）
- 性能：290 万三角形 0.58ms（AMD RX 7900 XTX）

## 与 Mesh Shader 的关系

Edge-Friend 的输出（细分后的三角形网格）可以直接对接 [[meshlets-and-mesh-shaders|mesh shader 管线]]，也可以作为 [[meshlet-compression|meshlet 压缩]]的上游输入。从 Catmull-Clark 曲面到最终帧的整个几何路径都可以驻留在 GPU 上，无需 CPU 回读。

## 相关

- [[meshlets-and-mesh-shaders]]
- [[meshlet-compression]]
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-edge-friend-subdivision]]
