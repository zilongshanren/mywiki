---
tags: [渲染, 光照, 管线, forward, clustered, doom-2016]
date: 2026-04-27
sources: 1
---

# Clustered Forward Rendering（簇化前向渲染）

Clustered Forward Rendering 是一种将视锥体（camera frustum）在三维空间中分割为若干"cluster"（又称 froxel，frustum-shaped voxel），并为每个 cluster 预计算影响它的灯光/decal/探针列表的渲染架构。着色时像素只查询自身所属 cluster 的局部列表，而不是遍历场景内所有灯光。

这一技术由 Emil Persson 和 Ola Olsson 等人提出，并在 [[sources/adrian-doom-2016-graphics|DOOM 2016（id Tech 6）]]中得到工业级实现。

## 与 Tiled 和 Deferred 的对比

早期的 Tiled Forward Rendering 将视口按 2D 网格分块，为每个 tile 维护灯光列表，但无法区分同一 tile 内前后不同深度处的灯光影响差异。Clustered 方案将 2D tile 沿 Z 轴进一步切分为多个深度切片，形成真正的三维划分，消除了 tile-based 的深度歧义。

相对于 [[deferred-rendering]]，Clustered Forward 的优势在于：G-Buffer 开销低（无需为复杂材质多写多读缓冲区）、MSAA 支持更自然、透明物体处理更直接。其代价是 CPU 端预构建 cluster 索引结构需要额外开销，以及每次着色仍需在 per-pixel 循环灯光。

## DOOM 2016 中的实现

id Tech 6 将相机视锥体划分为 **3072 个 cluster（16 × 8 × 24）**，深度切片沿 Z 轴按对数方式分布（近端密、远端稀）。CPU 将所有灯光、decal 和 cubemap 探针与 cluster 做相交测试，生成每 cluster 最多 256 个的索引列表，存入 GPU buffer。像素着色器执行时，根据像素的屏幕坐标和深度计算所属 cluster，通过两级间接索引（offset + index）取出列表，循环计算贡献。

DOOM 同时还输出薄 G-Buffer（法线+高光），用于 SSAO、SSR 和 IBL 等后续效果——这是一种 **Hybrid Forward-Deferred** 混合架构：前向着色主 pass，G-Buffer 服务于屏幕空间效果。

## 适用场景

Clustered Forward 特别适合：灯光数量多但每个 cluster 实际影响灯光数有限的场景；需要 MSAA 的游戏；以及材质系统复杂不适合 G-Buffer 压缩的情况。DOOM 2016 的成功使这一架构在 2016 年后被更多引擎采用。

## Sources

- [[sources/adrian-doom-2016-graphics]]
