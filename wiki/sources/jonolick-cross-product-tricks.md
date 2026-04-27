---
tags: [source, 图形, 数学, 几何, 叉积]
date: 2026-04-27
sources: 1
---

# Unusual Cross Product Tricks（Jon Olick）

[[jon-olick]] 发表于 2021 年 12 月的文章，介绍叉积在射影几何中"两点定直线、两线定交点"的对偶性技巧，并将其推广到三维的四维叉积。

## 摘要

本文的出发点来自计算机视觉中的对极几何（epipolar geometry）：在对极几何里，一张图像中的一个像素点对应另一张图像中的一条对极线，这条线可以通过叉积运算得到。Olick 把这个思想迁移到图形编程的日常工具箱。核心结论是：在齐次坐标下，叉积是一个**统一的"线性几何对象之间的对偶算子"**。两个 2D 点（补 1 升为三维齐次坐标）叉积得到过这两点的直线方程；两条直线叉积得到交点。在三维空间，三个三维点（补 1 升为四维齐次坐标）做四维叉积得到过三点的平面方程；三个平面做四维叉积得到三平面交点。文章给出了完整的 `cross4D` C 代码实现。

## 关键要点

- 2D 齐次坐标下：`cross3D(p0, p1)` → 直线方程，`cross3D(l0, l1)` → 交点（除以 z）
- 3D 齐次坐标下：`cross4D(p0, p1, p2)` → 平面方程，`cross4D(Π0, Π1, Π2)` → 交点（除以 w）
- 结果均为未归一化，使用前需归一化
- 该技巧源自对极几何 / Essential Matrix 的推导，被 Olick 引入图形编程

## 链接到的概念

- [[projective-cross-product-geometry]]
- [[homogeneous-rasterization-transpose-bug]]

## 原文

- 链接：https://www.jonolick.com/home/unusual-cross-product-tricks
- 本地：`raw/articles/jonolick.com/2021-12-09_unusual-cross-product-tricks.md`
