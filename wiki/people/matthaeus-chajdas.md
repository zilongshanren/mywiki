---
tags: [人物, 作者, 渲染, gpu, 编译器]
date: 2026-04-14
sources: 18
---

# Matthäus G. "Anteru" Chajdas

**Matthäus G. Chajdas**（网名 Anteru）是 AMD 的图形 / GPU 编译器方向工程师，博客 [anteru.net](https://anteru.net) 涵盖实时渲染研究、shader 编译器、API 设计与系统工程笔记。他的硕士 / 博士工作都在慕尼黑工大 Rüdiger Westermann 组，早期发表过 *Assisted Environment Probe Placement*（2011）等实时渲染辅助工具类论文。

## 风格

- **偏工程性的研究**：问题通常来自真实生产痛点（美术手工放探针），解法是工具化的预处理 + 美术 in-the-loop。
- **补完式写作**：发表多年后仍然回到原论文写博客补说明，解答读者对失败模式、采样密度、聚类启发式的具体疑问。
- **博客混合体**：技术文章之外，也混有系统管理笔记、硬件组装、产品试玩评论。本 wiki 只收录其中的渲染 / 编译器方向内容。

## 相关

- [[environment-probe-placement]]
- [[rendering-pipeline]]
- [[directx11-early-pitfalls]]
- [[homogeneous-rasterization-transpose-bug]]
- [[avoid-unsigned-types]]
- [[parquet-vs-csv-json]]
- [[subpixel-reconstruction-antialiasing]] —— I3D 2011，deferred 管线的子像素可见性 + 1x 着色重建
- [[tiled-light-trees]] —— I3D 2017（与 O'Donnell/Frostbite），tile 内 light BVH + clustered shading 混合
- [[d3d12-work-graphs]] —— ISCA 2025 把 work graph 从图形移植到 SpMV
- [[procedural-work-graph-generation]] — Work Graphs 驱动程序化生成，79,710 实例 / 3.74 ms
- [[voxel-lod-large-mesh]] — 体素 LOD 统一流式 + 剔除 + LOD 的超大网格光栅化方案

## Sources

- [[sources/chajdas-assisted-probe-placement]]
- [[sources/anteru-directx11-hints]]
- [[sources/anteru-homogeneous-rasterization-gotcha]]
- [[sources/anteru-avoid-unsigned-types]]
- [[sources/anteru-data-formats-csv-json]]
- [[sources/anteru-sraa]]
- [[sources/anteru-tiled-light-trees]]
- [[sources/anteru-workgraph-spmv]]
- [[sources/anteru-hybrid-sample-surface]]
- [[sources/anteru-giga-particle-fluid]]
- [[sources/anteru-edge-friend-subdivision]]
- [[sources/anteru-terrain-shadow-streaming]]
- [[sources/anteru-realtime-hybrid-hair]]
- [[sources/anteru-meshlet-compression]]
- [[sources/anteru-svgf-motion-blur]]
- [[sources/anteru-image-error-metrics]]
- [[sources/anteru-procedural-work-graphs]]
- [[sources/anteru-scalable-large-mesh]]
