---
tags: [rendering, marching-squares, mesh, isosurface, algorithm]
date: 2026-04-27
sources: 1
---

# Marching Squares 歧义解析（Asymptotic Decider）

[[marching-cubes]]（2D 版本为 Marching Squares）存在一类**歧义情形（Ambiguous Cases）**：当一个格子的两对对角顶点颜色相反时（如左上与右下为"内"、左下与右上为"外"），有两种等效的边界连接方式，且单凭顶点布尔值无法判断哪种更正确。简单随机选择会导致网格中出现孔洞或不一致的拓扑结构。

## 问题形式化

设四个角顶按顺时针顺序为 top_left、top_right、bottom_right、bottom_left，歧义情形即：

- top_left 和 bottom_right 均为正（或均为负），且
- top_right 和 bottom_left 为相反符号。

此时有两种选择：将两个"正"角连接（一种拓扑），或将它们隔开（另一种拓扑）。

## Asymptotic Decider

当每个顶点不仅有布尔状态，还有具体**数值**（正表示实体，负表示空）时，可利用双线性插值（bilinear interpolation）推断格子内部的连通性。

计算判别量：

```
Q = top_left * bottom_right - bottom_left * top_right
```

- `Q > 0`：两个"正"角通过格子内部连通，选择"连接"情形。
- `Q < 0`：两个"正"角在内部不连通，选择"隔开"情形。

### 直觉解释

双线性插值将数值函数 f 扩展到格子内部每一点。通过分析 f=0 等值线在格子内的走向，可以确定哪种拓扑与连续曲面更一致。Q 的符号对应双曲线鞍点的走向，恰好决定了两个正角是否在内部相连。

原始论文：Nielson & Hamann，*The Asymptotic Decider: Resolving Ambiguities in Marching Cubes*（1991）。

## 3D 推广

3D Marching Cubes 有更多歧义情形，处理更复杂。常用方案包括：

- **Marching Cubes 33**：引入更多基本情形，通过类似判别量消歧。
- **Lewiner Marching Cubes**：更系统的拓扑正确版本，完整处理所有 3D 歧义。

[[dual-contouring]] 从根本上规避了这类问题，因为它在格内用 QEF（Quadric Error Function）直接求解最优顶点位置，不依赖查找表的拓扑假设。

## 相关

- [[marching-cubes]] — 基础算法，歧义问题来源于此
- [[marching-squares-multicolor]] — 多色扩展，同样存在歧义情形
- [[dual-contouring]] — 从根本上绕开歧义的替代方案

## Sources

- [[sources/boris-marching-squares-ambiguities]]
