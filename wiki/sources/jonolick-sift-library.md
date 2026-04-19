---
tags: [source, 计算机视觉, SIFT, 单文件库]
date: 2026-04-14
sources: 1
---

# Scale Invariant Feature Transform (SIFT) Single File Library（Jon Olick）

[[jon-olick|Jon Olick]] 2025 年 1 月发布的 `jo_sift.h`——一个零依赖、纯 C、header-only 的 SIFT 实现。

## 摘要

SIFT（Scale Invariant Feature Transform）是计算机视觉里用于特征检测与描述的经典算法，在图像拼接、物体识别、三维重建中长期被依赖。它具有**尺度不变、旋转不变**以及**对噪声和部分遮挡鲁棒**的性质，描述子通常是 128 维向量。由于专利已过期，SIFT 现在可以在任意商业/个人项目中自由使用。`jo_sift.h` 按 Jon Olick 一贯的 STB 风格打包：单个 C header、无外部依赖、一个 API 做 keypoint 检测、另一个做匹配。这把 CV 能力下沉到了不适合引入 OpenCV 的场景——引擎工具链、资源处理器、嵌入式、快速原型——免去了 OpenCV 那种臃肿的依赖图。

## 关键要点

- SIFT 三要素：尺度不变（高斯金字塔 + DoG）、旋转不变（keypoint 主方向）、鲁棒性；
- 应用：图像拼接、物体识别、3D 重建；
- `jo_sift.h` 特性：header-only、零依赖、纯 C、专利过期后可自由使用；
- 定位：`stb_image.h` / `jo_jpeg.h` 一脉相承的单文件库哲学；
- 使用方式：检测 keypoints → 两图间匹配 keypoints。

## 链接到的概念

- [[sift-single-file-library]]
- [[jon-olick]]

## 原文

- 链接：https://www.jonolick.com/home/scale-invariant-feature-transform-sift-single-file-library
- 本地：`raw/articles/jonolick.com/2025-01-28_scale-invariant-feature-transform-sift-single-file-library.md`
