---
tags: [人物, 作者, 渲染, metal, apple]
date: 2026-04-14
sources: 8
---

# Warren Moore

**Warren Moore** 是 iOS / macOS 图形开发者，长期维护博客 [metalbyexample.com](https://metalbyexample.com) 与同名电子书 *Metal by Example*。2014 年 iOS 8 发布 [[metal-api-overview|Metal]] 的同一个夏天，他开始在博客上连载「Up and Running with Metal」系列，把 Apple 这套低层图形 API 从 `CAMetalLayer` / `MTLDevice` / `MTLCommandQueue` 这些基础对象一路讲到 3D 渲染、计算内核和色调映射，是中文圈之外公认的 Metal 入门一手资料。

## 风格

- **从「能跑」开始**：第一篇教程的目标只是把屏幕清成红色；每篇只引入必须的新对象，不贪多。
- **对协议而非类**：他刻意解释了 Metal 为什么大量用 `id<MTLDevice>` 这种 Objective-C 协议——暴露行为、隐藏具体实现。
- **评论区即 FAQ**：文章底下的评论里，他逐条回复初学者的配置、alignment、Retina drawableSize、OS X 移植等问题，是阅读原文之外额外的知识来源。
- **立场诚实**：在「Whats and Wherefores」里，他直言 Metal 本质上仍是**另一层抽象**，只是现在你可以选的最低的一层；也直言当时（2014）的 Metal 对 Mac 上的分立 GPU 架构并不友好。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Up and Running with Metal, Part 1: Clearing the Screen | [[metal-api-overview]]、[[cametal-layer-drawable]] |
| Up and Running with Metal, Part 2: Drawing Triangles | [[metal-shading-language-basics]]、[[metal-api-overview]] |
| The Whats and Wherefores of Metal | [[metal-api-overview]]、[[rendering-api-depth]] |
| Linear Algebra for Graphics Programming | [[mvp-transform]]、[[shader-vector-math-primer]]（支线参考文）|
| Up and Running with Metal, Part 3: Lighting and Rendering in 3D | [[metal-3d-rendering-pipeline]]、[[normalised-blinn-phong-shader]] |
| Feature Sets and Capabilities | [[metal-api-overview]] 的 feature-set 小节 |
| Textures and Samplers in Metal | [[metal-texture-sampler]] |
| Fundamentals of Image Processing in Metal | [[metal-compute-image-filter]] |

## 相关
- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[cametal-layer-drawable]]
- [[rendering-api-depth]]
- [[draw-call]]
- [[metal-3d-rendering-pipeline]]
- [[metal-texture-sampler]]
- [[metal-compute-image-filter]]
- [[metal-decade-history]] —— 2024 年十周年双篇回顾（早期 + 现代）
- [[hdr-video-edr-metal]] —— 2025 年 AVFoundation + Metal 完整 HDR 视频管线 + PQ/HLG tonemapping shader
- [[metal-4-api-redesign]] —— 2025 年 WWDC25 Metal 4 大版本的 API 重塑指南
- [[slug-gpu-glyph-rendering]] —— 2026 年专利释放后第一篇 Slug 算法在 Metal 上的最小实现

## Sources
- [[sources/metalbyexample-up-and-running-1]]
- [[sources/metalbyexample-up-and-running-2]]
- [[sources/metalbyexample-whats-and-wherefores]]
- [[sources/metalbyexample-linear-algebra]]
- [[sources/metalbyexample-up-and-running-3]]
- [[sources/metalbyexample-feature-sets]]
- [[sources/metalbyexample-textures-and-samplers]]
- [[sources/metalbyexample-image-processing]]
- [[sources/metalbyexample-decade-early-years]]
- [[sources/metalbyexample-decade-modern-era]]
- [[sources/metalbyexample-hdr-video]]
- [[sources/metalbyexample-metal-4-basics]]
- [[sources/metalbyexample-slug]]
