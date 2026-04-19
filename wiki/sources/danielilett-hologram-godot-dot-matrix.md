---
tags: [source, godot, shader, hologram, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Dot Matrix（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版四种变体之一，主视觉模式是**屏幕空间点阵**覆盖。

## 摘要

Dot Matrix 变体在共享的 PBR / 顶点 glitch / 切片 glitch 基础上，把最终像素按屏幕空间切成可配置的栅格：*Dot Size* 控制每个点的像素尺寸，*Dot Space* 控制点与点之间的空隙，*Rotation Radians* 旋转整个栅格。与 Grid 变体的"世界空间线框"不同，Dot Matrix 始终在屏幕空间运算，因此相机移动时点阵大小保持不变，风格更接近 LED 矩阵显示或老式单色点阵屏。

## 关键要点

- 点阵是**屏幕空间**而非世界空间。
- 共享 Vertex Glitch / Segment Glitch 子模块（详见概念页）。
- *Output Mode* 允许只输出到 Emission，使全息有 HDR 发光效果。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[godot-visual-shaders]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/dot-matrix/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-dot-matrix.md`
