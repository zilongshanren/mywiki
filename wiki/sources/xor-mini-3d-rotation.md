---
tags: [source, 渲染, 数学, shader]
date: 2026-04-14
sources: 1
---

# Mini: 3D Rotation（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2025 年 10 月的一篇，对 3D 旋转的几种数学形式——**Euler Angles**、**Axis-Angle**——做入门讲解，四元数留作下一篇。是 2D 旋转教程的延伸。

## 摘要

3D 旋转本质上仍是「绕某个平面转」。最直接的做法是把它拆成三次 2D 旋转（绕 X/Y/Z），即 Euler Angles：`vector.yz = rotate2D(roll) * vector.yz` 等。顺序敏感，会在 90° 姿态遇到 gimbal lock，插值也不自然。更一般的情形需要绕任意单位轴旋转，Axis-Angle 给出简洁公式：

```glsl
vec = mix(dot(vec, axis)*axis, vec, cos(ang)) + sin(ang) * cross(vec, axis);
```

这其实是 Rodrigues 公式的向量形式。Xor 一步步拆解每一项的几何意义：`dot*axis` 是旋转中心，`mix(..., cos)` 是 2D 旋转的 `cos*x` 分量，`sin*cross` 是 `sin*y` 分量。条件是 axis 必须是单位向量，ang 是弧度。比三次 2D 旋转少做几次运算，绕任意轴干净，也没有 gimbal lock——但姿态间插值仍要上四元数。

## 关键要点

- **旋转总是一个平面上的事**。2D 里只有一个平面，3D 才冒出多种表达方式。
- **Euler Angles**：三次 2D 旋转堆叠；顺序敏感；gimbal lock；适合 yaw + pitch 摄像机等朴素场景。
- **Axis-Angle**：Rodrigues 公式的 GLSL 形式，绕任意单位轴单步旋转；便宜、干净，但不解决姿态插值。
- **四元数**：文章明确说要单独写一篇，没有展开。
- **实用策略**：内部用四元数存储/插值，需要变换向量时转回矩阵或轴角。
- 来源：Fabrice Neyret 的 Shadertoy code-golfing 笔记。

## 链接到的概念

- [[3d-rotation-math]]
- [[mvp-transform]]
- [[coordinate-spaces]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/3d-rotation
- 本地：`raw/articles/mini.gmshaders.com/2025-10-19_mini-3d-rotation.md`
