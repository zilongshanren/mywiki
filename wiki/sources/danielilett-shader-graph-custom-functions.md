---
tags: [source, unity, shadergraph, hlsl, custom-function, 光照, urp]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics Part 10 - Custom Functions（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 7 月的 Shader Graph 入门系列第 10 部。主题是**Custom Function 节点**——Shader Graph 和 HLSL 的正式桥梁。案例是扩展 Part 7 的 cel shader，支持**主光颜色和衰减**、以及**多个附加光源**（URP 的 additional lights API）。

## 摘要

Part 7 的 cel shader 有两个硬伤：只用了主光方向、不看颜色和衰减；完全不处理附加光源（point / spot）。Shader Graph 的内建节点没有暴露这些数据——只能走 Custom Function 加 HLSL。

文章手把手教写 `CustomLighting.hlsl`：

- **`MainLight_float` 函数**：入参 `float3 WorldPos`，出参 `Direction / Color / Attenuation`。用 `#ifdef SHADERGRAPH_PREVIEW` 判断是不是预览窗口——是就返回假光源避免拿到垃圾，否则调 URP 的 `GetMainLight()` 填出参。函数名后缀 `_float`（或 `_half`）是 Shader Graph Custom Function 的硬约定，对应节点层的精度选项。
- **`AdditionalLight_float` 函数**：多一个 `int lightID` 入参，先赋黑色假光，然后 `#ifndef SHADERGRAPH_PREVIEW` + `if (lightID < GetAdditionalLightsCount())` 才覆盖成真实的 `GetAdditionalLight(lightID, WorldPos)` 结果。

节点侧：每个 Custom Function 要手动列 inputs/outputs 的名字和类型，**必须和 HLSL 代码一致**。`int` 类型 Shader Graph 不认，用 `Float` 代替，Unity 会隐式转换。

然后来到 Shader Graph **最大的短板——不支持循环**。要让图处理"所有附加光"，要么把 `AdditionalLight` 节点展开 4 次（写死 `LightID = 0..3`，超过就丢光）、要么写第三个 HLSL 函数 `AllAdditionalLights_float`——把循环塞进 HLSL，只返回累加后的 `LightColor`。后者明显更好：既处理任意数量的光，又只对实际存在的光付费。Ilett 坦承"这种场景下 HLSL 比纯图好"。

最后 Ilett 插了一段自我推广：他新出的 **PSX Shaders Pro** asset pack（PS1 风格的有限顶点精度、透视不正确纹理、CRT 后处理）。

## 关键要点

- **Custom Function 节点是 Shader Graph 打破所有限制的后门**——访问 URP 内部 API（光照、阴影、buffer）、做循环、手写数学——都走这扇门。
- `_float` / `_half` 后缀约定对应 Shader Graph 的精度切换，两者都写是 asset 分发时的好习惯。
- **`SHADERGRAPH_PREVIEW` 宏**是所有依赖 URP 运行时 API 的 Custom Function 的必备 guard——预览窗口里那些 API 返回垃圾数据。
- **Shader Graph 没有循环**——这是它做 per-light 处理、per-pixel 迭代算法、per-sample SSAO 的根本性限制。解法永远是"把循环塞进 HLSL、把结果作为一个 Custom Function 节点暴露给图"。
- `GetMainLight()` / `GetAdditionalLight(i, worldPos)` / `GetAdditionalLightsCount()` 都在 URP 的 `Lighting.hlsl`（`Packages/com.unity.render-pipelines.universal/ShaderLibrary/`）里，Shader Graph 自动 include 了这个文件。这个目录是 URP shader 作者应该知道的源码入口。
- URP 里 additional lights 有上限（默认 8），且"选哪 4 盏"的排序有时候反直觉（Ilett 遇到绿光被选而更近的蓝光被跳过）——这是 URP 内部 per-object light culling 的行为，无法在 shader 里左右。

## 链接到的概念

- [[shader-graph-custom-function-hlsl]]
- [[cel-shading-pipeline]]
- [[shader-graph-lighting-primer]]
- [[diffuse-lighting-lambertian]]
- [[shaderlab-hlsl-basics]]
- [[scriptable-render-pipeline]]

## 原文

- 链接：<https://danielilett.com/2024-07-09-tut7-14-intro-to-shader-graph-part-10/>
- 本地：`raw/articles/danielilett.com/2024-07-09_unity-shader-graph-basics-part-10-custom-functions.md`
