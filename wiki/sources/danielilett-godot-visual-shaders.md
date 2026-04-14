---
tags: [source, godot, shader, visualshader, shadergraph]
date: 2026-04-14
sources: 1
---

# Making Effects with Godot Visual Shaders（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 2 月的 Godot shader 初体验文章。他把过去在 Unity 里做过的三个经典效果（Dissolve / Hologram / Hull Outline）原样搬到 Godot 4.2.1 的 VisualShader 里，顺手做了一次和 Unity Shader Graph 的横评。

## 摘要

文章以"我终于试了下 Godot"开场，从添加测试球的微小坑（应该用 `MeshInstance3D` 而不是 `CSGSphere`）一路写到三个可视化 shader。Dissolve 的核心是世界空间 y 坐标 + 噪声扰动 + `Step` 阈值 + 边缘发光 emission，但因为 Godot **没有内建的"World Position"节点**，他被迫学会了 Godot 独特的 **Varying 机制**——在 Vertex 阶段通过 `Vertex × Model` 矩阵计算世界位置，声明一个 `Vector3 WorldPos` varying，用 `VaryingSetter`/`VaryingGetter` 跨 stage 传数据。又因为 Godot **没有内建噪声节点**，他学会了 **`VisualShaderNodeCustom`** 自定义节点——一个 `@tool` GDScript 类可以 override `_get_code` / `_get_func_code` / `_get_global_code` 三处代码注入点，直接往生成的 GLSL 里插 helper 函数。Hologram 用 `Texture2D` + `Time` 滚动 UV + 内建 `Fresnel` 节点实现。Hull Outline 走反向外推 + 第二 pass 的经典做法，在 Godot 里通过 Material 的 **Next Pass** 槽位挂两份材质，并把 outline 材质的 Cull Mode 设为 `Front`。结论是 Godot VisualShader 的表现像"一个可视化的 GLSL 代码 shader"——更接近原始代码，少很多抽象。

## 关键要点

- Godot VisualShader 缺失 World Position 节点，必须手动在 Vertex 阶段用 `TransformVectorMult(Model, Vertex)` 算，通过自定义 varying 传到 Fragment 阶段——这正是手写代码 shader 的标准做法。
- Multiply 有**七个同名不同签名**的节点（Float×Float / Vec×Vec / Matrix×Matrix / Matrix×Vec / `TransformVectorMult` 等），而 Unity Shader Graph 只有一个 Multiply 依赖类型推断。
- Godot 缺 `Remap` 节点，要用两个 `Multiply` + 一个 `Subtract` 手工展开 `[0,1] → [-a, +a]`。
- **`VisualShaderNodeCustom` 比 Unity 的 Custom Function 节点更强**，特别是 `_get_global_code()` 能把 helper 函数 / 全局变量插到 shader 文件顶部——这是 Unity Shader Graph 通常做不到的。Ilett 依此实现了 3D Perlin Noise 节点（Unity 内建 noise 只 2D）。
- 从 Fragment 上读 Vec3 的某个分量，应该用 `VectorDecompose` 节点，而不是节点右侧的"展开箭头"（当时版本有 bug）。
- HDR 发光需要在 Camera 的 **Environment → Glow** 打开，颜色参数要在 Color Picker 的 **RAW** 标签下拉到 >1；Unity 是 Volume + Bloom 后处理 + HDR Color Mode 的等价组合。
- Hull outline 的双 pass 组合：StandardMaterial 做主体 + 通过 Next Pass 挂 ShaderMaterial 做 outline，outline 材质的 **Mode → Cull** 设为 `Front` 实现反向外推。

## 链接到的概念

- [[godot-visual-shaders]]
- [[shader-prototyping-tools]]
- [[cel-shader-outline]]
- [[classic-shader-noise]]
- [[fragment-shader]]

## 原文

- 链接：<https://danielilett.com/2024-02-06-tut8-1-godot-shader-intro/>
- 本地：`raw/articles/danielilett.com/2024-02-06_making-effects-with-godot-visual-shaders.md`
