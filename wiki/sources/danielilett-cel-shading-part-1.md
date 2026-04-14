---
tags: [source, unity, shader, 光照, cel-shading]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 1 - Diffuse Lighting（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2019 年 6 月发表的卡通渲染系列第一篇，教学目标是把 **Lambert 漫反射光照**在 Unity 内建管线上用两种方式分别实现出来，为后续把平滑光照量化成离散阶梯（真正的 cel look）做铺垫。

## 摘要

文章从"为什么 diffuse 是所有光照模型的共同基座"讲起，接着并列给出两条路径：第一条是用 Unity 的 **Surface Shader**——写一个 `surf` 函数填 `SurfaceOutputStandard` 结构体，加 `#pragma surface surf Standard` 就能让 Unity 生成带 PBR 光照的完整 shader；第二条是手写 vertex/fragment shader——通过 `LightMode = ForwardBase` 和 `PassFlags = OnlyDirectional` 拿到方向光数据，在 fragment shader 里用 `dot(normal, _WorldSpaceLightPos0)` 做 Lambert 计算，再和 `_LightColor0`、`unity_AmbientSky` 相乘得到最终颜色。两种写法最终跑的数学一致，区别仅在于 Unity 代填了多少样板代码。

## 关键要点

- Lambert 公式的核心是归一化光向和归一化法线的点乘，必须先在 vertex shader 里用 `UnityObjectToWorldNormal` 把法线变到 world space。
- Surface Shader 的 `Input` 结构体有一组命名约定：`uv_MainTex` 自动解析为 `_MainTex` 的 UV；`SurfaceOutputStandard` 的 `inout` 表示既是输入也是输出。
- 手写 fragment shader 要 `#include "Lighting.cginc"` 才能用 `_LightColor0`，并且名字叫 `_WorldSpaceLightPos0` 但它存的是**方向**不是位置。
- 完整漫反射的精度补全需要考虑 `unity_AmbientEquator` 和 `unity_AmbientGround`，文章为了简洁只用了 `unity_AmbientSky`。
- Surface Shader 绑死内建管线，这也是 2020 年以后该系列被改写为 URP 手写 shader 的原因。

## 链接到的概念

- [[diffuse-lighting-lambertian]]
- [[unity-surface-shaders]]
- [[coordinate-spaces]]
- [[shader-vector-math-primer]]

## 原文

- 链接：https://danielilett.com/2019-06-05-tut2-1-diffuse/
- 本地：`raw/articles/danielilett.com/2019-06-05_cel-shading-part-1-diffuse-lighting.md`
