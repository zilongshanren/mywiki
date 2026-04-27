---
tags: [source, rendering, lightmap, spherical-harmonics]
date: 2026-04-27
sources: 1
---

# Directional Light Map from the Ground Up（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2015 年 6 月的文章，从渲染方程出发，逐步推导传统光照贴图的数学原理，再解释方向性光照贴图（Directional Light Map）如何解决法线贴图无法生效的问题。

## 摘要

传统光照贴图将每个采样点的辐照度（irradiance）烘焙到纹理中，基于三个假设：纯漫反射表面（Lambertian）、静态几何体、静态光源。其缺陷在于辐照度积分是围绕几何法线而非法线贴图法线进行，导致法线贴图变化无法在光照中体现，表面显得平坦。方向性光照贴图通过在烘焙时存储更多方向信息来解决此问题。文章介绍了两类方案：一是用球谐函数（Spherical Harmonics）近似辐照度环境图，精度高但内存开销大；二是 Valve 提出的 Radiosity Normal Map（RNM），仅存三个正交基方向下的辐照度，运行时按法线加权混合，在实践中效果良好且开销可控。Source Engine 采用完整 RNM，UE3 移动端使用简化版本（一个辐照度 + 三个强度权重）。

## 关键要点

- 光照贴图本质是辐照度图（irradiance map），Lambertian BRDF 将渲染方程简化为 `Lo = (ρ/π) × E`，使得仅存储 E 即可
- Radiosity 算法通过迭代传播能量来计算烘焙值，不适合非 Lambertian 材质
- 方向性光照贴图的核心矛盾：想要支持动态法线，就需要每点都存完整辐照度环境图，但内存无法承受
- RNM 用三个正交基方向的辐照度近似，重建公式 `color = Σ dot(normal, basis[i])² × lightmap_color[i]`，因正交性无需归一化
- UE3 移动端版本：三数值只编码亮度变化，不支持颜色变化——是性能与质量的折中

## 链接到的概念

- [[rendering/lightmap-baking-workflow]]
- [[rendering/spherical-harmonics]]
- [[rendering/diffuse-lighting-lambertian]]
- [[rendering/radiometry-integral-view]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/directional_light_map_from_the_groud_up/
- 本地：`raw/articles/agraphicsguynotes.com/2015-06-24_directional-light-map-from-the-ground-up.md`
