---
tags: [渲染, 光照, 分块, 层级加速结构, 延迟渲染]
date: 2026-04-19
sources: 1
---

# Tiled Light Trees

**Tiled Light Trees** 是 Yuriy O'Donnell（Frostbite）和 Matthäus Chajdas 在 I3D 2017 提出的**分块 + 层级光源加速结构**混合方案，目标是改善高光源场景下 [[tiled-light-culling|分块光源剔除]] / clustered shading 的最坏情况：**当场景深度方差很大时，一个 tile / cluster 里混入大量根本不贡献的光源**，shading pass 被迫对它们跑完整的剔除测试。

## 问题：clustered shading 的"坏 tile"

[[tiled-light-culling|Clustered shading]] 是目前主流的大量光源处理方案：屏幕切成 tile，深度再切成 cluster，每个 cluster 预先算出可能影响它的光源列表。问题在于**深度方差**：同一 tile 从脚底 1 米看到远山 1000 米时，cluster 沿深度轴划分得再细，也会有几个 cluster 装进几十个光源——而且这些光源在空间上并不聚簇。Shading pass 对每个像素都要把它所在 cluster 的光源列表线性扫一遍，扫到的多数又会被 per-pixel 剔除——这就是"坏 tile"现象。

## 思路：tile 内再建层级

Tiled light trees 的做法是**在每个 tile 内部构建一棵小的 BVH 风格层级**：tile 内的光源先做一次预划分，生成一棵以 AABB / 球为节点的树，shading 时在树上遍历——远离当前像素的子树可以**整棵剪掉**，不用逐光源测试。这相当于把 [[culling|BVH culling]] 的经典技术下沉到 tile 粒度。

由于每个 tile 的光源数一般 < 256，树本身很小，**构造开销被控制在 tile 级预处理**；遍历时 early-out 在高深度方差场景下显著减少比较次数。

## 混合策略：tree + clustered shading

论文坦承 light tree 的**遍历开销**有时会超过 clustered shading 的线性扫描——对**光源均匀分布、tile 深度方差小**的场景，clustered shading 的 branchless 线性扫比树遍历更快。O'Donnell 和 Chajdas 的关键贡献是**混合方案**：

- 每个 tile **同时**有 clustered shading 的光源列表和 light tree。
- 运行时根据 tile 的深度方差和光源数量**选择**：方差小、光源数少时走 clustered；方差大、光源数多时走 tree。

混合方案在**几乎所有实测场景下都不慢于任一单路**，并在最坏情况下显著优于两者。

## 工程价值

Tiled light trees 是 Frostbite 当年探索的一条路径，虽然没有完全替代 clustered shading 成为行业默认，但它的观察——**clustered shading 的坏 tile 问题靠在 tile 内部建层级来缓解**——后来在 UE5 Lumen 的 light grid 和 [[brian-karis|Karis]] 的 specular cone culling（见 [[tiled-light-culling]]）中都能看到类似思想：**tile 级的可见性剪枝需要 BRDF / 几何感知，而不是单纯距离球**。

## 相关

- [[tiled-light-culling]] —— 经典 tile 粒度的距离剔除 + Karis 的 specular cone 改良
- [[tiled-light-prepass]] —— Foundation 引擎的 thin G-Buffer 光照方案，结构正交
- [[deferred-rendering]]
- [[culling]] —— BVH / cone culling 的经典形式
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-tiled-light-trees]]
