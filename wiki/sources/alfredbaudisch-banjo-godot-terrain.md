---
tags: [source, 渲染, 复古, godot, n64, vertex-color, 地形]
date: 2026-04-19
sources: 3
---

# Project Style：Godot 里复刻 Banjo-Kazooie N64 地形（Alfred Baudisch）

[[alfred-baudisch]] 在自建博客的 `/project-style/` 子站点里把这组实验拆成三篇栏目索引——Photo Texture、Shaders、Vertex Colors——实际指向**同一个项目**：在 Godot 的 Visual Shader 系统里重现《Banjo-Kazooie》（任天堂 64）那种"富丽但廉价"的地形观感，并把它扩展成一套可 runtime 编辑的 dirt/clean paint 流程。

## 摘要

Banjo-Kazooie 当年在 N64 内存和带宽双重卡脖子的条件下，通过**把颜色变化烘焙进顶点色**、用少量 tiling 纹理做 decal blending 的方式堆出视觉层次。Baudisch 的项目用 Godot 的 Visual Shader 直接把这套数据通路复原：mesh 自带 vertex color（含 alpha），shader 以其作为乘色项和多层纹理混合权重，单次采样就得出 painterly 效果。进一步地，他把同一机制拿来做运行时 dirt paint——笔刷覆盖的顶点直接改 vColor.a，下一帧 GPU 按新权重混合，规避了 runtime splat map 的 RT 成本。工具链上 Blender 负责 vertex paint，Godot 负责 shader 与运行时，两端都原生支持顶点色，不需自建资产流水线。

> 说明：这三篇源文件本身是博客的分类列表页，正文主要是每个 sub-post 的开头段重复摘录，深度信息不在单页里。本摘要综合三页的片段内容概括其核心项目。

## 关键要点

- vertex color RGB 作 tint、alpha 作 splat 权重，是 N64 时代的"穷人 splatmap"，数据通路极简；
- Godot Visual Shader 原生支持读取 vertex color，配 Blender 的 vertex paint 模式形成完整工具链；
- runtime 通过修改顶点色实现 dirt paint，相对动态 splat map 省掉 RT 与笔刷烘焙的复杂度，代价是精度受 mesh 密度限制；
- 风格意义：复古不靠后处理模拟，而是**把当年的技术约束直接当美学底层**沿用（参见 [[retro-rendering-techniques]]）。

## 链接到的概念

- [[banjo-kazooie-vertex-color-terrain]]
- [[retro-rendering-techniques]]
- [[terrain-splatmap-shader-graph]]
- [[godot-visual-shaders]]

## 原文

- 链接：<https://alfredbaudisch.com/project-style/photo-texture/>、<https://alfredbaudisch.com/project-style/shaders/>、<https://alfredbaudisch.com/project-style/vertex-colors/>
- 本地：
  - `raw/articles/alfredbaudisch.com/2025-11-30_project-style-photo-texture.md`
  - `raw/articles/alfredbaudisch.com/2025-11-30_project-style-shaders.md`
  - `raw/articles/alfredbaudisch.com/2025-11-30_project-style-vertex-colors.md`
