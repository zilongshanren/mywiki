---
tags: [source, rendering, shader, unity, shaderlab, 入门]
date: 2026-04-14
sources: 1
---

# Structure（Ronja's Shader Tutorials 001）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 3 月发表的 shader 教程系列第一篇，用一个完整的 Unlit + Tint 示例，自顶向下拆解 Unity shader 的层级结构：从 `Shader → SubShader → Pass` 的 ShaderLab 骨架，到 `CGPROGRAM / ENDCG` 块内的 HLSL 代码、`Properties` 块、`Tags` 字典。

## 摘要

这是 Ronja 整个系列的起点，目的是让读者"先看懂结构、再谈语法"。文章先讲 vertex stage → rasterizer → fragment stage 的顶点/片元流水线结构，然后把一个最简单的 `Tutorial/001-004_Basic_Unlit` shader 完整贴出来，逐块解释 ShaderLab 外壳和 HLSL 内核的关系。关键观察是：**ShaderLab 不是执行语言**，它只是声明式地描述材质的元信息——`Properties` 是 Inspector 的 UI 绑定，`Tags` 是键值字典，`Pass` 才是真正装 HLSL 代码的地方。她还澄清了几个初学常见误区：`Fallback` 最常用途是借阴影 pass（几乎所有教程 shader 都 fallback 到 `VertexLit`）；多 SubShader 本应为不同硬件做降级但文档缺失、实践上一个就够用。这篇为后续四篇（HLSL 语法、Variables、Basic Shader、Surface Shader）建立了共同的代码骨架。

## 关键要点

- Shader 的三层嵌套结构：`Shader { Properties; SubShader { Tags; Pass { CGPROGRAM ... ENDCG } } }`。
- vertex stage 做变换（object→clip 空间）、rasterizer 做插值、fragment stage 决定像素颜色。
- ShaderLab 是声明式元数据层，真正的 GPU 代码在 `CGPROGRAM` 块里。
- `Properties` 把 HLSL 变量绑到 Inspector；`Tags` 是 SubShader / Pass 级的字典（`RenderType=Opaque`、`Queue=Geometry`）。
- `Fallback` 最常见作用是借用另一个 shader 的 shadow pass，而不是做硬件降级。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[rasterization]]
- [[unity-surface-shaders]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/001-structure/>
- 本地：`raw/articles/ronja-tutorials.com/2018-03-20_structure.md`
