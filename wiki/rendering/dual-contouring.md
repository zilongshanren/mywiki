---
tags: [rendering, mesh, procedural-generation, isosurface, qef]
date: 2026-04-27
sources: 1
---

# Dual Contouring

Dual Contouring 是一种等值面提取算法，相比 [[marching-cubes]] 能够还原尖锐边角（sharp features），且实现逻辑更简洁。"Dual"来自图论对偶：原始网格的**单元格**变成输出网格的**顶点**，而不像 Marching Cubes 那样把顶点放在格的边上。

## 核心思路

算法在每个单元格内放置一个顶点，然后对每条有符号变化（sign change）的格边，将相邻单元格的顶点连成边（2D）或四边形面（3D）。由于每格只有一个顶点，没有 Marching Cubes 的 256 种情形查表，连线规则极为简单。

### 梯度信息

为了把顶点放在有意义的位置（而非格心），算法需要 f 的**梯度**（gradient），即法线/hermite data。对每条有符号变化的边，在交叉点处采样梯度，收集到一组"过某点、方向为法线"的约束。

### QEF（二次误差函数）

每条约束对应一个误差项：顶点偏离理想直线的距离平方。把所有误差项求和得到 QEF，求最小值点即为最优顶点位置，本质是一个最小二乘问题。

### QEF 的实践陷阱

当法线互相平行（共线）时，QEF 的极值点不唯一，求解结果可能飞到单元格外部，导致网格破损。推荐的组合方案：
1. **约束 QEF**：在求解时添加盒子约束，强制解在格内
2. **中心偏置**：在 QEF 中加一个以格心为最小点的弱惩罚项，把解拉向中心；法线共线时效果最强，法线分布良好时影响极小

Surface Nets 是"彻底放弃梯度"的极简变体，直接取格内交叉点均值作为顶点位置，简洁但丢失尖角信息。

## 扩展

- **八叉树（Octree）版本**：在需要细节的区域细分单元格，实现多分辨率，同等精度下面数更少
- **Remesh 应用**：可将另一个网格作为输入的 f（内/外判断 + 法线），Dual Contouring 输出干净的重构网格（Blender 的 Remesh 修改器即使用此思路）

## 相关

- [[marching-cubes]] — 前驱算法，理解 Dual Contouring 动机的基础
- [[greedy-voxel-meshing]] — 不同方向的体素网格优化策略

## Sources

- [[sources/boris-dual-contouring]]
