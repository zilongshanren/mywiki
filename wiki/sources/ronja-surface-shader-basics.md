---
tags: [source, rendering, shader, unity, surface-shader, pbr, 入门]
date: 2026-04-14
sources: 1
---

# Surface Shader Basics（Ronja's Shader Tutorials 005）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 3 月发表的系列第五篇，演示如何把上一篇的手写 Unlit shader **改写成 Surface Shader**——让 Unity 自动生成 vertex/fragment 模板和 PBR 光照循环，开发者只填 `surf` 函数。

## 摘要

文章把"Surface Shader 是什么"拆成一次逐步转换：先从 004 的 Unlit shader 出发，**删掉** `vert` 函数、`appdata` / `v2f` 结构、`_MainTex_ST`、`UnityCG.cginc` 的 include、`Pass { ... }` 包装——Unity 会自动生成这些。然后补四样东西：一是一个叫 `Input` 的结构体，按**命名约定** `uv_MainTex` 自动对应 `_MainTex` 的 UV；二是把 `frag` 改名 `surf`，返回类型改 `void`，删掉 `SV_TARGET` 语义，接收 `Input i` 和 `inout SurfaceOutputStandard o` 两个参数；三是把结果写进 `o.Albedo` 而不是 `return`；四是加 `#pragma surface surf Standard fullforwardshadows` 声明 surface shader 入口与光照模型。换完之后整篇文章剩一半篇幅讲 **`SurfaceOutputStandard` 的七个字段**：Albedo（基色、被光照 tint）、Normal（切线空间法线，用于 normal map）、Emission（不受光、支持 HDR 和 bloom）、Metallic（0 非金属 / 1 全金属，影响反射 tint 是 albedo 还是白）、Smoothness（粗糙度反义，影响高光锐度和环境反射）、Occlusion（屏蔽光，非 HDR）、Alpha（透明度，只在 transparent shader 里起作用）。最后演示用 `[HDR]` 属性修饰 Emission 让它能调到 > 1、用 `Range(0,1)` 让 Inspector 出 slider、加 `#pragma target 3.0` 提高精度、加 `FallBack "Standard"` 借阴影 pass。作为 Ronja 入门系列的"第一个能 PBR 的 shader"，它也是后续所有 Surface Shader 教程的共同骨架。

## 关键要点

- Surface Shader 的核心是"**我只描述表面属性、Unity 替我写光照**"。
- `#pragma surface surf Standard fullforwardshadows` 是一行入口：函数名 + 光照模型 + 功能 flag。
- `Input` struct 字段命名有约定：`uv_XxxTex` 自动对应 `_XxxTex` 的 UV，`worldPos` 自动给世界位置。
- `SurfaceOutputStandard` 的七字段对应 PBR metallic workflow：Albedo / Normal / Emission / Metallic / Smoothness / Occlusion / Alpha。
- `[HDR]` 修饰符让 Color property 在 Inspector 里出 HDR picker、可超过 1。
- `Range(min, max)` 让标量 property 变成 slider。
- `FallBack "Standard"` 借阴影 pass——几乎所有 tutorial shader 都靠这一行有影子。
- `#pragma target 3.0` 提高精度，代价是移动端兼容性。

## 链接到的概念

- [[unity-surface-shaders]]
- [[shaderlab-hlsl-basics]]
- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[diffuse-lighting-lambertian]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/005-simple-surface/>
- 本地：`raw/articles/ronja-tutorials.com/2018-03-30_surface-shader-basics.md`
