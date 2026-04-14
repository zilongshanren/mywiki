---
tags: [source, 程序化几何, mesh, extrusion]
date: 2026-04-14
sources: 1
---

# Procedural Greeble Tutorial（Linden Reid）

[[linden-reid]] 2017 年 12 月为 Limit Theory 程序化几何系列写的教程，把前作「三角形 extrusion」推广到任意 n 边形 polygon，并用它批量生成科幻模型上的「greeble」细节。

## 摘要

Greeble 是指科幻 mesh 上那种细碎凸起，作者先抱怨了一下这个词再开工。算法两步：**给出任意 n 边形 polygon 的法线**（遍历所有 `(v1, v1+i, v2+i)` 三角叉积取均值，比固定两边更稳），然后对每面 **extrude 出一层新顶点、沿法线偏移、用 quad 缝合侧壁、用新 polygon 替代原面**。核心 greeble 函数就是对每面随机抽一个长度 `length ∈ [0.1, 1.0]` 再调 extrude。为避免结果过于均匀，作者给了两条改造：用 `random.chance(0.33)` 随机决定是否 extrude 这一面，以及在 extrude 内部用 `scale` 参数把新 polygon 的顶点向重心方向 lerp 一下——形成梯形台而不是方盒，视觉上更像法兰、螺栓、面板。代码是 Lua 伪代码，面向 Limit Theory CPU mesh API 但算法 API 无关。

## 关键要点

- n 边形 polygon 的法线取所有三角扇叉积平均
- Extrude = 复制顶点 + 沿法线偏移 + 侧壁 quad 缝合 + 替换原面
- 随机 length 产生 greeble 细节，全算法只有一个 for 循环
- `random.chance()` 做稀疏化，`scale` 做顶面收缩带来梯形台
- 与 stellation / 二次 extrusion 可组合递归应用

## 链接到的概念

- [[procedural-greeble]]
- [[lindenreid-procedural-extrusion]]
- [[mesh-warps-and-tessellation]]
- [[procedural-mesh-primitives]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/13/procedural-greeble-tutorial/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-13_procedural-greeble-tutorial.md`
