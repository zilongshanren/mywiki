---
tags: [source, rendering, shader, unity, blur, convolution, post-processing]
date: 2026-04-14
sources: 1
---

# Image Effects Part 3 — Blurring Algorithms（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 3 篇，系统讲了 Box Blur 和 Gaussian Blur 的卷积原理、可分离优化、多 pass 实现、以及 Super Mario Odyssey 边缘渐强模糊的复现。

## 摘要

文章首先引入**卷积核（kernel）**的概念：一个奇数边长的 NxN 矩阵，以像素为单位滑过图像，每个位置下把矩阵值乘上对应像素颜色、累加、再除以矩阵元素总和，得到中心像素的加权平均。全 1 矩阵就是 **Box Blur**；利用"可分离卷积"的性质，NxN 的 2D 卷积可拆成一次 1xN 横向加一次 Nx1 竖向，把 O(N²) 采样降到 O(2N)，但需要两个 shader pass——作者特别提醒**单 pass 之间不会自动把结果写回 `_MainTex`**，必须在 C# 里用 `RenderTexture.GetTemporary` 搭一块临时 RT 用 `Graphics.Blit(src, tmp, mat, 0); Graphics.Blit(tmp, dst, mat, 1)` 明确 pass 索引。接着把 Box Blur 的"平均"权重替换为 **Gaussian 函数** `G(x) = 1/(σ√2π) · exp(-x²/2σ²)`，得到 Gaussian Blur——由于高斯也是可分离的，一维 1D 高斯跑两遍即可。文章给出了单 pass 版本（双层 for loop，采样数退回到 N²）作为对照。最后用"到图像中心的距离"驱动 σ，实现 Super Mario Odyssey 式的**边缘强、中心清晰**的镜头模糊。一路穿插了 `_MainTex_TexelSize`（1/宽度 的 uv 单位步长）、`CGINCLUDE` 共享头、wrap mode（Clamp / Repeat / Mirror）对边缘像素的影响等实操细节。

## 关键要点

- **卷积**是把一个核矩阵在图像上滑动、乘加、归一化的过程；image effect 的每个邻域采样都要自己在 fragment shader 里手动 `tex2D`。
- **可分离卷积**：Box Blur 和 Gaussian Blur 都能拆成横+竖两次 1D 卷积，把复杂度从 N² 降到 2N——这是所有"全屏模糊"后处理的性能基础。
- 多 pass shader 在 Unity 里通过 `Graphics.Blit(src, tmp, mat, passIndex)` 显式驱动；中间必须用临时 RT 否则第二 pass 读不到第一 pass 的结果。
- `_MainTex_TexelSize.xy = (1/width, 1/height)`，是把"像素偏移"映射回 uv 空间的标准方式。
- Gaussian 权重中心高、边缘低，对"硬边"表现比 Box Blur 好得多；σ（`_Spread`）控制 falloff 宽度。
- **空间变化的 σ**：把 `getSigma(uv)` 写成到屏幕中心的距离，就能做"边缘逐渐模糊、中心保持锐利"——这是 Super Mario Odyssey blur 滤镜的实现。
- 纹理 wrap mode（Clamp / Repeat / Mirror）决定越界采样的行为；image effect 默认 Clamp。

## 链接到的概念

- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[unity-image-effect-basics]]
- [[sampler-filter-wrap-modes]]
- [[unity-grabpass-blur]]

## 原文

- 链接：https://danielilett.com/2019-05-08-tut1-3-smo-blur/
- 本地：`raw/articles/danielilett.com/2019-05-08_image-effects-part-3-blurring-algorithms.md`
