---
tags: [source, rendering, shader, unity, unlit, 入门]
date: 2026-04-14
sources: 1
---

# Basic Shader（Ronja's Shader Tutorials 004）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 3 月发表的系列第四篇，把前三篇的结构、HLSL 语法、变量声明拼成第一个**真正能跑的 Unlit + Tint shader**——UnityCG.cginc 辅助下把 object-space 顶点送进 clip space，在 fragment 里采样贴图 × 乘 tint。

## 摘要

这是 001–004 四连的收束篇：Structure、HLSL、Variables 都是铺垫，这篇终于把 `vert` 和 `frag` 两个函数体填出来。步骤是四步：一是用 `#pragma vertex vert` / `#pragma fragment frag` 声明入口函数；二是 `#include "UnityCG.cginc"` 把 Unity 的辅助库拉进来；三是 vertex 函数里用 `UnityObjectToClipPos(v.vertex)` 把 object-space 顶点一步变到 clip space（底层是 `UNITY_MATRIX_MVP * v.vertex`，但新手不需要自己算），再用 `TRANSFORM_TEX(v.uv, _MainTex)` 宏把 UV 乘上 `_MainTex_ST.xy` 加 `_MainTex_ST.zw`；四是 fragment 函数里 `tex2D(_MainTex, i.uv) * _Color` 返回最终颜色，函数签名上带 `: SV_TARGET` 告诉编译器这是 color render target 的输出。文章重点是**三个宏 / 函数的语义**——`UnityObjectToClipPos`、`TRANSFORM_TEX`、`tex2D`——这三个是后续所有 Unity 内建管线 shader 教程的共同入口。产出是一个完整可跑的 `Tutorial/001-004_Basic_Unlit` shader，正是 `Create > Shader > Unlit Shader` 默认模板的简化版，之后所有教程（包括 Surface Shader 转换）都以它为起点。

## 关键要点

- `#pragma vertex vert` / `#pragma fragment frag` 告诉 Unity 哪两个函数是入口。
- `#include "UnityCG.cginc"` 引入 Unity 的 shader 工具库（内建管线时代的标配）。
- `UnityObjectToClipPos(v.vertex)` = object → clip space 的一步捷径，封装了 MVP 矩阵乘法。
- `TRANSFORM_TEX(uv, _MainTex)` = `uv * _MainTex_ST.xy + _MainTex_ST.zw`，自动套用 Inspector 里的 Tiling/Offset。
- `tex2D(tex, uv)` 采样纹理，fragment 函数返回 `fixed4 : SV_TARGET`。
- 最简可跑的 Unlit + Tint 是"每个 shader 教程的起点模板"。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[fragment-shader]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[rendering-pipeline]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/004-basic/>
- 本地：`raw/articles/ronja-tutorials.com/2018-03-23_basic-shader.md`
