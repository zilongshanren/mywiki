---
tags: [shader, 光照, 着色模型, unity, 渲染]
date: 2026-04-14
sources: 1
---

# Lambert 漫反射光照

**漫反射（diffuse / Lambertian）**光照是所有照相级光照模型的共同基座——后来加上去的 specular、Fresnel、环境光，都是在 diffuse 的壳上打补丁。它的物理假设只有一句话：**入射到表面的能量被等量散射到所有出射方向**，于是任何一点的亮度只取决于**入射方向与表面法线的夹角**，和观察方向无关。

## 点乘就是 Lambert 公式

设 `L` 是归一化的光源方向、`N` 是归一化的表面法线，`L · N` 就是两者夹角的余弦。这个余弦正好就是 Lambert 定律所需的"法线方向的有效照射面积"因子——垂直入射时 1，切线入射时 0，背面时为负（通常 `max(0, L·N)` 截断）。它的非线性变化也正好模拟了光斑从正面到侧面柔和过渡的直觉。

因此漫反射着色的整个计算量就是：把法线变换到世界空间、归一化、和世界光方向做一次点乘。

## Unity 中的两条路

Daniel Ilett 的教程把 Unity 里做 diffuse 的两种写法并列给出：

- **[[unity-surface-shaders|Surface Shader]]**：写一个 `surf` 函数填 `SurfaceOutputStandard`（Albedo/Normal/Metallic/Smoothness/…），`#pragma surface surf Standard` 告诉 Unity 用内建 PBR 光照模型；Lambert / BlinnPhong 是非 PBR 的替代。所有光源循环和 shadow map 查询 Unity 替你生成——代价是只能用 Unity 的内建管线。
- **手写 vertex/fragment shader**：把 `LightMode` 设为 `ForwardBase`、`PassFlags` 设为 `OnlyDirectional`，通过 `_WorldSpaceLightPos0`（方向光方向，尽管名字是 Pos）、`_LightColor0`、`unity_AmbientSky` 这些内建变量取光照。然后在 fragment shader 里做 `dot(normalize(worldNormal), _WorldSpaceLightPos0)` 乘以 albedo 和光色，加上一点环境光。

两种路径最终做的数学完全一样，区别只是 Unity 生成的样板代码——Surface Shader 的工作被内建管线接管后在 URP/HDRP 里被 HLSL 代码替代。

## 作为卡通渲染的起点

[[crt-shader-effects|卡通 / cel 渲染]]的核心并不是换一套光照模型，而是**把 `L·N` 的平滑渐变替换成离散阶梯**——比如用一个小 ramp 纹理或 `floor(diffuse * N) / N` 产生 2-3 级阶。所以理解 Lambert 是理解 cel shader 的前置条件：没有平滑梯度，就谈不上把它量化。

## Sources

- [[sources/danielilett-cel-shading-part-1]]
- [[sources/xor-mini-dot-product]]
