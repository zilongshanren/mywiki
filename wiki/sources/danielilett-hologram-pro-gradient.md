---
tags: [source, unity, urp, hdrp, shader, hologram, gradient, unscaled-time]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Gradient（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的渐变变体参数手册，对应 Godot 版的 Gradient 子 shader。

## 摘要

Gradient 变体在 *Gradient Space*（Object / World / Screen 三选一）的 Y 轴上，于 *Gradient MinMax Y* 两阈值之间把 *Base Color* 线性插值到 *Base Color 2*，以此把全息体染成双色上下渐变；Fresnel 也随之暴露第二颜色 *Fresnel Color 2*，使 rim 亦上下异色。该变体同时保留完整的 Vertex / Segment 两类 glitch，以及 Fresnel 深度相交。关键工程细节是 *Use Unscaled Time*——Unity（与 Godot 类似）不向 shader 内置 unscaled time，必须由脚本每帧推送 uniform；启用后，即便 `Time.timeScale=0`（例如 UI 暂停菜单），shader 动画仍按真实时间节奏走。这对把全息放进 UI 或 pause 场景的用例很关键。参数语义与 Godot 版对齐，本页仅作产品文档归档。

## 关键要点

- *Gradient Space* 三态切换是产品化"同一种渐变算法、不同贴合语义"的样板：Object 跟模型、World 跟场景、Screen 跟相机
- *Gradient MinMax Y* 两阈值外区域被**钳位**到 Base Color / Base Color 2，而非循环——与一般 ramp 贴图的 wrap 行为相反
- *Use Unscaled Time* 暴露了一个通用引擎约束：shader 无法自己感知 timeScale，这个 uniform 必须由脚本写入
- Fresnel Color 2 让边缘光也上下异色，避免 rim 与面部色调脱节

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/gradient/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-gradient.md`
