---
tags: [source, rendering, shader, unity, uniform, 入门]
date: 2026-04-14
sources: 1
---

# Variables（Ronja's Shader Tutorials 003）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 3 月发表的系列第三篇，解释 Unity shader 里三种数据的来源：**object data**（来自 mesh）、**interpolators**（vertex 到 fragment）、**uniforms**（来自 material）。并顺便串讲 object / world / view / clip / screen 五个坐标空间。

## 摘要

文章围绕"shader 里的数据从哪来"这个问题组织。**Object data** 是 mesh 以数据流形式上传到 GPU 的顶点属性：最少要有 vertex position 和 triangle index，通常还带 normal、UV、vertex color；这些都在 object space，所以写 vertex shader 时不用操心物体的 transform。在 Unity 里它们通过一个习惯命名为 `appdata` 的 struct 传入 vertex stage，每个字段后面挂**语义（semantic）**告诉 Unity "这个 field 绑哪种 mesh 数据"——`POSITION`、`TEXCOORD0` 等。**Interpolators**（习惯命名 `v2f`）是 vertex stage 的输出结构体，字段被 rasterizer 在三角形内自动线性插值；必须有一个字段带 `SV_POSITION` 语义。**Uniform** 是一次 draw call 内对所有顶点/片元都相同的数据（颜色、贴图、矩阵），在 HLSL 代码块外直接声明全局变量即可，如果想让 material Inspector 能编辑就还要在 `Properties` 里再写一份。她还特别指出**纹理的 `_ST` 变量**这个 Unity 约定：声明 `_MainTex` 的同时声明 `float4 _MainTex_ST`，Unity 会自动把 Tiling/Offset 填进去，供 `TRANSFORM_TEX` 宏使用。最后一节用大白话总结坐标空间：object（模型局部）、world（场景全局）、view（相对相机）、clip（应用投影后）、screen（最终屏幕像素），并鼓励初学者"先别看矩阵、用 Unity 提供的辅助函数就够"。

## 关键要点

- 三种数据来源：object data（mesh）、interpolators（vertex→fragment）、uniforms（material）。
- HLSL 语义（semantic）把 struct 字段绑到 mesh 属性流：`POSITION`、`TEXCOORD0`、`SV_POSITION`。
- rasterizer 在三角形内做线性插值，fragment 看到的是插值后的 `v2f`。
- uniform 变量声明一次，`Properties` 再声明一次——两层：HLSL 全局变量 + Inspector UI。
- 纹理的 `_TextureName_ST` 约定自动携带 Tiling/Offset；用 `TRANSFORM_TEX` 宏套用。
- object / world / view / clip / screen 五个坐标空间的语义速查。

## 链接到的概念

- [[shaderlab-hlsl-basics]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[vertex-vector-interpolation-artifact]]
- [[compact-vertex-format]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/003-variables/>
- 本地：`raw/articles/ronja-tutorials.com/2018-03-22_variables.md`
