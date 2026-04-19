---
tags: [source, 渲染, shader, 顶点, gamemaker, glsl]
date: 2026-04-19
sources: 1
---

# Vertex Shaders（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 6 月 9 日的 GM Shaders 文章，应 X 粉丝投票选出的话题——**vertex shader 入门：什么时候用、怎么用、不能做什么**。

## 摘要

Xor 从 [[rendering-pipeline|渲染管线]] 的位置讲起：一切 draw 都从顶点开始，`draw_sprite` 是 4 顶点两三角形、`draw_text` 是每字符一个 textured quad。Vertex shader 跑在 primitive assembly 之前——这是它能**改变 fragment 作用域**的特权（加 padding、扩 outline、shell）。标准 GM GLSL VS 模板包括 attribute 三件套（position/colour/texcoord）和 MATRIX_WORLD_VIEW_PROJECTION 变换。重点几个 gotcha：**不同 draw 函数传入不同 attribute**（`draw_circle` 没 texcoord，用错 shader 会静默失败）；自定义 attribute 在 3D 里常用于 bone/tangent，attribute 数量直接影响顶点带宽。Varying 做线性插值、支持 float/vec/mat 但**不支持 int/bool**；典型用法是 **per-vertex lighting**（老派 Gouraud 风格，省 fragment 算力）。VS 能做 MVP 做不到的事——在投影前**直接修改 position**：sine 波浪、shockwave、primitive 外扩。限制部分列得很实用：VS/FS **uniform 不共用**（同名要各声明一次）、GM **VS 不能采样纹理**（texture2DLod 只在 HTML5 能用）、**derivative 函数在 VS 无意义**但 FS 用在 varying 上能从 dFdx/dFdy 叉乘计算 flat shading 法线——免 normal attribute。结尾提到自己一个 3D 水面 shader 同时用 VS 做波浪位移和法线计算；还顺带推荐了 Freya Holmer 的"summation/product 当 for-loop"的数学符号可视化。

## 关键要点

- **VS 在 primitive assembly 之前**——能扩展 FS 作用区域（padding / outline / shell）。
- **一切 draw 都是 vertex**——`draw_sprite`/`draw_text`/`draw_line` 都走 VS。
- **不同 draw 函数 attribute 集合不同**——写通用 shader 要考虑默认值或多 shader 策略。
- **自定义 attribute** = tangent / bone weight / baked AO 的入口，但 bytes 数直接拉升带宽。
- **Varying 只能传 float 族**——int/bool 插不了；per-vertex lighting 是最大的性能节省手段。
- **VS 改 position** 做波浪、冲击波、primitive 外扩——FS 办不到的事。
- **同名 uniform 不共享**——GM 下必须 VS/FS 各声明一次。
- **GM VS 不能采样纹理**——挡住了 vertex-texture-fetch 的 terrain displacement / GPU skinning 路径。
- **FS 里 `dFdx(pos), dFdy(pos)` 叉乘 = flat 法线**——免 normal attribute 的漂亮小技巧。
- **per-vertex 优化是移动端的大刀**——能摊就摊。
- **现代 GLSL 用 `layout(location = N)` 替代 `attribute`**——语义一样、语法更显式。

## 链接到的概念

- [[vertex-shader-basics]]
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[mvp-transform]]
- [[coordinate-spaces]]
- [[compact-vertex-format]]
- [[waving-grass-shader-vertex-offset]]
- [[shockwave-effect]]
- [[gpu-skinning-matrix-palette]]
- [[tangent-space-normal-mapping]]
- [[hlsl-derivation-correctness]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/vertex
- 本地：`raw/articles/mini.gmshaders.com/2024-06-09_gm-shaders-vertex-shaders.md`
