---
tags: [shader, unity, urp, hlsl, 入门]
date: 2026-04-14
sources: 1
---

# ShaderLab / HLSL 基础结构

一个最小可用的 Unity URP shader 由两层语言拼起来：外层是 Unity 特有的 **ShaderLab**（描述元信息和全局行为），内层是硬件无关的 **HLSL**（描述 GPU 上实际跑的顶点/片元代码）。Daniel Ilett 的 *Your First Shader* 教程把这两层按"shader 版的 HelloWorld"逐行拆开，这里提炼结构骨架。

## ShaderLab：元数据与 Pass 层

ShaderLab 的关键字很少——真正需要记住的只有这几层嵌套：

```
Shader "Basics/HelloWorld"      // 在 material 面板下拉里的路径
{
    Properties { ... }           // material 上可调的 Color/Float/2D 等
    SubShader
    {
        Tags { ... }             // 全局标签
        Pass
        {
            HLSLPROGRAM
            ...                  // 真正的 shader 代码
            ENDHLSL
        }
    }
}
```

- **`Properties`** 声明材质面板字段：形如 `_BaseColor("Base Color", Color) = (1,1,1,1)`——第一个名字是 HLSL 里用的内部名（下划线 + PascalCase 约定），第二个字符串是 Inspector 显示名，然后是类型和默认值。这些值同时需要在 HLSL 里**再声明一次**（`float4 _BaseColor;`），因为 ShaderLab 只是 UI 绑定层。
- **`Tags`** 在 URP 下至少要写三个：`RenderPipeline = UniversalPipeline`（限制只在 URP 使用；HDRP 写 `HDRenderPipeline`）、`RenderType = Opaque`、`Queue = Geometry`（渲染顺序：Geometry 是不透明，Transparent、AlphaTest 等在后面的教程里会用）。
- **`Pass`** 是一次"把整个物体画到屏幕"的操作。shadow caster、depth prepass、lightmap meta 等特殊行为都表现为额外的 Pass；一个最简 HelloWorld 只需一个 Pass。

## HLSL 层：vertex / fragment 模式

`HLSLPROGRAM` 内是一段类 C 语法的 HLSL 代码。即使教程只画纯色，也需要三段基础：

1. **`#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"`**——URP 的核心库，提供 `TransformObjectToHClip` 等函数。几乎每个 URP shader 都要 include 它。
2. **两个输入/输出结构体**：`appdata`（或 `Attributes` / `VertexInput`，业界惯例）定义 GPU 从 mesh buffer 拉哪些顶点数据，`v2f`（或 `Varyings` / `VertexOutput`）定义 vertex shader 传给 fragment 的插值数据。每个字段都得写一个**语义（semantic）**，比如 `float4 positionOS : POSITION` 告诉 API "从 vertex buffer 把 position 字段读进来"，`float4 positionCS : SV_POSITION` 告诉光栅化器"这是裁剪空间位置"。
3. **`vert` 和 `frag` 两个函数**——vertex shader 把对象空间坐标变到裁剪空间（`o.positionCS = TransformObjectToHClip(v.positionOS.xyz)`，见 [[coordinate-spaces]]），fragment shader 返回 `float4 : SV_TARGET`（屏幕颜色目标）。最后用 `#pragma vertex vert` / `#pragma fragment frag` 告诉编译器哪两个函数是入口。

## 为什么这份样板需要被记住

URP / HDRP 时代 Unity **放弃了 Surface Shader 的模板生成**——所有 shader 都得自己手写 `HLSLPROGRAM` 代码块，这意味着每个新 shader 都要重复一遍这段骨架。教程作者普遍的建议是"前几次照抄，抄几次之后肌肉记忆就建立了"。真正可变的部分只有：`Properties` 列表、两个 struct 的字段、`frag` 函数的计算逻辑。

这份骨架也是理解**[[unity-surface-shaders|Surface Shader]] 和手写 shader 差异**的分界线：Surface Shader 把这一整套 vertex/fragment 模板内化为"填 `surf` 函数"；URP 手写 shader 把主动权还给了开发者，但也把所有样板代码的负担一并交回。

## Sources

- [[sources/danielilett-your-first-shader]]
- [[sources/danielilett-image-effects-shader-primer]]
- [[sources/ronja-structure]] — Ronja 001，Shader/SubShader/Pass 的层级拆解
- [[sources/ronja-hlsl]] — Ronja 002，HLSL 标量/向量/swizzle/控制流速通
- [[sources/ronja-variables]] — Ronja 003，object data / interpolators / uniforms 三种数据来源
- [[sources/ronja-basic-shader]] — Ronja 004，UnityCG.cginc 辅助下的最简 Unlit + Tint 成品
- [[sources/alanzucconi-shader-intro-unity]] — Alan Zucconi 2015 的 Built-in RP 版 Shader 入门（ShaderLab + Cg/HLSL 骨架，`UNITY_MATRIX_MVP` 而非 `TransformObjectToHClip`），是本页 URP 视角的历史对照
