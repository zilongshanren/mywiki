---
tags: [source, 渲染, 阴影, 体积, 半透明, 矩]
date: 2026-04-14
sources: 1
---

# Beyond Hard Shadows: Moment Shadow Maps for Single Scattering, Soft Shadows and Translucent Occluders（Peters et al.）

[[christoph-peters]]、Cedrick Munstermann、Nico Wetzstein、Reinhard Klein 在 I3D 2016 的论文摘要页。把前一年的 [[moment-shadow-mapping|MSM]] 推广到三个「可过滤阴影」的经典应用。

## 摘要

前作 MSM 解决了「可过滤硬阴影」。本文沿用同一套四阶矩 + Hausdorff 矩问题闭式解的框架，把 MSM 套到另外三类需要对 shadow map 做滤波的应用上：

1. **Prefiltered single scattering**——参与介质里的体积阴影，原来由 Convolution Shadow Maps 处理，MSM 给出更少存储、更少 ringing 的替代品。
2. **Moment Soft Shadow Mapping（MSSM）**——Variance Soft Shadow Maps 的替代品，半影更干净、漏光显著减少。
3. **Moment Translucent Occluders**——Fourier Opacity Map 的替代品，用于半透明 occluder（烟、叶子、织物）。

三者的统一母题是：**凡是能把待滤波量写成「某个带界分布的一个函数的期望」的应用，都可以存该分布的矩并在运行时解矩问题重建。** 论文同时发布了一个可执行 demo，现场演示三类应用以及与 VSM/ESM/CSM 的并排对比；一个带文档的 shader 代码包单独下载。

## 关键要点

- **MSM 母题的三次复用**：single scattering、soft shadows、translucent occluders 可以共享同一张 moment shadow map 与同一套解码器。
- **相对基线的提升**：参与介质里 ringing 更少；soft shadow 漏光改善；半透明遮挡物存储预算更紧。
- **exponential VSM + 16-bit 量化**：demo 里把 EVSM 也塞进了 16-bit 路径用作对照。
- **可执行 demo + shader 代码**：罕见的「直接能跑」的图形学论文配套资源。
- **延伸 JCGT 版本**：摘要页备注有一个被邀请到 Journal of Computer Graphics Techniques 的加长版。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[christoph-peters]]
- [[shadow-mapping-basics]]
- [[volumetric-fog-froxels]]

## 原文

- 链接：<http://momentsingraphics.de/I3D2016.html>
- DOI：<https://doi.org/10.1145/2856400.2856402>
- 本地：`raw/articles/momentsingraphics.de/2016-01-01_beyond-hard-shadows-moment-shadow-maps-for-single-scattering.md`
