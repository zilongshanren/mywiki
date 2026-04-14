---
tags: [source, unity, shadergraph, 光照, pbr]
date: 2026-04-14
sources: 1
---

# Unity Shader Graph Basics Part 6 - Lighting Basics（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 3 月的 Shader Graph 入门系列第 6 部。前 5 部都在讲 Unlit 图，这一部把 **Lit 图的完整输出栈**——Base Color / Normal / Metallic / Smoothness / Emission / Ambient Occlusion——逐个拆开讲清楚，用 ambientCG 的 grass / brick 贴图作为案例。

## 摘要

文章先用一段篇幅介绍三种光照：diffuse（`L·N`，视角无关）、specular（视角相关，表现为亮斑）、ambient（全局基底亮度，粗略代表间接光）。然后转进 URP Lit 图：Unity 的 Lit shader 走 **PBR**，shader 作者不需要自己写光照公式，只要"告诉 Unity 物体的物理属性，Unity 替你算"。接下来逐个 output 讲：Base Color 用 `Sample Texture 2D` + `Parallax Mapping` 节点（高度图驱动 UV 位移，伪造深度）；Normal 要把 `Sample Texture 2D` 的 Type 改成 Normal；Metallic 和 Specular 是两种互斥的工作流，作者偏好 Metallic；**Smoothness 是个陷阱**——ambientCG 给的是 roughness 贴图（黑 = 光滑），而 Unity 要的是 smoothness（白 = 光滑），要用 `One Minus` 反转；Emission 需要 HDR 颜色 + Bloom 后处理才能真的发光；Ambient Occlusion 用贴图调制环境光。作者承诺 Part 7 会讲 Lit shader 的高阶 use case。

## 关键要点

- Lit 图有两种 workflow：**Metallic**（用 slider 表达金属性，更简单）和 **Specular**（直接控制高光颜色，更灵活）；选哪个是主观偏好，物理表达能力等价。
- Parallax Mapping 节点用 heightmap 修改采样 UV，**不改 geometry**——是便宜且无需 tessellation 的"假深度"技术。注意 albedo 和 normal 都要用这组位移后的 UV，否则纹理和法线会解耦。
- 法线贴图必须把 Sample Texture 2D 的 **Type 设 Normal**，Unity 会走一条不同的解压缩路径（可能是 DXT5nm）。
- **Roughness vs Smoothness 语义翻转**是接 ambientCG / Polyhaven / Substance 贴图的常见坑：ambientCG 的约定是黑 = 光滑、白 = 粗糙，Unity Shader Graph 的 Smoothness 期望白 = 光滑。解法是取 Red 通道过 `One Minus`。
- Emission 要生效有两个前置条件：颜色属性的 Mode 设成 **HDR**（允许 >1 分量）+ 场景里必须有 **Bloom 后处理**。新建 URP 工程会自动带 Bloom Volume Profile；否则要手动 `GameObject → Volume → Global Volume` + Override → Post-processing → Bloom。
- Ambient Occlusion 的值 0 = 完全遮蔽、1 = 完全可见；它只在环境光上起作用，不影响直接光。
- Displacement 和 Normal 的语义不同：displacement 假装"像素向外凸出"（通过 UV 位移），normal 只改"像素朝哪个方向"（通过法线替换）。两者可以也应该同时使用。

## 链接到的概念

- [[shader-graph-lighting-primer]]
- [[physically-based-shading]]
- [[diffuse-lighting-lambertian]]
- [[tangent-space-normal-mapping]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：<https://danielilett.com/2024-03-19-tut7-8-intro-to-shader-graph-part-6/>
- 本地：`raw/articles/danielilett.com/2024-03-19_unity-shader-graph-basics-part-6-lighting-basics.md`
