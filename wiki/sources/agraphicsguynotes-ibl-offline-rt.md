---
tags: [source, 渲染, pbr, ibl, 预计算, 实时渲染]
date: 2026-04-27
sources: 1
---

# Image Based Lighting in Offline and Real-time Rendering（A Graphics Guy's Note）

[[people/graphics-guy-notes|Jiayin Cao]] 发表于 2016 年 9 月的文章，对比 IBL 在离线与实时渲染中的实现路径，重点解析 UE4 的 Split-Sum 近似。

## 摘要

文章先以作者自己的离线渲染器为背景介绍 IBL 的核心思想：用一张 HDR 环境贴图代替场景中所有来自无穷远的入射辐射，通过 Monte-Carlo 路径追踪对半球积分进行无偏估计。离线部分只需用离散化反演法对 HDR 做重要性采样。实时部分以 UE4 的 [[split-sum-approximation|Split-Sum 近似]] 为主体：将镜面 IBL 积分拆成 prefiltered environment map 与 environment BRDF LUT 的乘积，把每帧 ~1024 次采样压缩为两次纹理查找。两项均预计算：环境贴图按 GGX 分布重要性采样后存入 mip 链（对应不同 roughness），BRDF LUT 存储 `(F₀·scale + bias)`，输入 `cosθₒ` 与 roughness。UE4 假设 `N = V`（入射方向 = 法线），这引入视角无关的偏差，但在实际场景里几乎不可察觉。

## 关键要点

- IBL 本质是用环境贴图替代场景全局入射辐射的 Monte-Carlo 积分。
- Split-Sum 将两个独立积分的乘积近似为各自积分的乘积，误差在视觉上可接受。
- `N = V` 假设是 UE4 实现额外引入的视角偏差，文章明确指出但认为可接受。
- environment BRDF LUT 仅为 2D 纹理（`cosθₒ, roughness`），运行时一次采样。
- 该方法为单次散射近似；高粗糙度金属的能量丢失需 [[ibl-multiple-scattering]] 补偿。

## 链接到的概念

- [[split-sum-approximation]]
- [[ibl-multiple-scattering]]
- [[microfacet-brdf]]
- [[physically-based-shading]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/image_based_lighting_in_offline_and_realtime_rendering/
- 本地：`raw/articles/agraphicsguynotes.com/2016-09-07_image-based-lighting-in-offline-and-real-time-rendering.md`
