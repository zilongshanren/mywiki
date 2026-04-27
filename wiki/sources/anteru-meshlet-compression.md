---
tags: [source, 渲染, 几何处理, meshlet, 压缩, mesh-shader]
date: 2026-04-27
sources: 1
---

# Towards Practical Meshlet Compression（Anteru's blog）

[[matthaeus-chajdas|Matthäus G. Chajdas]] 等提出的 meshlet 专用压缩编解码方案，以 mesh shader 内 GPU 并行解压为核心目标设计。

## 摘要

Meshlet 是 [[meshlets-and-mesh-shaders|mesh shader 管线]]的核心数据单元，但其索引缓冲和顶点属性的存储开销不可忽视。本文针对 meshlet 特性设计了一个压缩 codec：索引缓冲方面，通过将三角形排列为**最优广义三角带（Generalized Triangle Strips, GTS）**来压缩，GTS 生成以混合整数线性规划（MILP）建模；顶点属性方面，采用基于用户偏好的无缝（crack-free）量化。整体索引缓冲压缩率达 **16:1**（相对于传统顶点管线）。

测试场景中，1550 万三角形在 AMD Radeon RX 7900 XTX 上解压 + 渲染仅需 0.59ms，与 Edge-Friend 细分数据在同一数量级。

## 关键要点

- 索引缓冲：三角形排列成最优 GTS，以 MILP 求解，压缩率 16:1
- 顶点属性：crack-free 量化，由用户精度需求驱动
- GPU 解压在 mesh shader 内并行执行，无需单独解压 pass
- 与 [[anteru-edge-friend-subdivision|Edge-Friend]] 均在同一 GPU 上测试，吞吐量相当

## 链接到的概念

- [[meshlet-compression]]
- [[meshlets-and-mesh-shaders]]

## 原文

- 链接：https://anteru.net/research/towards-practical-meshlet-compression
- 本地：`raw/articles/anteru.net/2025-02-16_towards-practical-meshlet-compression.md`
