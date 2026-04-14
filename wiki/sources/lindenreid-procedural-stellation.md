---
tags: [source, 程序化几何, mesh, limit-theory]
date: 2026-04-14
sources: 1
---

# Procedural Stellation Tutorial（Linden Reid）

[[linden-reid]] 2017 年 11 月为 #PROCJAM 写的程序化几何教程之一，内容是把一个 mesh 的每个三角形"拱成"金字塔（tetrahedron），产生星状多面体。作者当时在 Procedural Reality 做 Limit Theory 的程序化飞船与空间站。

## 摘要

教程先讲单个三角形的 stellation：给定三个顶点 `v1, v2, v3`，算出重心 `center = (v1+v2+v3)/3` 与法线 `normal = normalize(cross(v2-v1, v3-v2))`，然后在 `center + normal * h` 处放一个新顶点 `v4`。h 是可调的拉伸距离。把原三角形的三条边分别与 `v4` 相连就得到 3 个新三角形，原三角形被丢弃（会被新侧面盖住）。作者强调**索引方向必须遵循 winding order**（Limit Theory 用 counter-clockwise）、**画图胜过硬算**、**退化三角形要检查法线长度大于 0**。然后把算法推广到整个 mesh：先把所有旧顶点按原顺序塞进新 mesh，再按旧三角形列表迭代 stellate，每次 `vi` 索引递增 1。反复应用这个函数可以得到越来越"尖锐"的多面星。

## 关键要点

- Stellation = 对每个三角形建一个 tip 顶点 + 3 个新三角形
- 法线用 `cross(e1, e2)` 再 `normalize`；对坏三角形要检查 length > 0
- winding order 决定索引顺序（CCW: `(i1,i2,i4), (i2,i3,i4), (i3,i1,i4)`）
- 整 mesh 循环时维护一个"下一个新顶点索引"计数器，每轮 +1
- 重复 stellate 同一 mesh 得到分形星体（见文末 Twitter 展示）

## 链接到的概念

- [[mesh-warps-and-tessellation]]
- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[triangle-primitives]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/11/04/procedural-stellation-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-11-04_procedural-stellation-tutorial.md`
