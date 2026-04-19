---
tags: [source, unity, urp, hdrp, shader, hologram, scanline, alpha]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Scanline（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的 Scanline 变体参数手册，对应 Godot 版的 Scanline 子 shader。

## 摘要

Scanline 变体用一张扫描线贴图**调制 alpha**（而非直接叠色）——这是全息 scanline 与 [[crt-shader-effects|CRT scanline]] 的核心差别：前者让表面部分透明，后者让表面部分变暗。*Scanline Mode* 三态切换（Screen Space / World Space / None）是产品化"同一种扫描线算法、不同贴合语义"的样板：屏幕空间模式下扫描线黏屏、像老式 CRT；世界空间模式下扫描线黏物体、像真·全息投影在空间中旋转。Screen Space 下暴露 *Scanline Rotation* 旋转方向，World Space 下暴露 *Scanline Direction* 指定世界向量（仅贴图的垂直分量参与采样）。*Scanline Velocity* 控制滚动速度，*Scanline MinMax Alpha* 把贴图 0/1 亮度映射到可调 alpha 区间——本质是把贴图当作 1D LUT 使用。相对 Godot Scanline 子 shader 没有新增功能，参数对齐，本页仅作产品文档归档。

## 关键要点

- Scanline 贴图调制的是 **alpha** 而非 color——"隐去部分面积"而不是"叠暗"
- Screen vs World Space 模式对应"黏屏"与"黏物体"两种视觉语义，直接决定扫描线是否随相机平移
- *MinMax Alpha* 把贴图亮度线性重映射到 alpha 区间，是把贴图当 1D LUT 的典型用法

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[crt-shader-effects]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/scanline/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-scanline.md`
