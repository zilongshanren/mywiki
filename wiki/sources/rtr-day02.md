---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 2 —— Application 阶段：CPU 在做什么

RTR 学习推送第 2 天。

## 摘要

**CPU 在渲染里作为决策者**——决定渲染什么、怎么渲染。介绍 Culling 层级、Draw Call 的真实成本、Batching 手段、GPU Instancing、SRP Batcher、Compute Shader。

## 关键要点

- Culling 层级：Frustum → Occlusion → Distance (LOD) → Contribution。
- **Draw Call 主成本是状态切换**，不是 GPU 执行。
- 状态切换（Shader/Texture/Blend）导致 GPU pipeline flush。
- **SRP Batcher** 用持久化 Constant Buffer 避免状态切换。
- **GPU Instancing** 真·合批，减少 Draw Call 数量。
- Mobile CPU 特别珍贵（功耗/热限制）。Vulkan/Metal 的移动端价值是降低 driver overhead。
- 中端 Android 200-300 Draw Call 就成瓶颈。

## 链接到的概念

- [[draw-call]]
- [[culling]]
- [[batching]]
- [[rendering-pipeline]]

## 原文

- 链接到：[[raw/articles/real time rendering/day2]]
