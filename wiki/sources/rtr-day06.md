---
tags: [source, 渲染, real-time-rendering]
date: 2026-04-05
sources: 1
---

# Real-Time Rendering Day 6 —— 一帧的完整生命

RTR 学习推送第 6 天。

## 摘要

**跟随一个三角形走完整个管线**——数据变换、信息丢失、架构权衡的整合视角。桌面 vs 移动端带宽差异（1008 GB/s vs 40 GB/s）。TBDR 架构的带宽换复杂度。

## 关键要点

- 可见顶点量级：500k-5M/帧，Overdraw 3-10×。
- **带宽预算**：RTX 4090 16.8GB/帧 @ 60fps；Adreno 730 667MB/帧 @ 60fps。
- 移动端瓶颈是**带宽**（不是 ALU），反过来桌面是 ALU。
- **片上内存**比 DRAM 带宽高 100-200×。
- **SRP Batcher** 降状态 setup 开销，不降 DrawCall 数；**GPU Instancing** 降 DrawCall 数。
- 移动端 shader 优化优先级：纹理采样 → 精度降低 → 分支消除 → ALU 复杂度。
- Alpha cutout 草破坏 TBDR HSR → 4× 性能损失。

## 链接到的概念

- [[rendering-pipeline]]
- [[tbdr-vs-imr]]
- [[draw-call]]
- [[overdraw]]

## 原文

- 链接到：[[raw/articles/real time rendering/day06]]
