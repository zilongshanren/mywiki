---
tags: [source, math, vectors, primer]
date: 2026-04-14
sources: 1
---

# 3D Math Primer for Game Programmers — Vector Operations（Jeremiah van Oosten）

[[jeremiah-van-oosten]] 2011 年发表在 3dgep.com 的数学入门系列第一篇，把游戏程序员日常会用到的所有向量运算从零讲一遍。

## 摘要

文章覆盖向量取反、加减、标量乘法、长度（norm）、归一化、两点距离、点乘、叉乘以及向量在另一向量上的投影分解。所有公式都配示意图与具体数值算例。点乘小节里的"两个**单位向量**点乘等于夹角余弦"是后续光照和方向判断的核心；叉乘小节强调结果与两个输入都垂直、模长等于平行四边形面积、并且**不可交换不可结合**。结尾专门提示了左手 / 右手坐标系下叉乘方向的差别，以及与 [[md5-model-format|MD5]] 这类工具链的相关性。是 Fletcher Dunn《3D Math Primer for Graphics and Game Development》的浓缩复习版。

## 关键要点

- 点乘的几何意义比代数定义重要：它是"投影长度 × 长度"或"夹角余弦 × 长度积"。
- 归一化前必须先判 0：用 `lengthSq > 0` 作守卫，避免 divide-by-zero。
- 向量减法的助记口诀：「a 到 b 的向量是 b 减 a」。
- 投影分解 `v = v∥ + v⊥`，对法线 n 是单位向量时简化为 `v∥ = n(v·n)`，是后续反射/折射公式的基础。
- 叉乘的方向取决于坐标系手性：从左手切换到右手时 z 轴翻转，视觉上从"指向屏幕里"变成"指向屏幕外"。

## 链接到的概念

- [[shader-vector-math-primer]]
- [[vector-dot-product]]
- [[3d-rotation-math]]
- [[coordinate-spaces]]

## 原文

- 链接：https://www.3dgep.com/3d-math-primer-for-game-programmers-vector-operations/
- 本地：`raw/articles/3dgep.com/2011-02-04_3d-math-primer-for-game-programmers-vector-operations.md`
