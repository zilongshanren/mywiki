---
tags: [source, rendering, shader, unity, uv]
date: 2026-04-14
sources: 1
---

# Planar Mapping（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 4 月发表的入门级 Unity shader 教程，演示如何用**顶点世界坐标的两个分量作为 UV**，从而在没有模型 UV 或想忽略模型 UV 的情况下给表面贴图。

## 摘要

文章把 **planar mapping** 分成三步：先用 `v.vertex.xz` 做最简版（贴图像是从头顶压下来、跟模型一起转），再套 `TRANSFORM_TEX` 宏让 Inspector 的 Tiling/Offset 生效，最后用 `mul(unity_ObjectToWorld, v.vertex)` 把坐标拿到世界空间，使贴图钉在世界上——这是地形、墙面等希望贴图跟空间而不是跟物体走的场景最常用的做法。文章末尾点名它的两大局限——垂直面拉伸和只适合 tileable 贴图——并把 triplanar mapping 作为下一步改进的方向留给后续教程。这篇是 Ronja 整个教程系列里为后续 SDF 系列服务的前置之一：2D SDF 教程就直接采用这里建立的「用世界坐标的 xz 当 2D 坐标」习惯。

## 关键要点

- 顶点着色器里可直接用 `v.vertex.xz` 产生 UV——vertex shader 天然插值，fragment 里就是每像素 UV。
- `TRANSFORM_TEX(uv, _MainTex)` 宏是 Unity shader 的标准动作，本质是 `uv * _MainTex_ST.xy + _MainTex_ST.zw`——忘了它材质 Inspector 里的 Tiling/Offset 就不起作用。
- `unity_ObjectToWorld` 矩阵把局部坐标变到世界空间；用世界坐标做 UV 让同一个 shader 在相邻物体间无缝贴图对齐。
- 缺点是垂直面上 UV 被压缩成一条线 → 贴图出现长条拉伸；triplanar 是标准修复方案。

## 链接到的概念

- [[planar-mapping]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[fragment-shader]]
- [[sdf-2d-primitives]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/008-planar-mapping/>
- 本地：`raw/articles/ronja-tutorials.com/2018-04-23_planar-mapping.md`
