---
tags: [source, 程序化几何, mesh, tessellation, limit-theory]
date: 2026-04-14
sources: 1
---

# Simple Mesh Tessellation & Triangulation Tutorial（Linden Reid）

[[linden-reid]] 2017 年 12 月的教程，把 mesh 细分与多边形三角化讲成三个"接地气"的算法。作者开头就免责声明：这不是计算几何教科书里的标准术语，而是她自己起的名字，面向游戏和程序化几何的实用派。

## 摘要

三个算法分别是：**Fan**（扇形三角化）——把 n 边形从第一个顶点出发连线到其他所有顶点对，不加新顶点，最省数据，但会产生畸形的尖角，适合作为最后一步交给 renderer。**Centroid**（质心三角化）——在多边形的顶点平均位置添加一个新顶点，然后从中心向每条边的两个端点连线，对 n 边形产生 n 个三角形，角度比 fan 更均匀，适合在 warp 之前做预处理。**Triforce**（Triforce 细分）——只在三角形上工作，取三条边的中点把原三角形切成 4 个小三角形（3 角上的 + 中间反向的），对等边三角形产生 regular tessellation，对非等边保角。实现上用一个 `edgeMap`（以 `min(v1,v2) * vc + max(v1,v2)` 为 key）避免相邻三角形在共享边上创建重复的中点顶点。

作者把这三种算法的用法放在 Limit Theory 的实际流水线里：先用 centroid 把高阶多边形降成三角形，然后用 triforce 反复细分得到更密的 mesh，再去应用 [[mesh-warps-and-tessellation|stellation 或 extrusion]]。fan 则作为最后一步省数据给 renderer。

## 关键要点

- 三个算法的命名是作者自创（fan / centroid / triforce），不是教科书术语
- Fan：不加新顶点，最省数据；但畸形尖角，不适合做 warp 的输入
- Centroid：加 1 新顶点，角度均匀，warp 前首选
- Triforce：加 3 条边中点，保角，对等边三角形产生 regular tessellation
- Triforce 必须用 edgeMap 去重，key = `min·vc + max` 的顶点索引 pair
- 典型流水线：centroid → triforce ×n → stellation/extrusion

## 链接到的概念

- [[mesh-warps-and-tessellation]]
- [[procedural-mesh-primitives]]
- [[unity-procedural-mesh]]
- [[triangle-primitives]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/03/simple-mesh-tessellation-triangulation-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-03_simple-mesh-tessellation-triangulation-tutorial.md`
