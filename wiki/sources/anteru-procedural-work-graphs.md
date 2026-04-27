---
tags: [source, 渲染, GPU, work-graphs, 程序化生成, 网格着色器]
date: 2026-04-27
sources: 1
---

# Real-Time Procedural Generation with GPU Work Graphs（anteru.net）

[[matthaeus-chajdas]] 发表于 2025 年 2 月的研究页，介绍将 [[d3d12-work-graphs|GPU Work Graphs]] 用于实时程序化内容生成的工作。

## 摘要

Work Graphs 的节点可以动态生成新的下游工作负载，这与递归式程序化算法的天然结构高度契合。论文将 Work Graphs 与 GPU 光线追踪、程序化 Mesh Shader 结合，构建了一套**实时程序化生成系统**，不需要额外的数据结构——现代渲染引擎已有的数据就够用。系统展示了实时编辑能力：在 AMD Radeon RX 7900 XTX 上，3.74 ms 内生成 79,710 个实例放置到场景中。

## 关键要点

- **Work Graph 用于程序化递归**：节点动态产生子工作，天然匹配递归结构（L-system、分形、实例化树等），无需 CPU 介入。
- **三技术组合**：Work Graphs（调度）+ Mesh Shaders（几何生成）+ Ray Tracing（可见性 / 碰撞），三者在 GPU 内部接力。
- **零额外数据结构**：系统设计让其可以直接集成进标准现代渲染引擎，降低移植成本。
- **实时编辑**：79,710 实例在 3.74 ms，意味着可以在编辑器里交互式预览程序化结果。
- **与 [[d3d12-work-graphs]] 的关系**：前者侧重 API 机制与性能特性；本文展示一个具体应用场景——把图形管线以外的"内容生成"工作流迁移进 Work Graphs。

## 链接到的概念

- [[d3d12-work-graphs]]
- [[procedural-work-graph-generation]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/research/real-time-procedural-generation-with-gpu-work-graphs
- 本地：`raw/articles/anteru.net/2025-02-16_real-time-procedural-generation-with-gpu-work-graphs.md`
