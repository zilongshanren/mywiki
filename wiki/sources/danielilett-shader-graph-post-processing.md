---
tags: [source, unity, shadergraph, urp, 后处理]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics (Part 12 - Post Processing)（danielilett.com / Daniel Ilett）

[[daniel-ilett]] 2025 年 10 月 Shader Graph Basics 收官期：用 URP Fullscreen Shader Graph + Full Screen Pass Renderer Feature 做屏幕空间后处理。

## 摘要

URP 自 2022 起把 Fullscreen Graph 列为官方后处理直出路径——Shader Graph 里选 Fullscreen target，图里通过 URP Sample Buffer 节点拿 Blit Source 与 Scene Normals，Renderer Feature 里拖 material 挂到特定 Inject Point。示例做两个：灰度滤镜（Luminance 后 Lerp 回去）、颜色 + 法线双梯度 outline（采样 color 与 normal 做 Sobel，用 fwidth 控制线宽）。

## 关键要点

- Fullscreen Graph + Full Screen Pass Renderer Feature = Shader Graph 直出后处理
- `URP Sample Buffer` 节点是拿 Blit Source / SceneNormalsTexture 的官方入口
- 颜色 + 法线双梯度 outline 比单纯深度 outline 更鲁棒

## 链接到的概念

- [[fullscreen-shader-graph-urp]]
- [[sobel-edge-detection]]

## 原文

- 链接：<https://danielilett.com/2025-10-14-unity-shader-graph-basics-part-12-post-processing/>
- 本地：`raw/articles/danielilett.com/2025-10-14_unity-shader-graph-basics-part-12-post-processing.md`
