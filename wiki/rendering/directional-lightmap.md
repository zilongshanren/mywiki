---
tags: [rendering, lightmap, baked-lighting, spherical-harmonics]
date: 2026-04-27
sources: 1
---

# 方向性光照贴图（Directional Light Map）

方向性光照贴图是传统[[rendering/lightmap-baking-workflow|光照贴图]]的扩展，核心目标是让烘焙光照能响应法线贴图的逐像素法线变化，从而避免 flat、缺乏细节的漫反射外观。

## 传统光照贴图的局限

传统光照贴图将辐照度（irradiance）以积分形式存储：围绕几何法线对整个上半球积分，烘焙结果是一个与方向无关的标量（或 RGB）。这意味着运行时无论法线贴图法线指向何方，查到的光照值都相同——法线贴图只能影响高光，无法影响漫反射，表面因此显得平坦。

根本原因在于两难困境：若要在烘焙时按法线贴图法线积分，就需要对每个纹素储存完整的辐照度环境图；而光照贴图的一大优势恰恰是低内存占用。

## 球谐函数方案

一种方案是用[[rendering/spherical-harmonics|球谐函数]]（通常 L2，9 个系数/通道）近似辐照度环境图，存入光照贴图。运行时用表面法线重建。精度较好，但内存仍是传统光照贴图的数倍，额外运行时求值也有代价。

## Radiosity Normal Map（RNM）

Valve 提出的实用方案。不存储完整环境图，仅存储三个固定正交基方向下的辐照度值：

```
basis[0], basis[1], basis[2]  // 均匀覆盖半球的正交基
```

重建公式（Real-Time Rendering 版本，非 Valve 原论文版本——原论文有误）：

```
color = dot(n, basis[0])² * L[0]
      + dot(n, basis[1])² * L[1]
      + dot(n, basis[2])² * L[2]
```

因为三个基向量彼此正交，法线在三个基上的投影平方和恰好等于 1，无需额外归一化。

Source Engine 使用完整 RNM（三组 RGB 值）。UE3 移动端使用简化版本：三个标量强度值 + 一个辐照度颜色，法线只影响亮度而非颜色。

## 实际意义

方向性光照贴图是预计算光照与实时法线贴图结合的重要桥梁，在强调性能的平台（主机、移动）上广泛使用。其假设（Lambertian 表面、静态场景）与传统光照贴图相同，代价是额外 3× 的纹理内存（RNM）或更多（SH）。

## Sources

- [[sources/graphics-guy-directional-lightmap]]
