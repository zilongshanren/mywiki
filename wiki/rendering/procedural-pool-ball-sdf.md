---
tags: [rendering, sdf, shader, unity, urp]
date: 2026-04-19
sources: 1
---

# 程序化台球贴图（SDF shader）

Daniel Pokladek 的这篇 Unity URP shader 教程把台球表面的三个视觉元素——**横向条纹**、**数字圆环背景**、**数字**——全部用 [[sdf-2d-primitives|2D SDF]] 加 `smoothstep` 程序化地画出来，而不用任何预绘制的贴图（数字除外，用的是 SDF atlas）。这类做法的好处是：同一个 shader 跑在任何分辨率、任何球大小上，边缘永远是 pixel-perfect 的锐利；美术侧改风格只要调几个属性（条纹厚度、圆半径、颜色）。

几个落地要点：

- **横条纹**：`lineDistance = length(uv.y - 0.5) - _Line_Thickness`，再 `smoothstep(0.01, 0.0, lineDistance)` 得到边缘柔化的 mask；最后 `lerp(baseColor, accentColor, mask)` 混色。
- **数字圆环**：`circleDistance = length(uv - center) - _Radius`。因为 UV 在 0..1 贴完整个球一圈，如果想让数字同时出现在球的正反两面，得把 U 方向 `*2` 再 `frac()`——等价于"把一张贴图裁成两半、各贴一面"。
- **数字 atlas**：4×4 网格的 SDF 纹理存 15 个数字加 1 个空位。通过 `fmod(_Number, 4)` 和 `floor(_Number/4)` 算出 atlas 里的 tile 偏移；Unity 的 UV 原点在左下而贴图在左上，作者选择用 `(frac(uv)-center)*vOffset+center` 在 shader 里修正而不是改贴图。这也涵盖了一个常见陷阱。
- **锐利文字**：见 [[sdf-number-atlas-text]]——从 SDF 纹理的 r 通道经过 `_Edge_Min/_Edge_Max` 的双阈值 `smoothstep` 还原出尖锐但抗锯齿的数字边缘。
- **无分支**：`circleMask *= saturate(_Number)` 用乘法替代 if，0 号球就没圆环——这是典型的**避免 GPU 分支**的小技巧。

这篇文章也是 [[sdf-operations-shader]] 思路在"一个具体小物件"上的精细落地：从 iquilezles 的 SDF primitives 列表 + XOR 的 SDF 文章作为基础知识起点，最后得到一个能在 ShaderGraph 和纯 HLSL 两种形态间互相对应的完整 shader。

## Sources

- [[sources/pokladek-procedural-pool-balls]]
