---
tags: [渲染, 剔除, planet-engine, 地形, 球面]
date: 2026-04-27
sources: 1
---

# 球面映射地形的视锥剔除

在平面地形引擎中，tile 天然轴对齐，视锥剔除只需对 AABB 做平面距离测试（[[view-frustum-culling-ryg]] 中的 p/n-vertex 法）。但在行星引擎中，铺设在球面上的 quad-tree tile 有两层复杂性：**任意朝向**（tile 的局部坐标系随球面位置旋转）与**剪切变形**（向 quad-sphere 低层级靠近时，矩形 tile 被仿射剪切成非矩形四边形）。

## 剪切的几何来源

球面不能被无缝矩形网格覆盖，Outerra 使用 quad-sphere 投影。越靠近面的边缘，tile 的 u/v 轴相对世界坐标系越倾斜，产生显著的剪切（shear）分量。上层 tile 还存在更复杂的非对称变形，但向下深入 quad-tree 后剪切成为主导变形。

用 AABB 或 OBB 包裹这类 tile 会导致大量**假阳性**，尤其对高倾斜的边缘 tile 代价极高。

## 核心思路：把视锥平面变换到剪切空间

仿射剪切变换的关键性质是保留平面相交关系。因此可以将**视锥平面**变换到 tile 的局部剪切坐标系中，再在该坐标系内按普通 AABB 测试进行剔除，而无需把 tile 包裹成更松散的包围体。

具体做法：

1. 由 tile 的两个切向量 u、v（世界空间）构造旋转矩阵 `R`，第三行为 `normalize(cross(u, v))`。在 GLSL 中：
   ```
   R[0] = u;
   R[1] = v;
   R[2] = normalize(cross(u, v));
   // 变换时用转置（行→列）：R = transpose(mat3(u, v, n))
   ```
2. 对每个视锥平面，用 `R * plane.xyz` 将平面法线投影到 tile 的局部坐标系。
3. 在 tile 的局部坐标系中，tile 的半尺寸（extents）是已知的轴对齐值，对 `abs(R * plane.xyz)` 与 extents 做 dot product 即可求出"最远角点到平面的投影距离"。

由于 u、v 向量在 quad-tree 同一层级内变化很小，矩阵 R 可以**在一定层级以下缓存复用**，进一步节省运算。

## 实现要点

- 视锥平面法线需要归一化，平面第四分量 `d=0`（摄像机位于原点，除远平面外所有平面过原点）。
- 该方法等价于"变换视锥而非包围盒"，仿射变换下面-球相交性质不变。
- 对于非剪切的简单 tile（球面极点附近等），退化为标准 AABB 测试，无额外代价。

## 相关

- [[view-frustum-culling-ryg]] — p/n-vertex 的一般化平面-AABB 测试基础
- [[culling]] — 剔除层级总览
- [[obb-frustum-sat]] — OBB 与视锥的分离轴测试，另一种处理任意朝向包围盒的方式

## Sources

- [[sources/outerra-sphere-terrain-culling]]
