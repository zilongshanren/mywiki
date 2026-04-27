---
tags: [source, graphics, math, vectors, 图形数学]
date: 2026-04-27
sources: 1
---

# Points, Vertices and Vectors（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 2011 年 5 月发表的图形数学入门文章，面向想学习计算机图形学的工程师，是他计划系列课程材料的第一篇。

## 摘要

文章系统介绍了 3D 图形编程所需的核心数学基础：点与向量的区别（点是欧氏空间中的位置，向量是两点之差描述方向与距离）；向量的标量乘法、加法、减法与平行四边形法则；齐次坐标如何用第四分量 w=0/1 区分向量与点；勾股定理推广至三维空间用于计算向量长度；单位向量的定义与归一化过程；笛卡尔单位向量 i/j/k 的代数操作；点积（标量积）的几何解释（投影）与代数表达式，以及在 Lambert 漫反射光照中的应用；叉积（向量积）的右手定则与行列式计算方法，以及在求三角形法线和面积中的用途。文章以派生三角形单位法向量为最终综合示例。

## 关键要点

- 点（Point）与向量（Vector）分属不同空间：欧氏空间与向量空间；坐标独立性是区分它们的根本动机
- 齐次坐标 `[x, y, z, w]`：w=0 表示方向（向量），w=1 表示位置（点），支持平移变换的矩阵形式
- 点积 `R·S = |R||S|cosβ`；单位向量之间的点积直接等于夹角余弦，适合硬件 `dot()` 内置函数
- 叉积 `R×S = T` 且 `|T| = |R||S|sinθ`；结果向量垂直于 R 和 S，右手定则决定方向；不满足交换律
- 叉积模等于平行四边形面积，三角形面积 = `|R×S| / 2`；可用于计算网格表面面积
- 未归一化法向量的符号反映三角形顶点顺序（顺时针 / 逆时针）

## 链接到的概念

- [[vector-dot-product]]
- [[shader-vector-math-primer]]
- [[3d-rotation-math]]
- [[homogeneous-rasterization-transpose-bug]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/05/points-vertices-and-vectors.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-05-29_points-vertices-and-vectors.md`
