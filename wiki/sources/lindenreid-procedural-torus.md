---
tags: [source, 程序化几何, mesh, 参数化曲面, limit-theory]
date: 2026-04-14
sources: 1
---

# Procedural Torus Tutorial（Linden Reid）

[[linden-reid]] 2017 年 11 月的程序化几何教程。她在文中说圆环是她"最喜欢的形状"——因为它看起来复杂，但数学上"美得惊人地简单"。文章以一种"视觉化数学"的口吻讲解为什么圆环只是两层嵌套的圆。

## 摘要

作者先从圆的参数方程出发：`x = cos(t)·r, y = sin(t)·r`，`t` 从 0 到 2π 等分取 n 个点。然后指出圆环的核心直觉——**在一个大圆的轨迹上运动一个小圆**。形式化成两个嵌套循环：外层用角度 θ 遍历大圆（stacks），内层用角度 φ 遍历小圆（slices）。顶点公式是 `x = cos(θ)·(outerR + cos(φ)·innerR), y = sin(θ)·(outerR + cos(φ)·innerR), z = sin(φ)·innerR`——把"当前截面的有效半径 `outerR + cos(φ)·innerR`"理解为随截面位置变化的圆半径。索引生成是一个 stack × slice 的二维网格，每相邻四个顶点构成一个 quad（两个三角形）。作者坦承她的实现**在接缝处存了重复顶点**（slice 的首尾没做取模），如果要算法线或做进一步的几何操作要么去重要么做坏三角形容错。文章最后推广到任意参数方程：可以把 `cos/sin` 替换成 hypotrochoid 之类的曲线得到"方形圆环"等变体，强调"torus 是一个 nested parametric equation"的心智模型。

## 关键要点

- 圆环 = 外层圆（轨道）× 内层圆（截面），共用 `cos/sin` 参数方程
- 投影半径 `outerR + cos(φ)·innerR` 是关键
- stack × slice 二维索引网格，每 4 顶点一个 quad
- 文章版本在 slice 接缝处存在重复顶点（known limitation）
- 把内外层的 `cos/sin` 换成任意参数函数 → 得到各种"异形环"

## 链接到的概念

- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[mesh-warps-and-tessellation]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/11/06/procedural-torus-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-11-06_procedural-torus-tutorial.md`
