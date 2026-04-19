---
tags: [source, unity, shadergraph, water, foam, edge-glow, shield]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics Part 9 - Scene Intersections 2（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 5 月的 Shader Graph 入门系列第 9 部。延续 Part 8 建立的 `DepthIntersection` 子图，再在它上面搭两个视觉效果：**水面岸边的泡沫**和**能量护盾式的边缘辉光**。这是系列里第一次展示"同一基础设施换不同后处理得到完全不同视觉"的 shader 范式。

## 摘要

文章两大段。**Wave Foam Effect**：把 Part 5 的波浪 shader 复制成 `IntersectionFoam`，接入 `DepthIntersection` 子图。先做最朴素版——`distance / FoamDistance → Step → Multiply(FoamColor) → Add(BaseColor)`——阈值内的区域画白色泡沫。结果是一圈直硬边的白带，丑。然后加 `Simple Noise`（用 `Time * FoamVelocity` 偏移 UV 让它随时间滚动）作为 Step 的阈值输入，泡沫边缘变成噪声波动的有机形状。

但还剩一个问题：直线型的"摄像机视向"决定了物体正下方的水能感知到相交，物体**侧面旁边的水**看到的深度是远处地面、感知不到相邻的立方体。解法是把子图**改造成带 `Vector2 Offset` 输入**——用 `Screen Position(Default)` 加 `Offset` 换 `Scene Depth` 的默认 UV，让采样点偏离当前像素。`Offset` 默认 `(0, 0)` 保证不破坏现有图。主图再把 `Simple Noise` 同时喂给两处：一次当阈值、一次当 offset 乘子，泡沫就"涌"到了立方体旁边。副作用是物体另一侧也冒出错误的泡沫，Ilett 用第二个 `Step`（把 `Negate(distance)` 比对 noise）把错误侧剪掉——不是干净算法，但工作。

**Edge Glow Effect**：新的 `IntersectionGlow` unlit 图。思路是**两种"边缘"加在一起**——(a) UV 接近 0 或 1 的部分（几何边界），(b) depth intersection 点。UV 边缘用两个 `Smoothstep` 分别处理 `[0, EdgeThreshold]` 和 `[1-EdgeThreshold, 1]`，然后把 x、y 分量加起来。Intersection 边缘用 Part 8 的老配方（`OneMinus → Saturate → Power`）。两者用一个 `Add` 节点汇合，再乘 HDR `GlowColor` 加到 base color 上。这个效果对 `UV` 不连续（例如 sphere）不好使，但对 shield / cube 这种 UV 对齐几何边缘的 mesh 完美。

## 关键要点

- **Subgraph 可以非破坏性演化**：给 `DepthIntersection` 加 `Offset` 输入，默认值 `(0, 0)` 保证所有已有图继续工作——这是图形 API 对上游稳定性的廉价维护方式。
- **噪声 + 时间 = 有机运动**：Shader Graph 的 `Simple Noise + Time * Velocity + Tiling And Offset` 三件套是给任何周期性效果（water、fire、mist、holographic distortion）加"生命感"的通用配方。
- **`Smoothstep` 可以接 Vector 输入**：Ilett 特意解释这点——输入 `Vector4` 的 UV 时，Unity 逐分量独立做 smoothstep，不用手动 split。这是 Shader Graph 文档里容易遗漏的行为。
- **"把两个不同类型的边缘加起来"** 是 shield shader 的精髓——UV 边和 intersection 边是两个独立来源，简单 `Add`（配 `Saturate` 防溢出）就拼出了"能量护盾"视觉。
- 系列最长的一篇；Ilett 明确说这一部是"把前面学的节点组合起来做有层次的效果"的练习，不是引入多少新节点。
- 这一部用的 `DepthIntersection` 子图在 Mystery Dungeon sketch shader 时已经不够用（后处理没法用 Shader Graph 做），但**思想延续**——"从已有 depth texture 里推出 intersection" 是 2024 年 Ilett 后续教程的反复主题。

## 链接到的概念

- [[depth-intersection-subgraph]]
- [[scene-color-depth-nodes]]
- [[uv-manipulation-nodes]]
- [[stylized-water-shader]]
- [[fresnel-edge-highlight]]
- [[bloom-threshold-blur-composite]]
- [[classic-shader-noise]]

## 原文

- 链接：<https://danielilett.com/2024-05-28-tut7-13-intro-to-shader-graph-part-9/>
- 本地：`raw/articles/danielilett.com/2024-05-28_unity-shader-graph-basics-part-9-scene-intersections-2.md`
