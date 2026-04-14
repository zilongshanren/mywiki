---
tags: [source, rendering, shader, unity, 颜色, 数学]
date: 2026-04-14
sources: 1
---

# Color Interpolation（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 2018 年 5 月发表的系列第 009 篇，用三种层层递进的变体把 shader 里「两色之间过渡」的数学讲透。

## 摘要

文章从一个常见错误版本切入：`col = _Color + _Secondary * _Blend`——这实际上做的是把两束光打在同一点上，亮度随 blend 增加，原色永远不会完全消失。正确版本是凸组合 `col = _Color * (1 - _Blend) + _Secondary * _Blend`，这就是线性插值（linear interpolation）的定义，HLSL 里提供 `lerp(a, b, t)` 内置。文章随后把同一套数学套到两张纹理上（分别 `tex2D` 后 `lerp`），再把 `_Blend` 从 uniform 改成从第三张灰度纹理采样的标量（`tex2D(_BlendTex, uv).r`），得到最朴素的 **mask-driven blending**——即后续地形 splat map、溶解效果、污渍贴花的共同骨架。

## 关键要点

- 加法不是插值——凸组合（权重和为 1）才是。
- `lerp(a, b, t)` 在 HLSL 对向量逐分量插值，GLSL 里同名是 `mix`。
- 多张纹理插值时 `TRANSFORM_TEX` 和 `_ST` 要放在 fragment shader 里各算一次 UV。
- 第三张灰度图 `.r` 作为 blend 标量 → mask-driven 混合 → 地形、溶解、贴花的统一抽象。
- 本文被后续 checkerboard 教程直接引用，因为棋盘的 0/1 选择器本质就是 `lerp`。

## 链接到的概念

- [[shader-color-interpolation]]
- [[alpha-blending]]
- [[color-space]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/009-interpolating-colors/>
- 本地：`raw/articles/ronja-tutorials.com/2018-05-03_color-interpolation.md`
