---
tags: [source, 渲染, shader, 数学, 旋转]
date: 2026-04-14
sources: 1
---

# Mini: Rotation（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 9 月的一篇，面向初学者讲**如何旋转一个 2D 向量**——从水平线段的三角函数出发推出 `mat2` 旋转矩阵，再用「每次只转两个轴」把方法扩展到 3D。是他 2025 年 10 月那篇更偏表示比较的 [[sources/xor-mini-3d-rotation|Mini: 3D Rotation]] 的前置教程。

## 摘要

Xor 用几何直觉把 2D 旋转矩阵推导清楚：一条从 A 出发、长 `L` 的水平线旋转 `θ` 后，终点 B 的偏移是 `(cos θ, -sin θ) * L`（屏幕坐标 y 向下，所以负号）。一条垂直线段旋转后偏移是 `(sin θ, cos θ) * L`——水平和垂直旋转的分量刚好「x/y 互换」。对任意向量 `(x, y)` 做旋转就是两者的线性组合，写成 `mat2(cos, -sin, sin, cos)` 乘向量。文章还强调了 `vec2 * mat2` 和 `mat2 * vec2` 的差别（顺时针 vs 逆时针），提醒「矩阵的行列顺序决定了旋转方向」。3D 旋转被简化为**一次只转两个轴**——`P.xy *= rot1`（绕 z）、`P.xz *= rot2`（绕 y），这就是欧拉角在 shader 里最朴素的实现。

## 关键要点

- **角度单位是弧度**（0 到 2π），想用度数就先 `radians(deg)`。
- **2D 旋转矩阵的推导**：水平线段走三角函数；垂直线段分量互换；一般向量是两者叠加。
- **`mat2(cos, -sin, sin, cos)`**：GLSL 列主序，乘法顺序决定方向。
- **乘法顺序的陷阱**：`mat*vec` 和 `vec*mat` 旋转方向相反；反向旋转只要调换就行。
- **3D 旋转 = 拆成多对轴**：每次只转两个坐标分量（`.xy`、`.xz`、`.yz`），重复三次就覆盖所有自由度——即 Euler angles 的 shader 实现。
- 四元数留到后续教程（实际文章里是 Mini: 3D Rotation 作为续集）。

## 链接到的概念

- [[3d-rotation-math]] — patch：补充 2D 推导来源
- [[coordinate-spaces]]
- [[shader-vector-math-primer]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-rotation-1364623
- 本地：`raw/articles/mini.gmshaders.com/2022-09-24_mini-rotation.md`
