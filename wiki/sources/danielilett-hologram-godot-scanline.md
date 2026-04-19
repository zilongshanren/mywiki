---
tags: [source, godot, shader, hologram, scanline, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Scanline（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版变体之一，主视觉模式是**水平扫描线**在物体表面滚动。

## 摘要

Scanline 变体把扫描线做成一条"滚动的 alpha 蒙版"——不是叠加一层装饰颜色，而是用一张扫描线贴图调制输出 alpha，让全息物体本体在扫描线位置变亮、其他位置变暗甚至被裁切，从而表现 CRT / 全息投影常见的"条纹化亮度"。*Scanline Mode* 是设计亮点：可在**屏幕空间**（扫描线黏在屏幕，相机旋转时线条与眼睛对齐）与**世界空间**（扫描线沿世界某方向，相机绕物体转时线条随物体一起走）之间切换，两种模式分别对应"电视屏"与"物理全息投影"的心智模型。*Scanline Texture* 可替换为任意重复纹理，*Scanline Velocity* 控制滚动速度，*Scanline MinMax Alpha* 用来把纹理的 0/1 映射到可调的 alpha 区间——是常见的"把贴图当 LUT"写法（参照 [[color-lut]]）。

## 关键要点

- 扫描线通过 **alpha 调制** 实现，而非叠色。
- **屏幕空间 vs 世界空间**模式切换覆盖两种典型语义。
- *Scanline Texture* 实际上是可替换的 1D 样条，可以换成任意密度、任意形状的条纹。
- 与 [[cyan-retro-crt-shader|CRT 后处理]] 的区别：这里是**材质级**而非**后处理级**扫描线。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[godot-visual-shaders]]
- [[crt-shader-effects]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/scanline/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-scanline.md`
