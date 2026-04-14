---
tags: [source, 渲染, decal, 法线贴图, fallout, cryengine]
date: 2026-04-14
sources: 1
---

# Fallout 3: Worn Edges（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 2013 年写的 Fallout 3 石头拆解，重点是 Bethesda 怎么用一层**额外的 decal 几何**把低多边形石头的硬边做成看起来像高多边形的破损轮廓。

## 摘要

Simon 先展示远观 / 近观 / wireframe 三张图：远看像高面数，近看才发现几何其实相当节省，破碎感来自一层薄壳几何贴着主 mesh 的轮廓。这层薄壳是一个带 alpha 的 **normal-mapped decal**——它不是 [[physically-based-shading|parallax mapping]]（Bethesda 这里没有 heightmap 输入），而是**真正的额外几何**，CryEngine 官方文档里把这种做法用于被破坏建筑的边缘。

Simon 通过 Intel GPA 关闭 Alpha1/AlphaTest 后看到了 decal 片的痕迹——虽然不算铁证，但足以支撑猜想。Crytek 的一位同事告知 Simon，他在 Bethesda 时的做法就和 CryEngine 文档描述一致：在高多边形 asset 上手摆 decal 壳，然后存进 prefab 供关卡美术复用。Simon 追问：怎么在 LOD 里处理这些 decal？答案很漂亮——**LOD 就是把 decal 删掉**，远景看不到细节，连 draw call 都省了。后续一位读者用 NifSkope 直接打开 `.nif`，肉眼确认 decal 网格是一层略大于实体边缘的薄壳，Simon 的猜想被完全证实。

文章还附带讨论 Bethesda 的纹理打包习惯：**normal map 的 alpha 通道存 specular**，因此 DXT5 一张顶两张。这种做法在 PBR 成为主流后（Skyrim Special Edition / Fallout 4）逐渐被放弃。

## 关键要点

- **Decal 壳** 是一种把「边缘轮廓 / 破损细节」从主 mesh 解耦出来的通用技巧，CryEngine 和 Bethesda 都在用
- 与 parallax mapping 相比，decal 是真实的几何，任意角度看都不会穿帮
- LOD 策略是**直接删掉**远距 decal，把细节成本严格限制在近景
- Bethesda 把 specular 存进 normal map 的 alpha 通道是**为了节省显存**（DXT5 vs DXT1 的 2× 差异），PBR 工作流后被边缘化

## 链接到的概念

- [[normal-decal-edge-blending]]
- [[normal-map-blending]]
- [[fizzle-lod-fading]]

## 原文

- 链接：https://simonschreibt.de/gat/fallout-3-edges/
- 本地：`raw/articles/simonschreibt.de/2013-01-21_simonschreibt-5.md`
