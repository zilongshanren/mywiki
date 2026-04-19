---
tags: [source, godot, shader, hologram, grid, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Grid（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版四种变体之一，主视觉是**世界空间三轴网格线**。

## 摘要

Grid 变体在 PBR / glitch / fresnel 骨架之上叠加一层"科幻投影网格"：沿世界空间三轴各自有一组 *Grid Axis Strength*（值为 0 即关闭该轴），*Grid Density* 控制疏密、*Line Thickness* 控制线宽（世界空间单位）、*Line Falloff* 控制网格线边缘从实到虚的过渡；*Grid Offset* 静态位移、*Grid Velocity* 使网格沿三轴匀速滚动，常用于"扫描中的全息投影"表现。还可以围绕 *Rotation Axis* 指定的轴做 *Rotation Amount* 度角度的整体旋转，便于错开与物体主轴的共线位置（否则会出现摩尔纹式伪影）。

## 关键要点

- 与 Dot Matrix 的对比：Grid 是**世界空间**，相机靠近时线会变粗；Dot Matrix 是**屏幕空间**，点的尺寸恒定。
- 滚动网格 + 切片 glitch 的组合非常契合"远方投影"的美术预期。
- 三轴独立开关允许只在地面或墙面方向留线。

## 链接到的概念

- [[godot-hologram-shader-effects]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/grid/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-grid.md`
