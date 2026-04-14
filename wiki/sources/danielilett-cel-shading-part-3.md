---
tags: [source, unity, shader, 光照, cel-shading, normal-map, fresnel]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 3 - Bump Mapping and Fresnel Lighting（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 卡通渲染系列第三篇，往之前的 cel shader 里加两样细节：**法线贴图**（bump map）和**菲涅尔边缘光**（rim light）。两者都只改 `LightingCel` 函数，不影响前面两 pass 的结构。

## 摘要

前半篇讲法线贴图。作者用 Unity Standard Assets 里的 Ethan 模型做演示——一开始因为没有法线贴图，衣服褶皱完全没有细节。在 `Input` 里加 `float2 uv_BumpMap`，在 `surf` 里一句 `o.Normal = UnpackNormal(tex2D(_BumpMap, IN.uv_BumpMap))` 就把切线空间法线送进了光照函数。因为 `LightingCel` 内部本来就要 normalize `s.Normal`，Surface Shader 框架会自动处理切线空间到世界空间的变换——开发者完全不用碰 TBN 矩阵。后半篇加 Fresnel：`rim = 1 - dot(normal, viewDir)`，乘以原始 `diffuse`（而不是 `diffuseSmooth`）作为受光面 mask，再用 `smoothstep(fresnelSize, fresnelSize * 1.1, rim)` 切成硬边缘光。`_Fresnel` 属性在 `[0, 1]` 之间暴露给 Inspector，值越大 rim 区域越宽。最终光照方程变成 `(diffuseSmooth + specularSmooth + rimSmooth) * _LightColor0 + unity_AmbientSky`。

## 关键要点

- `UnpackNormal` 负责把 `[0,1]` 的 RGB 纹理值反压缩到 `[-1,1]` 的切线空间法线向量——具体用 DXT5nm 还是 RGB(A) 取决于平台，Unity 内部处理平台差异（见 [[tangent-space-normal-mapping]]）。
- Surface Shader 的 `uv_<TextureName>` 命名约定让 Unity 自动生成 UV 传递代码，但要求 **`Input` 结构体成员名必须精确匹配**——写成 `uv_BumpMap` 而不是 `uv_bumpMap`。
- Fresnel 乘 `diffuse` 而不是 `diffuseSmooth` 的理由：`diffuseSmooth` 是硬色阶，会让 rim 光严格跟随阴影边界"掉电"；原始 `diffuse` 是平滑值，能让 rim 在阴影边界自然淡出，视觉上更连续。
- rim 和 specular 都只是"**在阴影 mask 之上再叠一层的硬斑**"——cel shading 的所有光照分量都被组织成"先算原始值、再用 smoothstep 切硬、再加起来"。
- 作者只展示了 Surface Shader 版本，明确提到 fragment shader 变体留给读者自己改——Part 3 没给代码。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[tangent-space-normal-mapping]]
- [[unity-surface-shaders]]

## 原文

- 链接：https://danielilett.com/2019-06-12-tut2-3-fresnel/
- 本地：`raw/articles/danielilett.com/2019-06-12_cel-shading-part-3-bump-mapping-and-fresnel-lighting.md`
