---
tags: [source, rendering, shader, 体积渲染, raymarching, unity]
date: 2026-04-14
sources: 1
---

# Volumetric Rendering – Part 1（Alan Zucconi）

[[alan-zucconi|Alan Zucconi]] 2016 年 7 月的文章，Unity 体积渲染系列的开篇，介绍 volumetric raycasting 与 raymarching 的基本套路，并实现"用一个 cube 外壳渲染出一个虚拟球"。

## 摘要

传统 3D 引擎的世界是"一层一层的空壳"——无论多复杂的几何最终都被渲染成三角面，fragment shader 的计算停留在表面上。要模拟光在材质内部的传输（烟、雾、水、Plasma Globe、SDF 艺术）就必须让 shader 绕过这个约定。作者的做法是把一个普通 cube 当作**入口**：cube 外壳触发 fragment shader，shader 自己从相机出发沿视线走离散步长查询"当前点是否在虚拟体积里"。文章对比了 **analytic raycasting**（解析求交）和 **volumetric raymarching**（迭代步进）两条路线，指出只有后者能处理任意形状。最基础的实现用 64 步固定步长 + `distance(p, center) < radius` 判据得到一个红球。下一篇会讲 distance-aided raymarching（sphere tracing），即用 SDF 的距离作为步长，这是 Inigo Quilez / Shadertoy 生态的主流技术。系列后续还会讲 SDF 组合、阴影、AO。

## 关键要点

- fragment shader 不必只画外壳——它可以沿 viewDir 做内部积分
- `worldPosition`（外壳击中点）+ `viewDirection`（相机到击中点）是 raymarching 的两个输入
- Analytic raycasting 对任意形状无解，volumetric raymarching 是通用方案
- 固定步长 = 浪费，distance-aided raymarching / sphere tracing 是下一步优化
- Cube 作为外壳最省事：六面都可触发、任意角度都可进入
- 系列后续会讲 distance-aided raymarching、SDF、AO、soft shadows

## 链接到的概念

- [[volumetric-raymarching-intro]]
- [[sdf-ray-marched-shadows]]
- [[sdf-2d-primitives]]
- [[volumetric-fog-froxels]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.alanzucconi.com/2016/07/01/volumetric-rendering/>
- 本地：`raw/articles/alanzucconi.com/2016-07-01_volumetric-rendering-alan-zucconi.md`
