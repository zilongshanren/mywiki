---
tags: [source, 渲染, tessellation, nanite, displacement]
date: 2026-04-19
sources: 1
---

# Nanite Tessellation（Brian Karis / Graphic Rants）

[[brian-karis|Brian Karis]] 2026-02-01 发表的 Nanite Tessellation 系列**开篇**，交代 UE5.4 里动态 tessellation + displacement 系统的**动机**。系列计划共 ~7 篇：Intro / Possible approaches / How to tessellate / Nanite + Reyes / Variable sized work / Vertex dedup / VisBuffer & Deferred materials / Wrapping up。

## 摘要

Karis 解释为什么在有了 [[nanite-virtualized-geometry|Nanite]]"通用几何虚拟化"之后还需要 geometry amplification：因为**位移**是一个对**通用**解来说代价不划算的特例。位移能享受三重优势——数据压缩（1 个 scalar vs. 5+ 属性）、程序化纹理（tiling / detail texture / shader mix 的时间与动态优势）、艺术家工作流（和电影业一样的 sculpt-then-displace、rig-then-displace）、以及 Fortnite 这种大 scalability 游戏天然偏好"低模 + 放大"。因此 UE5.4 在 Fortnite 地面和 *Marvel 1943: Rise of Hydra* demo 里 ship 了这套系统。

## 关键要点

- **功能定义**：shader graph 定义的位移函数，在运行时动态 tessellate Nanite 基础 mesh。
- **哲学不变**：Nanite 的"authoring decisions should have no impact on performance"仍是目标，但坦承"未完全实现"。
- **为什么不靠 Nanite 自身放大**：Karis 过去公开论证过 amplification 不是虚拟化几何的通用方案（不能改 genus）——但这不等于 amplification **没有**自己的合适场景。
- **三重优势**：压缩（scalar + 2D 通用 + 程序化）、艺术家工作流（雕刻、rig、动画解耦）、scalability（艺术家更愿意低模 + 放大而非高模 + 简化）。

## 链接到的概念

- [[tessellation-approaches-overview]]
- [[nanite-tessellation-approach]]
- [[nanite-reyes-comparison]]
- [[nanite-virtualized-geometry]]

## 原文

- 链接：<http://graphicrants.blogspot.com/2026/02/nanite-tessellation.html>
- 本地：`raw/articles/graphicrants.blogspot.com/2026-02-01_nanite-tessellation.md`
