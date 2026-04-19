---
tags: [source, unity, shadergraph, 光照, fresnel, cel-shading]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics Part 7 - Custom Lighting（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 5 月的 Shader Graph 入门系列第 7 部。在 Part 6 介绍完 Lit 图的 PBR 黑盒之后，这一部教两件事：**用 Fresnel 做边缘高光**，以及**用 Unlit 图 + `Main Light Direction` 节点手写 cel shading**——两者都是绕开 Lit 黑盒、用 Unlit 图自己算光照的起步。

## 摘要

文章分两节。前半讲 Fresnel：解释 Fresnel 效应的物理来源（掠射角下反射增强），然后转到实用路径——Shader Graph 的 `Fresnel Effect` 节点直接给出 `pow(1 - N·V, Power)`，用 HDR 颜色配 Bloom 后处理就能做出发光边缘。注意"HDR 颜色选色器里 `(1,1,1,intensity=3)` 和 `(8,8,8,intensity=0)` 等价"这个看似 bug 的行为实际是两种合法表达同一颜色的方式。Fresnel 效果只在曲面上好看，立方体这类几何会因为法线均匀而失效。

后半讲 Cel shading：把 Part 6 讲过的 diffuse light 数学 `max(0, N · L)` 用节点画出来——`Main Light Direction` → `Negate` → `Dot(Normal Vector)`——这是 Shader Graph 里第一次手写光照公式。然后用 `Step` 或 `Smoothstep` 节点把连续渐变切成硬阶，这是 cel shading 的核心。Ilett 推荐 `Smoothstep` 因为边界有 1-2 像素羽化。最后用 `Ambient Light Strength` 属性 + `Lerp` 保证背光面不会纯黑，而是被环境光提到某个基底值。这一部没处理额外光源（方向光以外的 point light、spot light），留给 Part 10 的 Custom Function 路径。

## 关键要点

- `Fresnel Effect` 节点在 Unlit 图里也能用，输出 `pow(1 - dot(N, V), Power)`。Lit 图内部已经有 Fresnel（属于 PBR specular），但 Unlit 路径能让你"只要边缘光、不要 PBR 其它"。
- **HDR + Bloom 是 Unity 里所有"发光"效果的唯一公式**——没有 Bloom 后处理，HDR 颜色超过 1 的部分只会被裁剪成白色。Ilett 从 Part 6 的 Emission 开始反复强调。
- `Main Light Direction` 节点是 URP 的新节点（相对早期 Shader Graph），把方向光方向暴露给图。Shader Graph 没有对应的 "Main Light Color" 或 "Main Light Attenuation" 节点——要这些数据必须走 [[shader-graph-custom-function-hlsl|Custom Function]] 路径调 `GetMainLight()`。
- `Step` vs `Smoothstep`：前者产生硬边（0 或 1），后者在 `Edge1` 和 `Edge2` 之间平滑插值。cel shading 几乎总是用 `Smoothstep` 加一点羽化，纯硬边在 1 像素宽度上会有闪烁。
- 这个 Part 故意只做"单主光 + diffuse"的最简 cel shading，**完全没有 specular**——作者把 specular 和多光源当作练习留给读者，也是下一篇 Part 8 开始绕到 scene intersection 话题的借口。

## 链接到的概念

- [[fresnel-edge-highlight]]
- [[cel-shading-pipeline]]
- [[shader-graph-lighting-primer]]
- [[diffuse-lighting-lambertian]]
- [[bloom-threshold-blur-composite]]
- [[shader-graph-custom-function-hlsl]]

## 原文

- 链接：<https://danielilett.com/2024-05-07-tut7-11-intro-to-shader-graph-part-7/>
- 本地：`raw/articles/danielilett.com/2024-05-07_unity-shader-graph-basics-part-7-custom-lighting.md`
