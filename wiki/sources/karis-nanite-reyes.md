---
tags: [source, 渲染, nanite, reyes, tessellation, 软光栅]
date: 2026-04-19
sources: 1
---

# Nanite + Reyes（Brian Karis / Graphic Rants）

[[brian-karis|Karis]] 2026-02-06 的第四篇，本系列最长。把 UE5.4 Nanite Tessellation 的**完整流水线**摊开——ClusterRasterize 扩展、PatchSplit、PatchRasterize，以及 DS 自动导数缺失这个老问题的权宜解法。

## 摘要

Nanite 的 LOD 仍按原始表面误差（位置 + 法线）决策，位移影响被忽略（shader 不可知）；同一 mesh 里可以**同时**被 Nanite 简化（小 patch 合并）和被 tessellation 放大（大 patch 细分）。**ClusterRasterize** 扩展成：TessFactor ≤ 1 直接光栅化、≤ MaxDiceFactor 进 dice queue、否则进 split queue。位移函数必须执行所以是 per-material shader。**PatchSplit** 是**全局 shader**——为支持 async overlap 和避免 per-material dispatch 的 spin-up 浪费，所有 split 决策必须 fixed function、不能执行位移、不能读 programmable normals。subpatch 用 16 字节 (cluster idx + tri idx + 3 个 16:16 barycentric)。递归展开最初用 persistent threads + lockless queue（与 Nanite cluster culling 同构），但 D3D spec 在 PC 上不保证前进，现在 PC 走 multipass，主机仍用 persistent threads。位移范围由 artist 手填（最常被踩坑的地方）。

**PatchRasterize** 纯软光栅（micropoly 永远小不到需要 HW）。踩坑：RDNA3 前 scalar float 实际走 vector unit 一条 lane，Rune Stubbe 的优化把多个 patch 摊到一个 wave（用 `WaveReadLaneAt` 跨 lane 拿数据）；跳过 normal 归一化让 transform 变线性从而可共享；没有 MaxEdgeLength 保护，陡位移让三角形被软光栅的 64 像素 clamp 裁成撕裂。**DS 自动导数缺失**：Tessellation Table 不规则，无法有限差分；用链式法则 `dUV/dTessFactors = dUV/dXYZ · dXYZ/dTessFactors`，第二项等于 1/DicingRate（连续），第一项 piecewise constant 且 corner valence 不定——只能 preprocess 时按顶点存，多 UV 套要分别存，增加 heavyweight data。

## 关键要点

- Nanite LOD **只看原始 mesh 误差**，对位移完全不可知。
- **PatchSplit 必须是 global shader**——决定了一切 split 时的位移逻辑都得是 fixed function。
- Persistent threads 在 PC 上被迫改 multipass（spec 合规），async overlap 掩盖 drain。
- **位移范围由 artist 手填**，踩坑最多；屏幕 bounds 用 Niessner-Loop 棱柱并集。
- **Scalar float 坑**：Rune Stubbe 的多 patch-per-wave 优化；normal 不归一化让 VS 侧可共享。
- **软光栅的 MaxEdgeLength 保护**缺失——陡位移导致 64 像素 clamp 撕裂。
- **DS 自动导数**：链式法则近似 + 每顶点预存第一项。

## 链接到的概念

- [[nanite-tessellation-approach]]
- [[nanite-reyes-comparison]]
- [[variable-sized-work-pattern]]
- [[visibility-buffer]]
- [[virtual-shadow-maps]]
- [[nanite-virtualized-geometry]]

## 原文

- 链接：<http://graphicrants.blogspot.com/2026/02/nanite-reyes.html>
- 本地：`raw/articles/graphicrants.blogspot.com/2026-02-06_nanite-reyes.md`
