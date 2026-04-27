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
- [[cached-shadowmaps]] —— 时间维度的「culling」：帧间不变的投射者不重绘
- [[occlusion-culling]] —— 遮挡剔除的具体方案（HZB 查询 / SPU 软光栅）
- [[hierarchical-z-buffer]] —— max-downsample 金字塔：遮挡剔除的基础数据结构
- [[unity-procedural-mesh]] —— 新手最容易踩的坑：winding order 写反 → 整个面被背面剔除
- [[gpu-driven-grass-tiles]] —— compute shader 做瓦片级 frustum vote + scan compact + draw indirect 的一个完整落地
- [[view-frustum-culling-ryg]] —— ryg 对 AABB-vs-frustum 的完整方法链：从 8 顶点 baseline 到 SPU 上 ≈24 cycle/box 的 SIMD p/n-vertex
- [[stingray-simd-sphere-oobb-culling]] —— Stingray 的暴力 SoA + SIMD + 多线程两级剔除实现

## Sources

- [[sources/rtr-day02]]
- [[sources/bruop-frustum-culling]] — Bruop：OBB clip-space 顶点测试 + AVX2 手写 intrinsics，10k 对象从 8.2 ms 降到 3.3 ms
- [[sources/outerra-sphere-terrain-culling]] — Outerra：球面 quad-tree tile 的仿射剪切空间精确视锥剔除
