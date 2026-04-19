---
tags: [source, unity, shadergraph, terrain]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics (Part 11 - Terrains)（danielilett.com / Daniel Ilett）

[[daniel-ilett]] 2025 年 10 月 Shader Graph Basics 第 11 期：手工复刻 Unity Terrain 的 splatmap 材质混合，并加一个基于世界法线自动把陡峭处切到岩石层的扩展，最后做一个世界空间扫描波的发光环。

## 摘要

Unity 内置 Terrain 只允许 4 层 splatmap，约定用 `_Control` + `_Splat0..3` 贴图。Shader Graph 里没有直接对应节点，需要手工把 control 四通道作为权重把 4 个 splat 的 albedo 加权相加；再用 normal 的世界 Y 分量做阈值切岩石 tint；最后用两次 `Step` 夹出一个圆环做世界扫描波。

## 关键要点

- `_Control` 四通道作为 4 层 splat 的权重，手工相加
- 基于世界法线的岩石自动贴附：`dot(worldNormal, up)` < 阈值切第 5 层
- 世界扫描波：两次 `Step` 夹出圆环 + Emissive + Bloom

## 链接到的概念

- [[terrain-splatmap-shader-graph]]
- [[world-scan-shader-effect]]

## 原文

- 链接：<https://danielilett.com/2025-10-12-unity-shader-graph-basics-part-11-terrains/>
- 本地：`raw/articles/danielilett.com/2025-10-12_unity-shader-graph-basics-part-11-terrains.md`
