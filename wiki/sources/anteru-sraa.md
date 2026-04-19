---
tags: [source, 渲染, 反走样, 延迟渲染]
date: 2026-04-19
sources: 1
---

# Subpixel Reconstruction Antialiasing（I3D 2011）

[[matthaeus-chajdas|Chajdas]]、McGuire、Luebke 发表于 **ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2011** 的论文。核心算法详见 [[subpixel-reconstruction-antialiasing]]。

## 摘要

**SRAA** 把**单像素（1×）着色**与**子像素可见性**组合起来，产生抗锯齿图像而不增加着色成本。它以 [[deferred-rendering|延迟着色]] 管线为目标（deferred 无法用 MSAA），作为一个 post-process 运行在**超分辨率的 depth + normal buffer** 之上，无需修改 shader。

类似 [[analytical-antialiasing|MLAA]]，但 SRAA 能**更好地尊重几何边界**，且运行时间**与场景和图像复杂度无关**。

SRAA 适合 shading-bound 应用。实测 1280×720 下 1.8 ms 完成，质量相当于 4–16× shading。只要应用每帧 shading 超过 1 ms（多数游戏在 5–10 ms），SRAA 就比 SSAA 净省。论文还给出通过降质换性能的若干简化版。

## 关键要点

- **子像素 visibility + 1× shading 的分离**：这是 SRAA 最核心的结构贡献。
- **几何边缘信息 > 彩色图边缘信息**：深度 + 法线的双边 reconstruction kernel 比 MLAA 的亮度边缘检测可靠得多。
- **固定成本**：不随场景复杂度变化，对 frame pacing 友好。
- 论文直接附了 CUDA kernel 源码——9 个 neighbors 的双边权重 + 9 次彩色 tap。

## 链接到的概念

- [[subpixel-reconstruction-antialiasing]]
- [[deferred-rendering]]
- [[analytical-antialiasing]]
- [[temporal-antialiasing]]
- [[matthaeus-chajdas]]

## 原文

- 链接：<https://anteru.net/research/subpixel-reconstruction-antialiasing>
- 本地：`raw/articles/anteru.net/2025-02-16_subpixel-reconstruction-antialiasing.md`
