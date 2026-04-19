---
tags: [source, unity, hlsl, texture, urp]
date: 2026-04-19
sources: 1
---

# Textures & UVs | Unity Shader Code Basics 02（danielilett.com / Daniel Ilett）

[[daniel-ilett]] 2025 年 10 月新启动的 Shader Code Basics 第 2 期：HLSL 侧纹理采样骨架 + SRP Batcher CBUFFER 的最小可跑模板，以及滚动 UV 示例。

## 摘要

HLSL 里采样纹理需要 `TEXTURE2D(_MainTex);` 声明 + 配套 `SAMPLER(sampler_MainTex);` + `float4 _MainTex_ST;` 的 tiling/offset，再用 `TRANSFORM_TEX(uv, _MainTex)` 在 vertex 阶段应用 ST，最后 fragment 里 `SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, uv)`。要进 SRP Batcher 必须把 material 属性塞进 `CBUFFER_START(UnityPerMaterial) ... CBUFFER_END`。滚动 UV 用 `_Time.y * speed` 加到 uv 上。

## 关键要点

- `TEXTURE2D` / `SAMPLER` / `_ST` / `TRANSFORM_TEX` / `SAMPLE_TEXTURE2D` 五件套
- SRP Batcher 的门票：`CBUFFER_START(UnityPerMaterial)` 包 material 属性
- 滚动 UV = uv + `_Time.y * speed`

## 链接到的概念

- [[hlsl-texture-sampling-basics]]
- [[srp-batcher-cbuffer]]

## 原文

- 链接：<https://danielilett.com/2025-10-16-textures-uvs-unity-shader-code-basics-02/>
- 本地：`raw/articles/danielilett.com/2025-10-16_textures-uvs-unity-shader-code-basics-02.md`
