---
tags: [rendering, mesh, procedural-generation, isosurface, voxel]
date: 2026-04-27
sources: 3
---

# Marching Cubes

Marching Cubes 是一种从标量场（scalar field）提取等值面的经典算法，输入是一个在空间中可求值的函数 f(x)，输出是近似表示 f=0 等值面的多边形网格。广泛用于破坏性地形、MRI 医学可视化、metaballs 渲染等场景。

## 核心原理

算法将空间划分为均匀网格，对每个单元格的所有角点评估 f 的正负状态。在 2D 中，一个正方形格有 4 个角点，共 2⁴=16 种状态；在 3D 中一个立方格有 8 个角点，共 256 种状态（利用对称性可简化为 15 种基本情形）。每种状态通过查找表对应一组固定的边界线段（2D）或三角面（3D），各格独立处理后拼合成完整网格。

### 自适应版本

基本版本将边界顶点放在格边中点，导致明显的 45° 阶梯感。自适应版本利用 f 的数值（而非仅布尔状态）对边缘两侧的值做线性插值，将顶点放在更接近真实等值面的位置，视觉质量显著提升。

## 局限性

- 无法还原尖锐边角（sharp features）：格内的边界线/面始终位于格的内部，无法触达格的顶点，因此正方形的角会被截断
- 存在歧义情形：2D 中两个对角线上的"内"点既可以连成一个通道也可以断开，选择不一致会导致 3D 中的漏洞网格

这两个问题促成了 [[dual-contouring]] 的设计。

## 实现参考

Boris The Brave 提供了带注释的 Python 实现：[mc-dc on GitHub](https://github.com/BorisTheBrave/mc-dc)

## 相关

- [[dual-contouring]] — 解决 Marching Cubes 歧义和尖角问题的改进算法
- [[greedy-voxel-meshing]] — 另一种体素网格化策略，侧重面数优化
- [[marching-squares-multicolor]] — 多色 2D 扩展，支持 N 种颜色区域间的边界绘制
- [[marching-squares-ambiguities]] — Asymptotic Decider 方法系统消解歧义情形

## Sources

- [[sources/boris-marching-cubes]]
- [[sources/boris-2d-marching-cubes-multicolor]]
- [[sources/boris-marching-squares-ambiguities]]
