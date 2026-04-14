---
tags: [source, 渲染, shader, hlsl, glsl, direct3d]
date: 2026-04-14
sources: 1
---

# Mini: HLSL（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 12 月 2 日的一篇 Mini，主题是**从 GLSL ES 视角学 HLSL**——GameMaker 编译到 Windows 时会把 GLSL ES 内部转成 HLSL，直接写 HLSL 可以跳过这层翻译、拿到更高性能和额外功能。内容叠加进 [[shaderlab-hlsl-basics]]。

## 摘要

作者把 HLSL 相较 GLSL ES 的三个理由列出来：**效率**（免转译）、**功能**（MRT、导数、transpose 等原生支持）、**语法偏好**。核心差异在「shader 如何和外界交换数据」：HLSL 不用 attribute / varying，而是用**带语义的 struct**，比如 `struct ATTRIBUTE { float3 pos : POSITION; float2 tex : TEXCOORD0; float4 col : COLOR; };`，里面的字段名可以随意起，真正挂钩的是后面的 **semantic**（`POSITION`、`TEXCOORD0-7`、`COLOR`、`COLOR0-3` 对应 `gl_FragData[]`、`SV_TARGET` 作为 pixel shader 返回值）。main 函数签名变成 `VARYING main(ATTRIBUTE INPUT)`（vertex）和 `TARGET main(VARYING INPUT) : SV_TARGET`（pixel）。

类型和函数名差异以速查表给出：`vec2-4 → float2-4`、`ivec → int2-4`、`mat → floatNxN`；`mix → lerp`、`fract → frac`、`mod → fmod`、`inversesqrt → rsqrt`、`clamp(x,0,1) → saturate(x)`、`atan(y,x) → atan2(x,y)`（注意参数顺序颠倒）、`dFdx/dFdy → ddx/ddy`、`if(x<0) discard → clip(x)`。纹理访问从 `texture2D(sampler, uv)` 变成 `tex.Sample(sampler, uv)`——HLSL 把纹理和采样器分开了，GameMaker 里基础纹理是 `gm_BaseTextureObject.Sample(gm_BaseTexture, uv)`。多张纹理要 `Texture2D foo : register(t1);` + `SamplerState bar : register(s1);` 显式注册。

## 关键要点

- **三大理由**：效率（免转译）、功能（MRT / 导数 / transpose 原生）、语法偏好。
- **Struct + semantic**：HLSL 输入输出都走结构体，字段靠 `POSITION` / `TEXCOORD0-7` / `COLOR` / `SV_POSITION` / `SV_TARGET` 这类 semantic 挂钩。
- **类型速查**：`vec → floatN`、`mat → floatNxN`、`ivec → intN`；float / int / sampler2D 不变。
- **函数速查**：`mix/lerp`、`fract/frac`、`mod/fmod`、`atan(y,x)/atan2(x,y)`（参数顺序翻转）、`dFdx/ddx`、`clamp(x,0,1)/saturate(x)`、`if(x<0) discard/clip(x)`。
- **纹理 / 采样器分离**：HLSL 里 `Texture2D` 和 `SamplerState` 是独立对象；采样通过 `tex.Sample(sampler, uv)`；多纹理要 `register(tN)` + `register(sN)` 显式编号。
- **GM 特供**：基础纹理对象是 `gm_BaseTextureObject`，对应采样器是 `gm_BaseTexture`，GML 端 API 不变。
- **参数顺序的坑**：GLSL 的 `atan(y,x)` 和 HLSL 的 `atan2(x,y)` 参数顺序是反的，移植 shader 时容易出 bug。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[fragment-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-hlsl-1486931
- 本地：`raw/articles/mini.gmshaders.com/2022-12-02_mini-hlsl.md`
