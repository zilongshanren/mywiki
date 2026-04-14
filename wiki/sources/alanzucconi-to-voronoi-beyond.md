---
tags: [source, rendering, shader, unity, voronoi, noise]
date: 2026-04-14
sources: 1
---

# To Voronoi and Beyond（Alan Zucconi）

[[alan-zucconi]] 于 2015 年 2 月发表的 Unity shader 教程，用一篇长文把 Voronoi 图的概念、距离度量、应用与 GPU 实现一次讲通。

## 摘要

文章从数学定义出发：Voronoi 图是一种把空间按"最近种子点"划分的镶嵌（tassellation），结果形态完全由距离度量决定。作者依次演示 Euclidean、Manhattan 和更一般的 [Minkowski 距离](https://en.wikipedia.org/wiki/Minkowski_distance)——后者用参数 `p` 在 `p=1`（曼哈顿）到 `p=2`（欧氏）之间平滑过渡，从而让同一份 shader 连续地变换 cell 形态。随后列举 Voronoi 在游戏里的三类常见用途：预先 Voronoi 切分的可破坏物体（Unity Fracturing & Destruction 插件）、用 Voronoi 边作为 AI 避敌的"最安全路径"、以及用 Delaunay 对偶图近似最短路径。文章还给出 Unity 里最朴素的实现：通过 undocumented 的 `SetFloatArray`/`SetVectorArray` 接口把 seed 点与颜色数组传给 fragment shader，再让每个像素 brute-force 扫描整个点集找最近点。最后提到 weighted Voronoi（Dirichlet tassellation）和 Chris Wellons 的锥体投影法（把 seed 点变成从上往下看的 cone，让深度测试自然解决"最近"问题，几乎零 shader 算力）。

## 关键要点

- 不同距离度量产生迥异的 cell 形状：Euclidean 给圆润多边形、Manhattan 给电路板式直角图案、Minkowski 用 `p` 参数在两者间插值
- Minkowski 公式 `D = (Σ|Δi|^p)^(1/p)` 是 Euclidean/Manhattan 的统一母式，shader 里只要一个 `pow` 就能实现"变形 Voronoi"
- Voronoi 在游戏里的经典落地：预切碎物体、AI 避敌路径（走 Voronoi 边）、最短路径近似（走 Delaunay 对偶图）
- Unity 的 brute-force shader 实现：`_Points[100]` + `_Length` + 对每像素 O(N) 扫描。简单但不可扩展
- 替代方案：Chris Wellons 的 cone projection——给每个 seed 画一个 cone 让 depth test 自动挑最近点，O(N) vs O(W·H·N)
- weighted Voronoi：在距离上加一个 `_Weights[i]` 偏移即可得到吸引力可调的细胞（Milan Domkář 的 foam lattice 即此类）
- 自然界的 circle packing 收敛到六边形 lattice（蜂巢、冷却熔岩、肥皂泡）——本质是同时扩张的圆在压力下退化成 Voronoi

## 链接到的概念

- [[worley-voronoi-noise]]（本篇补丁对象）
- [[alan-zucconi]]
- [[cellular-texture-generation]]
- [[sdf-2d-primitives]]

## 原文

- 链接：https://www.alanzucconi.com/2015/02/24/to-voronoi-and-beyond/
- 本地：`raw/articles/alanzucconi.com/2015-02-24_to-voronoi-and-beyond-alan-zucconi.md`
