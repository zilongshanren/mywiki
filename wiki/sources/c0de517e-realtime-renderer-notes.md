---
tags: [source, 渲染管线, 延迟渲染, 前向渲染, 实时渲染]
date: 2026-04-27
sources: 1
---

# Notes on real-time renderers（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2014 年 9 月的文章，系统比较实时渲染器的四种主流管线架构：Forward、Forward+、Deferred Shading、Deferred Lighting。

## 摘要

这是一篇工程性笔记，以利弊对照表的形式整理了四种管线的核心权衡。文章写于次世代主机（PS4/Xbox One）普及初期，因此对显存带宽、着色器排列组合爆炸、MSAA 可行性的讨论具有鲜明的时代背景。Pesce 的总体判断是：没有一种管线是万能的，选择取决于光源数量/类型、材质复杂度、硬件带宽和对透明物体的需求。他对「Tiled/Clustered 能显示数千灯光」的演示持批评态度：廉价无阴影点光源是 GI 的糟糕替代，制造的是圆形光斑而非真实间接光，并不是真正的收益。

## 关键要点

- **Forward**：基线最快，内存最小，支持 MSAA；缺点是动态灯光剔除弱，Shader 排列组合爆炸
- **Forward+（Light Indexed）**：用 Tile/Cluster 代替几何切割，解决动态灯光剔除；但仍需完整深度预通，shadowmap 必须全部预生成
- **Deferred Shading**：纹理与光照解耦，支持多 Pass 贴花/特效，Shader 变体少；带宽高，透明物体难处理，简单光照场景基线成本大
- **Deferred Lighting**：带宽略低于 DS（历史上对 Xbox 360 EDRAM 有意义）；允许阴影逐光生成；现已式微
- Tiled/Clustered 的真正价值在于单次 Tile 处理多光源降低带宽，而非演示数量；实际中能负担的有阴影灯光数量仍受限
- 廉价无阴影点光源是低质量 GI 替代品，应用 Voxel/Vertex/Lightmap bake 代替
- 两种几何剔除策略对比：Volume Early-Z（精确到 quad）vs Tile（平均到 tile），各有权衡

## 链接到的概念

- [[deferred-rendering]]
- [[forward-plus-rendering]]
- [[light-prepass-pipeline]]
- [[tiled-light-prepass]]
- [[tiled-light-culling]]
- [[cascaded-shadow-maps]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/09/notes-on-real-time-renderers.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-09-03_notes-on-real-time-renderers.md`
