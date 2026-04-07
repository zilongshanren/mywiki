---
tags: [渲染, 性能]
date: 2026-04-05
sources: 1
---

# 裁剪（Culling）

**在 CPU 端决定哪些对象不需要发给 GPU**。分层过滤，百万对象缩减到千级别。

## 层级

| 层级 | 依据 | 剔除什么 |
|---|---|---|
| **Frustum Culling** | 视锥体 | 不在相机视野内的 |
| **Occlusion Culling** | 被其它物体挡住 | 不可见的 |
| **Distance Culling / LOD** | 距离 | 远到看不清的（或降低精度） |
| **Contribution Culling** | 视觉贡献 | 屏幕上 <1 像素的 |

## 为什么层级

前面层级便宜（包围盒测试）但粗糙；后面层级精细但昂贵。先用便宜的大幅削减，再用昂贵的精修。

## GPU-Driven Culling

UE5 Nanite 等把 culling 移到 GPU，用 compute shader 并行剔除，突破 CPU 瓶颈。

## CPU 决策的重要性

**CPU 决定渲染什么；GPU 执行**。差的 CPU culling → GPU 被迫处理大量不可见对象 → GPU 资源浪费。

## 相关

- [[rendering-pipeline]]
- [[draw-call]]
- [[batching]]

## Sources

- [[sources/rtr-day02]]
