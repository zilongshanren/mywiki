---
tags: [source, 渲染, unity, shader, mask, sdf]
date: 2026-04-14
sources: 1
---

# My take on shaders: Custom masks (Part I) (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列第四篇（2017-06-07），承接 [[image-effect-mask-blend|simple masks]] 那篇——把「贴一张静态遮罩贴图」升级为「直接在 fragment shader 里用闭式表达式实时算出一个圆盘 mask」。

## 摘要

文章给出一支极小的圆盘 mask shader：核心公式是 `length(uv - center) * sizeRatio` 算距离，`saturate(dist / _Radius)` 归一化为 `[0,1]`，`pow(circle, pow(_Hardness, 2))` 调硬度，再用 `_Invert ∈ [-1, 1]` 翻转或调强。`_SizeX/_SizeY` 是手工纵横比校正——因为屏幕 UV 是 [0,1] 但实际宽高比不是 1:1，不补偿就会得到椭圆而不是圆。Alisavakis 自己坦白这支 shader 是他从一个更复杂的 ring shader 里反向简化出来的，对自己「能用但说不清」很诚实，借这次写作把每一行的为什么彻底想清楚。文末他强调：单独看圆盘 mask 几乎没用，但作为一块可以用 C# 实时控制圆心 / 半径 / 硬度的积木，它是后续无数局部特效的起点。

## 关键要点

- 把外部贴图 mask 改为 in-shader SDF 圆盘，解锁参数化（圆心、半径、硬度都能动态调）和分辨率无关。
- `saturate(dist / _Radius)` 的本质是把距离场归一化为带柔边的灰度遮罩。
- `pow(circle, pow(_Hardness, 2))` 的二次嵌套只是为了把美术调节范围压回常识区间（13 而不是 180）。
- `_SizeX/_SizeY` 用来抵消屏幕 aspect-ratio 把圆扳回正圆。
- `_Invert ∈ [-1, 1]` 一根旋钮兼任「翻转方向」和「降低强度」两个功能。
- 单独不可用，但这是 [[shockwave-effect|冲击波]] / 注意力引导 / 动态 vignette 的基础积木。

## 链接到的概念

- [[custom-mask-shaders]]
- [[image-effect-mask-blend]]
- [[sdf-2d-primitives]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-custom-masks-part-i/>
- 本地：`raw/articles/halisavakis.com/2017-06-07_my-take-on-shaders-custom-masks-part-i.md`
