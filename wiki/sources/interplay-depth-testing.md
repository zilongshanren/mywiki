---
tags: [source, 渲染, 深度测试, D3D11]
date: 2026-04-14
sources: 1
---

# Order and Types of Depth Testing（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2013 年 1 月的短文，系统整理 D3D11 时代 depth testing 的几种阶段和它们与 pixel shader 的相互作用。

## 摘要

文章把 depth test 分成两类：**默认的 late depth test**——按 D3D / GL 规范应在 pixel shader 之后发生，目的只是正确 z 排序混合；以及**Early-Z / Hierarchical-Z**——在 shader 之前判定并剔除被遮挡像素，前者在像素级、后者基于分块的深度近似。Early-Z 默认开启，但**在几种情况下会被关掉**：pixel shader 输出 `SV_Depth`；使用 alpha test / alpha-to-coverage；pixel shader 写 UAV。D3D11（以及 OpenGL 4.2）给了两条救援通道：对于写深度的场景，**Conservative Depth**（`SV_DepthGreaterEqual` / `SV_DepthLessEqual`）让 shader 承诺方向单调，从而仍可跑 Early-Z；对于写 UAV 的场景，HLSL 的 `[earlydepthstencil]` 属性强制 GPU 在 shader 之前跑 depth / stencil。文章指出 Early-Z 和 Hierarchical-Z 并非 D3D11 才有——早就存在于 pre-D3D11 GPU，只是 D3D11 才暴露出调校它们的语义。Anagnostou 最后指向 [[fabian-giesen|Fabian Giesen]] 的《A Trip Through the Graphics Pipeline 2011》系列作为完整背景。

## 关键要点

- **Early-Z** vs **Hierarchical-Z**：一个像素级、一个 tile 级分块近似，合称 Early-Z 系列
- 四种破坏 Early-Z 的情形：写 depth、alpha test、alpha-to-coverage、写 UAV
- **Conservative Depth**：HLSL 的 `SV_DepthGreaterEqual` / `SV_DepthLessEqual` 恢复写深度场景的 Early-Z
- **`[earlydepthstencil]`**：HLSL 属性恢复写 UAV 场景的 Early-Z，但作者必须承诺 side effect 受深度测试控制
- Early-Z / Hi-Z 不是 D3D11 的新特性——硬件早就有，只是 D3D11 才给出调校旋钮

## 链接到的概念

- [[early-z-late-z]]
- [[conservative-depth]]
- [[hierarchical-z-buffer]]
- [[z-buffer]]
- [[fragment-shader]]
- [[kostas-anagnostou]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2013/01/17/depth_testing/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-01-17_order-and-types-of-depth-testing.md`
