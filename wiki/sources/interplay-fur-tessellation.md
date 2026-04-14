---
tags: [source, rendering, tessellation, fur, hair, d3d11, geometry-shader]
date: 2026-04-14
sources: 1
---

# Rendering Fur using Tessellation（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2014 年底的一篇技术笔记，分享他几年前入门 D3D11 时写的一个**用 tessellator 的 isoline 域生成毛发**的实验工程，并顺带给非图形读者做了一个简短的 D3D11 tessellation 科普。

## 摘要

文章前半段是 tessellation 101：patch / control point、tessellation factor、三种 domain（triangle / quad / **isoline**）、四种 partitioning（integer / pow2 / fractional odd / even）、以及 hull → tessellator → domain 的三阶段管线——hull 拆成 control-point shader（逐顶点，能看到整个 patch）和 patch-constant shader（逐 patch，输出 tessellation factors）；fixed-function tessellator 在归一化 UVW 域上生成新点；domain shader 拿着这些新点加上插值的控制点做真正的位置生成。后半段是 fur 方案：**选 isoline 域**——它输出 64 条线 × 每条 64 段的 UV 点——一个 UV 分量解释成"第几根毛"，另一个解释成"毛的第几段"。domain shader 根据 line 号从一张**随机 barycentric 坐标**表里找毛的起点（CPU 预生成，避免 hash 在 shader 里），根据 segment 号沿法线向上扩展。hull shader 只负责 backface cull——把 tessellation factor 写 0 能让 tessellator 完全不产出点。如果一个三角形需要超过 64 根毛（密度高的区域），就用多 pass 渲染。纯线无体积感，再挂一个 geometry shader 把线转换成 triangle strip 给毛加宽度。最后补上 MSAA x4（必须）、anisotropic highlight + rim light、Emil Persson 的 **Phone Wire AA**（受限于 alpha 排序问题只保留了最小宽度那一半）。同一套 pipeline 几乎不改直接拿去渲染草地也 work。

## 关键要点

- **isoline domain 是 fur 的天然选择**：它产出 2D UV 是"线号 × 段号"的二维阵列，正好对应"每根毛 / 每根毛的每段"的数据结构。tessellator 不懂 mesh 概念，它只在归一化域上产点，这让同一 pipeline 适用于任何 mesh。
- **最大输出 64 × 64**。超过需要多 pass 或更密的 base mesh。Anagnostou 在每个三角形上按面积计算密度，超 64 就继续 pass。
- **Master strand + barycentric 插值**是简化模拟成本的关键。长毛、有碰撞/风模拟时，不要对所有毛做 simulation——只对每个三角形顶点的"主毛"做，渲染时 domain shader 用 barycentric 把三根主毛插值到每根子毛。模拟成本 $O(\text{顶点数})$ 而不是 $O(\text{毛数})$，但**主毛本身也必须被渲染**（被插值子毛的端点覆盖）。
- **hull shader 写 0 tessellation factor** 是廉价 backface culling 的手段，对 fur / grass 要保守——即使基础面背向相机，靠近 silhouette 的毛可能仍然可见。
- **geometry shader 给线加宽度**。tessellator 只输出 line primitive，要有"毛宽度"必须接一个 GS 把每段线扩成两个三角形；宽度来自 screen-space 的 billboard 式扩展。
- **MSAA 对细线几何是强制**：x4 就能明显改善，x8 边际收益小。**Phone Wire AA**（最小宽度 clamp + 差值 alpha 淡出）本来可以处理更远距离的 hair breakup，但 alpha sort 在 fur 密度下做不稳定，作者只留了最小宽度部分。
- **数据流用 structured buffer 走**：main mesh、主毛、barycentric 表都是 SRV；vertex buffer 只有一个占位点，**index buffer 的长度 = 三角形数** 是实际触发 tessellation pipeline 的机制。
- **同一 pipeline 几乎零改动转草**。isoline + 向上扩展本来就是"密集小线段几何"的通用形状，fur vs grass 的差别主要是 shading（anisotropic 还是 diffuse 色带）和长度/密度。

## 链接到的概念

- [[tessellation-fur-rendering]]
- [[deferred-grass-shader]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2014/12/31/rendering-fur-using-tessellation/
- 本地：`raw/articles/interplayoflight.wordpress.com/2014-12-31_rendering-fur-using-tessellation.md`
