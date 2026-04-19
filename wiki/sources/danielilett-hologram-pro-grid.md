---
tags: [source, unity, urp, hdrp, shader, hologram, grid]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Grid（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的网格变体参数手册，对应 Godot 版的 Grid 子 shader。

## 摘要

Grid 变体在**世界空间**沿三轴生成规则网格线，*Per Axis Strength* 逐轴单独开关（某轴置 0 即关），*Grid Density* 控疏密、*Line Thickness* 控线宽、*Line Falloff* 控边缘软硬。整套网格可围绕 *Rotation Axis* 旋转 *Rotation Radians* 弧度，并沿 *Grid Offset* 平移、以 *Grid Velocity* 速度滚动。配合标准 PBR 底座与 Fresnel 子模块（含 *Use Scene Intersections* 深度相交辉光）构成一个典型"科幻网格投影"外观。Pro 版的基础 Grid **不含** glitch 子系统——如果同时想要故障感，应使用独立的 Grid + Glitch 变体（见 [[sources/danielilett-hologram-pro-grid-glitch]]）。这种"把 glitch 做成独立 shader，而不是每个 shader 都带一个开关"的取舍，与 Uber 变体的思路对立，是 [[shader-combination-strategies|uber vs variant]] 决策的一个实际案例。参数语义与 Godot 版对齐，本页仅作产品文档归档。

## 关键要点

- **世界空间**网格与 [[sources/danielilett-hologram-pro-dot-matrix|Dot Matrix 的屏幕空间点阵]]在"装饰贴合谁"上完全对立
- *Grid Velocity* 直接把运动烘进 shader，美术无需写脚本就能让网格"流"起来
- *Line Falloff* 是把硬边网格变成柔边的单一参数——实际是在条件 step 上加 smoothstep 宽度
- 不内置 glitch 是刻意的：保持纯 Grid 变体的编译体积与参数面板最小

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[shader-combination-strategies]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/grid/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-grid.md`
