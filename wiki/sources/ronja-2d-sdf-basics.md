---
tags: [source, rendering, shader, sdf, 2d]
date: 2026-04-14
sources: 1
---

# 2D Signed Distance Field Basics（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 11 月发表的 SDF 入门教程，是她整个 SDF 系列的首篇，覆盖 2D 圆和矩形的 SDF 写法、translate/rotate/scale 空间变换，以及两种 SDF 可视化手法。

## 摘要

文章先介绍 SDF 的基本定义——形状表示成一个返回「到最近表面有符号距离」的函数——然后从最简单的圆开始：`length(p) - radius`。矩形较复杂一点，需要分内外两段合成：`length(max(|p| - half, 0))` 处理外部欧氏距离，`min(max(ex, ey), 0)` 处理内部的负距离，两者相加得到完整 SDF。空间变换部分是整篇教程的理论亮点——Ronja 把 translate/rotate/scale 都写成**作用在采样点上的逆变换**：要把形状向右移，就把采样点向左移。这个「被采样点承担变换」的设计让所有基元形状无需关心 transform 参数，非常干净。缩放会破坏「返回真实距离」的 SDF 性质，修复方法是输出时再乘回缩放系数。最后两节是可视化：一种是 `fwidth(d) + smoothstep` 得到带天然抗锯齿的硬边形状（text rendering / TextMesh Pro 派系），另一种是 `abs(frac(d / spacing + 0.5) - 0.5)` 产生周期等值线，配上内外部不同颜色做成地形图式调试视图。整篇教程建立了后续 SDF 系列（[[sdf-ray-marched-shadows|软阴影]]、布尔运算、变形等）所需的工具库 `2D_SDF.cginc`。

## 关键要点

- SDF 的「signed」在于内部负距离——这让布尔运算和 offset 效果可以直接写成 `min`/`max`。
- 矩形 SDF 的内外分段合成是 shader 里「用 min/max 做自动分支」的标准模式。
- **变换作用在采样点上而非形状上**：`translate/rotate/scale` 都是逆变换 —— 同一原则在纹理矩阵、相机矩阵、[[mvp-transform|MVP]] 里反复出现。
- **缩放破坏距离场性质**：除以 s 放大形状的同时也把距离放大 s 倍，修复需要在最终距离上乘回 s。非均匀缩放无解析解。
- **`fwidth(d)` + `smoothstep(w, -w, d)`**：单像素宽的抗锯齿边，等价于 TextMesh Pro 的 SDF 字体渲染机制。
- **`abs(frac(d / spacing + 0.5) - 0.5) * spacing`**：把任意 SDF 转成周期等值线——调试 SDF 的利器。

## 链接到的概念

- [[sdf-2d-primitives]]
- [[sdf-ray-marched-shadows]]
- [[jump-flooding-algorithm]]
- [[planar-mapping]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/034-2d-sdf-basics/>
- 本地：`raw/articles/ronja-tutorials.com/2018-11-10_2d-signed-distance-field-basics.md`
