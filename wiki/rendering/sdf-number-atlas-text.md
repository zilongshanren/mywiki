---
tags: [rendering, sdf, text, shader, atlas]
date: 2026-04-19
sources: 1
---

# SDF 数字 Atlas 文字渲染

把数字或符号存为 [[sdf-2d-primitives|SDF]] 纹理 atlas，再在 shader 里用 `smoothstep` 双阈值解码，是一种把"小型符号集"嵌入 runtime shader 的常见手法。和传统的位图字体对比，SDF atlas 有两个核心优点：**任意分辨率下都保持锐利**（缩放、放大、甚至 mipmap 采样都不会糊）、**抗锯齿免费**（`smoothstep` 自带平滑过渡）。代价是生成 atlas 的离线工具链略复杂——常用 Ben Cloward / Valve 那一派的"2D 距离变换"或 msdfgen 这类工具生成多通道 SDF。

Pokladek 在台球 shader 里给出的最小实现：

1. 离线准备一张 4×4 的 SDF atlas 纹理（16 个 tile，存 0..15 的数字和一个空白）。运行时用 `_Number` 整数属性选 tile。
2. tile 索引到 UV 偏移：`u = fmod(_Number, 4); v = 3 - floor(_Number/4)`。注意 Unity UV 原点在左下，贴图在左上——这一步顺便把 V 方向翻过来。
3. 最终 atlas UV：`(tileLocalUV + float2(u,v)) * 0.25`，采样 r 通道就是 SDF 值。
4. 双阈值解码：`smoothstep(_Edge_Min, _Edge_Max, sdfSample)` 把 [0,1] 的 SDF 值变成 [0,1] 的 mask，边缘由 `_Edge_Min/_Edge_Max` 的宽度控制——宽一点就柔，窄一点就锐。
5. 和外层 mask（例如 [[procedural-pool-ball-sdf|数字圆环]] 的 circleMask）做 `lerp` 组合，避免数字"越过"圆环边缘。

这比 Unity 的 TextMeshPro 更"裸金属"，但同样原理相通——TMP 背后就是 msdf（多通道 SDF）+ 类似的 smoothstep decode。

## Sources

- [[sources/pokladek-procedural-pool-balls]]
