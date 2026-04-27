---
tags: [source, 渲染, 光线追踪, BVH, 加速结构, AABB, TLAS, BLAS, DirectX12]
date: 2026-04-27
sources: 1
---

# Ray Tracing Acceleration Structures（Alain Galvan / alain.xyz）

[[people/alain-galvan]] 发表于 2022 年 4 月的文章，从理论到 API 实现全面介绍光线追踪加速结构，包含 AABB/Triangle 相交测试、BVH 数据结构、SAH 启发式、Morton 码、DirectX 12 TLAS/BLAS 构建代码及 HLSL 光追 shader 示例。

## 摘要

文章以 AABB 和 Triangle 相交测试为起点，解释 GPU 厂商为何将其映射到硬件 ASIC（AMD RDNA2 即如此）。BVH 是核心数据结构，支持多种变体：AABB 树、Wide BVH（每节点多子树）、SAH 优化分割、Morton 码加速构建。KD-Tree 对比 BVH 更轻量但遍历较慢。SAH 通过子节点 AABB 面积比估计命中概率，PLOC 等 GPU 构建器在合并阶段使用 SAH。Morton 码将 3D 位置编码为 32 位哈希，通过 bit 交织 XYZ 分量实现空间排序。DX12/Vulkan 的两级 BVH（BLAS + TLAS）允许静态/动态物体分别管理；文章附有完整 DirectX 12 C++ 代码展示 scratch buffer 分配、BLAS/TLAS 构建命令提交，以及 HLSL raygen/hit/miss shader 框架。

## 关键要点

- 三角形应通过索引列表引用而非直接嵌入节点，便于 BVH 重排时不重写几何体
- 最简 BVHNode 可压缩至 64 字节（左右 AABB + 两个子树指针）
- SAH 公式：`SA(child)/SA(parent) * N_triangles_in_child`，用于评估分割方案
- Morton 码构建：对每节点 bbox 中心做 scene_scale 归一化后编码为 Z-order curve
- DX12 加速结构 build flag：`PREFER_FAST_TRACE`（高质量遍历）vs `PREFER_FAST_BUILD`（快速重建）
- Vulkan/DX12 `TraceRay` 在 AMDIL 层变为 `image_bvh_intersect_ray` + `image_bvh_triangle_intersect_ray` 两条 ASIC 指令

## 链接到的概念

- [[rendering/bvh-construction]]
- [[rendering/bvh-traversal-hardware]]
- [[rendering/ray-tracing-api-debate]]
- [[rendering/hybrid-raytracing-pipeline]]

## 原文

- 链接：https://alain.xyz/blog/ray-tracing-acceleration-structures
- 本地：`raw/articles/alain.xyz/2022-04-24_ray-tracing-acceleration-structures.md`
