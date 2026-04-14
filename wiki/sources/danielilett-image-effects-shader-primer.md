---
tags: [source, rendering, shader, unity, post-processing, tutorial]
date: 2026-04-14
sources: 1
---

# Image Effects Part 0 — Shader Primer（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 4 月发表的图像特效系列预备篇，为后续教程建立 ShaderLab / HLSL 骨架与 `OnRenderImage` 挂接方式。

## 摘要

本文是 Daniel Ilett 《Image Effects》系列的第 0 篇——在后续分篇介入灰度、深度、模糊等具体特效之前，先把 Unity built-in 管线时代写一支 image effect shader 所必需的样板讲透。内容包括：ShaderLab 的 `Shader / Properties / SubShader / Pass` 层级；`CGPROGRAM ... ENDCG` 包裹的 HLSL 代码块；`#pragma vertex/fragment` 声明入口函数；`appdata / v2f` 结构体与 `POSITION / SV_POSITION / TEXCOORD0` 语义；Unity 提供的 `UnityCG.cginc`、`UnityObjectToClipPos`、`TRANSFORM_TEX` 等辅助；以及一个最小 C# 脚本 `OnRenderImage(src, dst)` + `Graphics.Blit(src, dst, material)` 把 shader 接到相机后处理回调上。文章把顶点着色器退化成几乎透传，让初学者专注在 fragment shader 上——这也是整套 image effect 系列的切入姿态。

## 关键要点

- ShaderLab 只是 Unity 与 shader 之间的中介层，真正的 GPU 代码在 `CGPROGRAM` 块里，语言为 Cg / HLSL 子集。
- Properties 中的字段必须在 HLSL 段里**再声明一次**才能被 GPU 读到；`_MainTex_ST` 附带 tiling / offset。
- `UnityObjectToClipPos` 与 `TRANSFORM_TEX` 是 `UnityCG.cginc` 里最常用的两个辅助。
- image effect 的 vertex shader 只做裁剪空间变换和 UV 透传，所以后续教程基本只改 fragment。
- `OnRenderImage(src, dst)` 是 built-in 管线下把相机输出"劫持"到自定义 shader 的唯一官方回调；URP/HDRP 已弃用。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]

## 原文

- 链接：https://danielilett.com/2019-04-27-tut1-0-smo-shader-basics/
- 本地：`raw/articles/danielilett.com/2019-04-27_image-effects-part-0-shader-primer.md`
