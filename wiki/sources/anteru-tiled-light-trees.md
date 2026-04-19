---
tags: [source, 渲染, 光照, 分块]
date: 2026-04-19
sources: 1
---

# Tiled Light Trees（I3D 2017）

O'Donnell（Frostbite）和 [[matthaeus-chajdas|Chajdas]] 发表于 **ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2017** 的论文。详细算法见 [[tiled-light-trees]]。

## 摘要

实时处理大量光源仍是实时图形的主要挑战之一。即便是 practical clustered shading 这类最新方案也存在性能塌陷的坏例——尤其是**高深度方差**场景中，现有算法无法适应光源分布，最终会评估大量对最终图像无贡献的光源。

作者提出 **"tiled light trees"**：一种**适应光源分布的层级加速结构**，改善现有方案的最坏情况。由于 traversal 开销，算法有时会慢于 clustered shading。为最优处理这些情况，作者进一步提出**混合方案**——结合 light tree 与 clustered shading 的优势，**几乎在所有场景下都优于任一单独方案**。混合算法易于实现，适合实时应用（如游戏）。

## 关键要点

- **问题定义**：clustered shading 的坏 tile——高深度方差下光源列表膨胀且不聚簇。
- **光源 BVH 下沉到 tile 级**：每个 tile 内部的光源建小树，遍历时 early-out 剪大段。
- **混合策略**：按 tile 的深度方差/光源数自适应切换 tree / clustered。
- 这是 Frostbite 团队在 UE5 Lumen 时代前对"**tile 内的光源可见性剪枝**"问题的一次系统性尝试，思想上和 [[tiled-light-culling|Karis 的 specular cone culling]] 并列——都承认 tile 内部需要比"球距离"更精细的剔除信号。

## 链接到的概念

- [[tiled-light-trees]]
- [[tiled-light-culling]]
- [[deferred-rendering]]
- [[matthaeus-chajdas]]

## 原文

- 链接：<https://anteru.net/research/tiled-light-trees>
- 预印本：<https://anteru.net/files/2017/TiledLightTrees-preprint.pdf>
- 本地：`raw/articles/anteru.net/2025-02-16_tiled-light-trees.md`
