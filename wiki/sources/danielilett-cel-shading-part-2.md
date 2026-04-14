---
tags: [source, unity, shader, 光照, cel-shading, surface-shader]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 2 - Cel-shaded Lighting（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 卡通渲染系列第二篇，也是**第一次让 shader 真正变成 toon look** 的一篇。方法是在 [[unity-surface-shaders|Surface Shader]] 上写一个自定义 Lighting 函数，把漫反射值量化成硬色阶，再叠一个量化的镜面高光。文章同时给出 Surface Shader 和手写 vertex/fragment shader 两个版本。

## 摘要

作者先解释**为什么不能继续用 `#pragma surface surf Standard`**：Standard 把光照完全藏在内建 PBR 路径里，无法插手。解决方案是写一个命名符合约定的 `half4 LightingCel(SurfaceOutput s, half3 lightDir, half atten)`，把 `#pragma` 改成 `#pragma surface surf Cel`，Unity 就会用它替代 PBR 方程。相应地 `SurfaceOutputStandard` 要换成旧版 `SurfaceOutput`。然后文章给出三个迭代版本：**（a）** 最原始的 `diffuse > 0 ? 1 : 0` 两色阶；**（b）** 用 `fwidth + smoothstep` 让阶梯边界有 1-2 像素柔化，避免严重的走样；**（c）** 加上 specular——`halfVec = normalize(lightDir + viewDir)`，`pow(dot(normal, halfVec) * diffuseSmooth, _Glossiness)`，再用常量上界的 `smoothstep` 把 specular 也切成硬斑。最后文章把 fragment shader 变体也写了一遍，差别主要在 view direction 需要 `WorldSpaceViewDir()` 手算并通过 `v2f` 传进 fragment。

## 关键要点

- **自定义 Lighting 函数**是 Surface Shader 里接管光照方程的唯一方式——命名必须以 `Lighting` 开头，剩下部分就是 `#pragma surface surf <name>` 用的名字。
- `fwidth(x) = abs(ddx(x)) + abs(ddy(x))` 给出标量 `x` 在屏幕相邻像素的变化幅度，用作 `smoothstep` 的上界能实现**自适应抗锯齿**——在大片同色区变化为 0 保持硬阶，在边界变大形成柔化。
- Specular 用 `fwidth` 会失控，因为 `pow` 让它在边界的变化过于剧烈；Ilett 用 `smoothstep(0, 0.01 * _Antialiasing, specular)` 的常量上界代替。
- `specular * diffuseSmooth` 是关键的 mask——没有它，阴影背面也会出现高光（因为 half vector 的 dot product 可能仍然为正），视觉上非常奇怪。
- fragment shader 变体里用 `_WorldSpaceLightPos0` 作为方向光方向，名字带 "Pos" 但存的其实是**方向向量**——Unity 历史遗留。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[unity-surface-shaders]]
- [[diffuse-lighting-lambertian]]
- [[analytical-antialiasing]]

## 原文

- 链接：https://danielilett.com/2019-06-08-tut2-2-cel-shading/
- 本地：`raw/articles/danielilett.com/2019-06-08_cel-shading-part-2-cel-shaded-lighting.md`
