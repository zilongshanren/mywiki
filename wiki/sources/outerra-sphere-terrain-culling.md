---
tags: [source, rendering, culling, planet-engine]
date: 2026-04-27
sources: 1
---

# View Frustum Culling of Sphere-mapped Terrain（Outerra）

[[people/outerra-team]] 发表于 2012 年 11 月的文章，介绍在行星引擎中对球面 quad-tree 地形 tile 进行精确视锥剔除的方法。

## 摘要

平面地形的 tile 是轴对齐的，视锥剔除只需标准 AABB 测试。但球面地形的 tile 不仅朝向任意，还因球面投影导致仿射剪切变形，用 AABB 或 OBB 包裹会产生大量假阳性。文章提出将视锥平面变换到 tile 的剪切坐标系中，利用仿射变换保留面交性质的特点，在剪切空间内直接做 p/n-vertex 式的 AABB 测试，无需松散包围盒。由 tile 的 u、v 切向量构造旋转矩阵 R，把平面法线投影到局部空间后对 extents 取绝对值 dot，即为精确测试。该矩阵在 quad-tree 同层可缓存复用。

## 关键要点

- 球面 tile 的剪切变形在低层级 quad-tree 中是主导形变，用 OBB 包裹代价较高。
- 仿射变换（含剪切）保留平面相交关系，因此可以"把视锥搬进 tile 空间"。
- 构造 `R = [u | v | cross(u,v)]`，以转置方式变换视锥平面法线。
- extents 是 tile 在其局部坐标系中已知的半尺寸，测试完全等价于 p/n-vertex。
- R 矩阵可在某层级以下缓存，因为 u/v 向量变化很小。

## 链接到的概念

- [[sphere-mapped-terrain-culling]]
- [[view-frustum-culling-ryg]]
- [[culling]]

## 原文

- 链接：https://outerra.blogspot.com/2012/11/view-frustum-culling-of-sphere-mapped.html
- 本地：`raw/articles/outerra.blogspot.com/2012-11-17_view-frustum-culling-of-sphere-mapped-terrain.md`
