---
tags: [source, unity, urp, hdrp, shader, hologram, dynamic-resolution]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro — Dot Matrix + Glitch（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders Pro*（Unity URP/HDRP 商业插件）的 Dot Matrix + Glitch 组合变体——等价于 Godot 版 Dot Matrix 加上 glitch 子系统。

## 摘要

相比 [[godot-hologram-shader-effects|Godot 版 Dot Matrix]]，Unity Pro 版的功能集几乎对等，但多暴露了一组 PBR 参数（*Metallic / Smoothness / AO*）以及一个真正属于 Unity 平台特有的工程块——**Dynamic Resolution**。文档解释：当启用 FSR / DLSS 动态分辨率时，Unity shader 内部拿到的有时是**升采样前**的分辨率，这会导致 dot matrix 的点阵尺寸在不同渲染路径下不一致（点会变大或变小），作者暴露 *Upscaling Amount* 手动补偿系数让美术在运行期修正。这是把 **屏幕空间特效 × 动态分辨率** 这一常见坑写进产品 API 的一个实际案例——值得登记为概念，因为 DLSS/FSR 下的"逻辑分辨率 vs 物理分辨率"混淆对任何依赖屏幕空间 UV 的后处理或材质都是现实问题。

## 关键要点

- **Dynamic resolution 的分辨率语义坑**：FSR/DLSS 下 shader 拿到的不是呈现分辨率。
- *Upscaling Amount* 是手动旁路——等价于让美术补一个系数，而不是从系统 API 读取。
- 与 [[dynamic-resolution-scaling]] 的衔接：后者讲系统级 DRS，这里讲它对屏幕空间材质的副作用。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[dynamic-resolution-scaling]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/dot-matrix-glitch/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-dot-matrix-glitch.md`
