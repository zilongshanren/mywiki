---
tags: [source, 渲染, unity, shader, 坐标, shader-bits]
date: 2026-04-14
sources: 1
---

# Shader bits: World and screen space position (Harry Alisavakis)

[[harry-alisavakis]] 2017-10-11 发表的 *Shader bits* 系列开篇。作者自己说这是"a new post series that will hopefully feature more posts in the future"——存放那些"小但常用"的 shader 备忘。

## 摘要

文章把"怎么在 Unity shader 里拿到 worldPos 和 screenPos"这件事整理成四段模板（vertex/fragment × world/screen × 两种 shader 风格），一抄即用。Vertex/fragment 风格下需要显式在 `v2f` 里加 `float4 worldPos`，然后在 vertex shader 里写 `o.worldPos = mul(unity_ObjectToWorld, v.vertex)`，利用 Unity 预置的对象到世界矩阵一次乘法完成；screenPos 则有专门的 `ComputeScreenPos(o.vertex)` 一行搞定（输入是 clip space 位置）。Surface shader 风格更神奇：**只要在 `Input` struct 里写一个名字恰好是 `worldPos` 或 `screenPos` 的 `float3` 字段**，Unity 的 surface shader 代码生成器就自动帮你补齐后台计算——这是按约定（保留字段名白名单）驱动的 API，写错一个字母就彻底失效。作者没有讲太多 MVP 变换的原理，重点是**把这四种写法固化成抄袭模板**，为自己和读者省掉以后每次写新 shader 的翻代码时间。

## 关键要点

- **Vertex/fragment world pos**: `mul(unity_ObjectToWorld, v.vertex)` —— 一次矩阵乘，就是 MVP 链里的 M。
- **Vertex/fragment screen pos**: `ComputeScreenPos(o.vertex)` —— 内置辅助，返回 `(x, y, z, w)`，`xy / w` 为 `[0, 1]` 屏幕 UV。
- **Surface shader**: 只需在 `Input` struct 里写 `float3 worldPos;` 或 `float3 screenPos;`，Unity 识别保留名就自动生成底层代码。
- Surface shader 的这种"按名字驱动"是一套**隐式白名单 API**：没有报错、没有文档索引，写错字母就静默失效。其他同系列保留字段还有 `viewDir`、`worldNormal`、`color : COLOR`。
- Shader bits 系列的目的是**把常用片段固化为可抄模板**，不讲宏大概念——"I have more bits like that"。
- 和同作者两周前的 [[abzu-portal-cards-shader|ABZÛ portal card]] 直接呼应：那里用的 worldPos 写法在这一篇被抽出为独立 bit。

## 链接到的概念

- [[world-screen-space-position-shader]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[unity-surface-shaders]]
- [[fragment-shader]]
- [[planar-mapping]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/shader-bits-world-and-screen-space-position/>
- 本地：`raw/articles/halisavakis.com/2017-10-11_shader-bits-world-and-screen-space-position.md`
