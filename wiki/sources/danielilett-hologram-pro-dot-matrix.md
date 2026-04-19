---
tags: [source, unity, urp, hdrp, shader, hologram, dot-matrix, dynamic-resolution]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Dot Matrix（Daniel Ilett）

[[daniel-ilett]] 为 Unity URP/HDRP 产品 *Hologram Shaders Pro* 撰写的变体参数手册，对应 Godot 版的 Dot Matrix 子 shader。

## 摘要

Dot Matrix 变体在屏幕空间把全息表面切成一串规则方块，方块尺寸 *Dot Size*、间距 *Dot Space* 均以像素为单位，*Rotation Radians* 旋转整套网格，再叠加 Unity 标配的 PBR 底座（*Output Mode / Base Color / Base Texture / Normal / Alpha Clip / Metallic / Smoothness / Ambient Occlusion*）。这份 Pro 版相对 Godot 版多暴露两组东西：一是 URP/HDRP 才有的 *Metallic / Smoothness / AO*；二是专为动态分辨率（FSR/DLSS）准备的 *Upscaling Amount*——Unity 在启用动态分辨率时，shader 里有时拿到的是升采样前分辨率而非呈现分辨率，这会让点阵尺寸随帧率漂移，*Upscaling Amount* 是旁路补偿。参数语义与 Godot 版完全对齐，因此本页仅作为产品文档归档，主要设计观察沉淀在 [[godot-hologram-shader-effects]]。

## 关键要点

- Dot Matrix 是**屏幕空间**装饰层，不受物体姿态影响——这与同套产品的世界空间 Grid 恰好形成对照
- *Dot Size* 与 *Dot Space* 均以像素计量，决定为何必须补偿动态分辨率
- Pro 版引入的 *Upscaling Amount* 是所有依赖屏幕空间 UV 的材质在 [[dynamic-resolution-scaling]] 下的通用解法
- PBR 四件套（Metallic / Smoothness / AO / Normal）仅在 *Output Mode* 选择 Base Color 或 Both 时才具意义；Emission-only 模式下几乎全被发光覆盖

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[dynamic-resolution-scaling]]
- [[dither-alpha-clipping]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/dot-matrix/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-dot-matrix.md`
