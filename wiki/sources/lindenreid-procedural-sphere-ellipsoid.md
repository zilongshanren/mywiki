---
tags: [source, 程序化几何, mesh, 参数化曲面, limit-theory]
date: 2026-04-14
sources: 1
---

# Procedural Sphere / Ellipsoid Tutorial（Linden Reid）

[[linden-reid]] 2017 年 11 月的 UV-sphere 教程。她强调大多数网上教程只给代码不解释"为什么"，所以这篇的重点是把球看穿——先懂简单基元，才能建复杂的 torus、stellation、extrusion 等。

## 摘要

教程从圆的参数方程出发铺垫 "parametric" 的概念——坐标是角度的函数。进入 3D 时引入两层循环：外层 stack 用 `θ` 扫南北方向（只走 `[0, π]` 而不是 `[0, 2π)`，因为半圈就够描述上下半球），内层 slice 用 `φ` 扫经度（`[0, 2π)`）。每个 stack 的水平半径 `stackRadius = sin(θ)·r` 随高度缩放：赤道最大、两极为 0。顶点公式是 `x = cos(φ)·stackRadius, y = cos(θ)·r, z = sin(φ)·stackRadius`。南北两极是奇点（`sin(θ)=0` 导致所有 slice 塌到同一点），所以**硬编码**两个极点顶点并让 stack 循环从 1 到 n−1。索引生成分三段：顶极扇、中间 quad 网格、底极扇——每段的 winding order 都要单独推理。

把球推广到椭球只需要**把 `stackRadius` 拆成两个 (stackRadiusX = sin(θ)·width, stackRadiusZ = sin(θ)·length)**，再把 y 方向的半径替换成 `height`。三轴独立后可以做任意比例的 sphere-like 形状。作者说这套学出来就为之后学 icosasphere、torus、warp 打下基础——基元的拓扑结构是固定的，只在参数层面变化。

文章末尾读者评论里有人问 `res` 是什么——应该就是 `n`（subdivisions），属于文本里的变量不一致。

## 关键要点

- UV 球 = "半径随 y 位置变化的圆环层叠"
- θ ∈ [0, π]（只扫半圈）、φ ∈ [0, 2π)
- 两极是参数奇点，需要硬编码并把循环缩减一格
- 椭球 = 球的 `stackRadius` 按 X/Z 各向异性拆分 + 独立 height
- 索引需要分顶极扇、中间 quad 网格、底极扇三段处理
- 这是 UV-sphere 方法，与 icosasphere 方法互补（顶点均匀性不同）

## 链接到的概念

- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[mesh-warps-and-tessellation]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/11/07/procedural-sphere-ellipsoid-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-11-07_procedural-sphere-ellipsoid-tutorial.md`
