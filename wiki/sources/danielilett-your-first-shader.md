---
tags: [source, unity, urp, shader, hlsl, 入门]
date: 2026-04-14
sources: 1
---

# Your First Shader - Unity Shader Code Basics 01（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2025 年 10 月发表的 Shader Code Basics 系列开篇，用 Unity 6 + URP 从零搭建一个"显示单色"的 HelloWorld shader，目的是把 ShaderLab 骨架和 HLSL 代码块最小化地走一遍，让从未写过代码 shader 的人第一次能把效果跑起来。

## 摘要

教程特意声明**面向 Unity 6 + URP**，并强调 URP / HDRP / Built-in 的 shader 库差异很大，必须上来就锁定管线选择。然后从 `Shader "Basics/HelloWorld" { ... }` 的外壳讲起——`Properties` 块声明一个 `_BaseColor` 颜色字段（shader 内部名 + Inspector 显示名的两段式语法），`SubShader > Tags` 设 `RenderPipeline = UniversalPipeline / RenderType = Opaque / Queue = Geometry`，然后在 `Pass` 里开 `HLSLPROGRAM` ... `ENDHLSL` 代码块。HLSL 侧的最小组合是：include `Core.hlsl`、在 HLSL 里**再次**声明 `float4 _BaseColor`、定义 `appdata { float4 positionOS : POSITION; }` 和 `v2f { float4 positionCS : SV_POSITION; }`，写 `vert` 函数调用 `TransformObjectToHClip`、写 `frag` 函数直接 `return _BaseColor`，最后用 `#pragma vertex vert` / `#pragma fragment frag` 绑入口。最后作者建议新手故意写错几处，体会 shader 的报错风格。

## 关键要点

- URP shader 一定要 include `Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl`，所有坐标变换辅助函数（如 `TransformObjectToHClip`）都在里面。
- ShaderLab 的 `Properties` 和 HLSL 的变量声明**要写两遍**——这是 Unity 最让新手困惑的一点，但它反映了 ShaderLab 只是 UI 绑定层、HLSL 才是真正的 shader 代码。
- Struct 字段必须带**语义（semantic）**：`POSITION` / `SV_POSITION` / `SV_TARGET` 是让 GPU 知道"从 vertex buffer 拉什么"和"输出到哪里"的关键。
- `v2f o = (v2f)0;` 这种强制初始化是 shader 里避免未定义值的惯用写法。
- Unity 6 + URP 时代已经完全放弃 Surface Shader 的自动生成，所有样板代码必须手写——这也是 Daniel Ilett 重启整个 Shader Basics 系列的原因。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[coordinate-spaces]]
- [[rendering-pipeline]]

## 原文

- 链接：https://danielilett.com/2025-10-15-tut10-01-your-first-shader/
- 本地：`raw/articles/danielilett.com/2025-10-15_your-first-shader-unity-shader-code-basics-01.md`
