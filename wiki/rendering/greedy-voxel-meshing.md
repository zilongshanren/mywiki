---
tags: [渲染, 体素, 网格生成, 优化]
date: 2026-04-14
sources: 1
---

# 贪心体素 meshing（Greedy Voxel Meshing）

**Greedy meshing** 是把一块 voxel 数据（典型是 Minecraft 风格的 $N \times N \times N$ 块区域）转成**尽可能少的四边形**的经典算法。它同时解决两个问题：

1. **剔除被完全遮挡的面**——相邻两个实心 voxel 之间的面永远看不见。
2. **合并同属性的相邻面**——连成一大片的草地顶面可以用一个大 quad 表示，而不是 $N^2$ 个单位方格。

在体素世界里，「渲染」的瓶颈几乎从来不是 GPU 算力，而是 `draw call` / 顶点数 / 内存带宽。把 $O(N^3)$ 的 voxel 数据压成 $O(N^2)$ 量级的几何，一个 chunk 从几万顶点降到几百个——GPU 静态 mesh 渲染就是最爽的那种「把一切交给 VRAM」。

## 算法骨架

对每个 chunk 的 6 个面方向分别处理（+X, -X, +Y, -Y, +Z, -Z）。对每个方向：

1. 切出垂直于该方向的二维 mask，每个格点存「这个位置有一个面吗？如果有，它的 face type 是什么？」
2. 在 mask 上做贪心合并：从左上到右下，找到第一个未处理的格点，向右扩展到类型不同或越界为止，再向下扩展同样多行——这就是这个面的矩形范围。
3. 把该范围标记为已处理，输出一个四边形。

面的「类型」是贪心合并的 key：方向 + 材质 ID + 光照 / AO 掩码的 tuple。两个面只有 tuple 完全一致才能合并。

## 权衡

- **和 geometry shader 生成的方案比**：geometry shader 可以更省内存（一个面只存一个 vertex），但 greedy mesh 出的静态 mesh 跑得更快——静态 mesh 是 GPU 最爱的路径。
- **和 marching cubes / dual contouring 比**：后者支持平滑表面，greedy mesh 只能出方块风，但逻辑简单、重新生成快，适合需要频繁编辑的 Minecraft-like 世界。
- **重新生成延迟**：一个 chunk 内的一个 voxel 改变就要重 mesh 整个 chunk（或者至少一个方向）。chunk 要选得够小以控延迟，又得够大以摊薄固定成本——Exile 选 31×31×511，Minecraft 选 16×16×256。

## 和 [[voxel-ambient-occlusion]] 的配合

AO 值在 mesh 生成时就计算并烘到顶点属性里，保持「静态 mesh + 简单 shader」这条 hot path。AO mask 是贪心合并 key 的一部分，所以只有四个角 AO 一致的连续面才能合并——细节处理不好会看到伪影。

## 相关

- [[voxel-ambient-occlusion]] — 两者通常一起实现
- [[compact-vertex-format]] — 合并后还需要压缩每顶点数据
- [[max-slater]]
- [[skysaga-rendering-tech]] —— Meandros 引擎中 greedy meshing + chunk-based occlusion 的组合应用

## Sources

- [[sources/slater-exile-voxel-rendering]]
