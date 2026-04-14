---
tags: [source, 渲染, metal, 数学, 线性代数, 教程]
date: 2026-04-14
sources: 1
---

# Linear Algebra for Graphics Programming（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 9 月发表的 *Metal by Example* 支线文章，把 3D 图形数学（向量、矩阵、变换、投影）按"Metal 教程里到底会用到什么"的最小集合过一遍。Warren 自称"living document"，不追求严谨推导，只给出**记号约定**和**几何直觉**——目标是让 Part 3 之后需要用 MVP 矩阵的读者有一份"我们以后写 `simd::float4x4` 时意思是什么"的参考。

## 摘要

文章从 Cartesian 平面扩展到 3D 空间开始，迅速带过 handedness 的选择（Warren 在右手系工作，但 Metal 的 clip space 是左手系，中间要做一次翻转）。线性变换部分只给出 identity/scale/rotation 三种 3×3 矩阵，rotation 展开到 Z 轴公式和绕任意单位轴的 Rodrigues 公式。Affine 一节解释"平移不是线性变换，必须靠 4D 齐次坐标里的 shear 来模拟"——这是所有图形程序员都会踩一次的概念点。投影一节给出 Metal 的 `[−1, 1] × [−1, 1] × [0, 1]` clip space 与之匹配的投影矩阵——文章原版抄了 OpenGL 的矩阵（Z 到 `[−1, 1]`），读者 Alex K. 在评论里指出这个 bug，Warren 后来把矩阵改成 Metal NDC 的 `[0, 1]` Z 版本。最后"Conventions"一节讲 Apple 的 `simd` 库——与 Metal 完全一致的 SIMD 类型和操作，和 **column-major 存储**——并提醒读者 `matrix.columns[col][row]` 的访问顺序容易出错。

## 关键要点

- **齐次坐标的由来**：平移在 3D 里不是线性变换（因为不满足 `T(0) = 0`），但把它塞进 4×4 矩阵右上角就变成了 4D 里的 shear——这是为什么图形管线统一用 4×4 而不是 3×3。
- **组合顺序**：`T·R·S` 作用在 column vector 上是**自右向左**执行：先 scale，再 rotate，再 translate。用 row vector 约定的引擎（DirectX 历史上）顺序相反，切换时要记得。
- **OpenGL vs Metal clip-space 的 Z**：OpenGL 是 `[−1, 1]`，Metal 是 `[0, 1]`——抄错一张投影矩阵就会把近/远平面外的东西也当作可见。评论区的 bug 修复链接值得读。
- **`simd` 库是 Objective-C 与 MSL 之间的共享类型层**：WWDC 2014 介绍过，用它在 CPU 侧构建矩阵然后直接 memcpy 进 MTLBuffer 给 shader 读。column-major 约定对应 shader 里的 `matrix[col][row]` 下标。
- **normal 矩阵的前置条件**：文章里没有展开，但给了"向量变换不同于点变换"这一提示，Part 3 用到的 `transpose(inverse(modelView))` 正是基于此。

## 链接到的概念

- [[mvp-transform]]
- [[shader-vector-math-primer]]
- [[coordinate-spaces]]
- [[3d-rotation-math]]
- [[metal-api-overview]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/linear-algebra/
- 本地：`raw/articles/metalbyexample.com/2014-09-14_linear-algebra-for-graphics-programming.md`
