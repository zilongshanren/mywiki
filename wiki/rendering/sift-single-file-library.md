---
tags: [计算机视觉, 特征检测, 单文件库, SIFT, 图像匹配]
date: 2026-04-14
sources: 1
---

# SIFT 单文件库（jo_sift.h）

**SIFT（Scale Invariant Feature Transform）** 是 David Lowe 1999/2004 年提出的经典特征检测+描述子算法，长期是图像拼接、物体识别、三维重建的基础工具。[[jon-olick|Jon Olick]] 在 SIFT 专利到期后（2020 年），按照他一贯的 STB 风格，把它打包成了一个**零依赖的单文件 C header**——`jo_sift.h`。

## SIFT 的三个特性

- **尺度不变**：不同尺度上检测同一个特征点，通过高斯金字塔 + DoG（Difference of Gaussians）在尺度空间里找极值；
- **旋转不变**：给每个 keypoint 赋一个主方向（基于局部梯度直方图），描述子在该方向下计算；
- **鲁棒**：在部分遮挡、一定程度噪声和光照变化下仍能稳定匹配。

描述子通常是 128 维向量，编码 keypoint 周围的梯度结构，两张图之间通过最近邻 + ratio test 做匹配。

## jo_sift.h 的定位

工程美学和 `stb_image.h`、`jo_jpeg.h` 一脉相承：

- **Header-only**：一个 `.h` 文件丢进项目就能用，没有外部依赖，不需要单独编译链接；
- **纯 C**：便于绑定到任何语言或嵌入到资源管道；
- **专利已过期**：商业和个人项目都可自由使用。

典型用法是调用"检测 keypoints → 在两张图间匹配 keypoints"两个 API，用于全景拼接、图像对齐、基础的物体识别原型或者作为其他 pipeline 的前置步骤。

## 工程观点

Jon Olick 常年在维护 `jo_*.h` 系列（WAV writer、GIF writer、MPEG writer、ADPCM encoder、jo_nn.h 神经网络等），背后的一贯理念是：**一个问题一个文件、默认能 build、能读完**。SIFT 本来是很多 CV 库的重量级依赖（OpenCV 以前甚至把它关进 `xfeatures2d` contrib 模块），现在有了 single-file 版本，可以把 CV 能力下沉到不适合引入 OpenCV 的场景（引擎工具链、资源处理器、嵌入式）。

## Sources

- [[sources/jonolick-sift-library]]
