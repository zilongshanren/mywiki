---
tags: [source, 程序化几何, mesh, limit-theory]
date: 2026-04-14
sources: 1
---

# Procedural Mesh Extrusion Tutorial（Linden Reid）

[[linden-reid]] 2017 年 11 月为 #PROCJAM 写的程序化几何教程系列第二篇。承接 stellation：把每个三角形沿法线推出去做成三棱柱。

## 摘要

单三角形的 extrusion 流程与 stellation 非常相似，但顶点数与拓扑不同：先算法线 `normal = normalize(cross(v2-v1, v3-v2))`，然后创建三个新顶点 `v4 = v1 + normal*h, v5 = v2 + normal*h, v6 = v3 + normal*h`。原三角形的三条边与新三角形的对应边组成三个 quad 侧面 + 一个顶面，总共 **7 个三角形**（侧面 2×3 + 顶面 1）。原三角形的索引在整 mesh 循环里被丢弃，因为会被侧面/新顶面盖住。整 mesh 版本与 stellation 的骨架完全一致，只是每轮 vi 计数器要 +3 而不是 +1，因为每次生成 3 个新顶点。作者建议靠画图来确认索引的 winding order，并强调这类 warp 可以和 stellation 组合——对同一个 mesh 交替应用，或改变 h 重复应用，得到渐进式的程序化外形。

## 关键要点

- Extrusion = 沿法线平移三个顶点，得到三棱柱（顶面 + 三个 quad 侧面）
- 7 个新三角形的索引需要手画出来
- 每个三角形新增 3 顶点，索引计数器每轮 +3
- 原三角形会被侧面盖住，所以跳过不加到新 mesh
- 与 stellation、multi-pass 应用、变 h 等可以组合产生复杂形状

## 链接到的概念

- [[mesh-warps-and-tessellation]]
- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[triangle-primitives]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/11/05/procedural-mesh-extrusion-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-11-05_procedural-mesh-extrusion-tutorial.md`
