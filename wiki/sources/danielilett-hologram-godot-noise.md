---
tags: [source, godot, shader, hologram, noise, stylized]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Godot — Noise（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Hologram Shaders* Godot 版变体之一，主视觉模式是**胶片颗粒噪点**覆盖。

## 摘要

Noise 变体在共享的 PBR / 顶点 glitch / 切片 glitch / fresnel 骨架上叠加一层时变随机噪声，用来模拟胶片颗粒或全息投影的细粒度扰动，让画面从"过于完美的 CGI 全息"变成"略带信号噪点的可信全息"。噪声子系统由四个参数驱动：*Noise Speed* 决定噪点变化速率（即时间维度采样步长），*Noise Scale* 决定每颗噪点的空间尺寸，*Noise Strength* 决定噪点对最终颜色的影响权重，*Noise Color* 给噪声整体染色。概念上与 [[classic-shader-noise]] 的高频扰动思路一致，但这里直接作用于 Emission 颜色而非顶点位移。

## 关键要点

- 噪声作为独立装饰层，与 glitch、fresnel 解耦。
- *Noise Color* 独立染色，便于与 *Base Color* 风格化搭配。
- 四参数套路等价于"空间尺度 + 时间尺度 + 强度 + 色彩"的通用噪声接口。

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[godot-visual-shaders]]
- [[classic-shader-noise]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-godot/noise/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-godot-noise.md`
