---
tags: [shader, unity, 内建管线, 光照, 样板代码]
date: 2026-04-14
sources: 1
---

# Unity Surface Shader

**Surface Shader** 是 Unity 内建渲染管线（Built-in RP）时代的一种**shader 抽象**：你只描述**表面有哪些属性**（albedo、法线、金属度、光滑度、发光、alpha），Unity 替你生成与之匹配的、跨多光源 / 多 pass / 多 rendering path 的完整 shader 变体。

## 工作方式

Surface Shader 的"入口"是一个 `#pragma surface <func> <lightingModel>` 指令——例如 `#pragma surface surf Standard`。编译时，Unity 会：

1. 把你写的 `surf(Input, inout SurfaceOutputStandard)` 嵌进它内部的 vertex/fragment 模板；
2. 针对 forward base、forward add、deferred、meta（lightmap 烘焙）等路径分别生成一份变体；
3. 注入对应光照模型（`Standard`、`StandardSpecular`、非 PBR 的 `Lambert` / `BlinnPhong`）的光照方程。

开发者只需要填两个结构体：

- `Input` 是从模板传给 `surf` 的几何数据，成员命名有约定——`float2 uv_MainTex` 按名字自动解析为"`_MainTex` 的 UV"，`float3 worldPos` 表示世界空间位置，等等。
- `SurfaceOutputStandard` 是 `inout` 输出的表面属性：`Albedo`、`Normal`（切线空间）、`Metallic`、`Smoothness`、`Occlusion`、`Emission`、`Alpha`。它是 Unity 5 引入 PBR 以后的新版结构体；老版 `SurfaceOutput` 用于 Lambert/BlinnPhong。

## 代价：隐性样板 + 管线锁定

Surface Shader 把光照循环、阴影接收、雾、lightmap 采样都藏在生成代码里，代价是：

- **不可移植**——生成的代码绑死 Unity 内建管线，URP / HDRP 都不支持。
- **变体爆炸**——每个 rendering path × 每种光源都是一个变体，编译时间和 shader variant collection 膨胀。
- **灵活度顶端有墙**——想改光照方程只能写自定义 lighting function（`half4 LightingCustom(...)`），或者换成手写 vertex/fragment shader。

因此 URP / HDRP 时代的 Unity shader 教程（包括 [[shaderlab-hlsl-basics|Daniel Ilett 的 Shader Code Basics 系列]]、[[cyanilux]] 的 URP 文章）基本不再讨论 Surface Shader——它是内建管线最后的温情，但在 SRP 时代已被 `HLSLPROGRAM` 代码块 + URP Shader Library（`Lighting.hlsl` 等）取代。对初学者而言，Surface Shader 教程仍然是理解**"一个完整 PBR shader 由哪些部件拼成"**的最短路径。

## Sources

- [[sources/danielilett-cel-shading-part-1]]
- [[sources/ronja-surface-shader-basics]] — Ronja 005，把手写 Unlit 逐步转换成 Surface Shader 的骨架演示
