---
tags: [source, 渲染, shader, 噪声, gyroid]
date: 2026-04-19
sources: 1
---

# Dot Noise（Xor）

[[xor-shader-artist|Xor]] 2025 年 9 月的 tutorial，提出一种比 3D Simplex/Perlin 便宜一个数量级的 aperiodic 3D 噪声——`dot_noise`，适合每像素采样次数极高的 [[density-field-volumetric|体积渲染]] 场景。

## 摘要

从 gyroid `dot(cos(p), sin(p.yzx))` 起步——周期 τ 完美重复。把其中一条频率换成无理数 $\phi$ 打破周期：`dot(cos(p), sin(PHI*p))`——但两层波仍共用同一组轴线，结构化瑕疵明显。解法：给两层用**不同的旋转**，选"最无理"的选择——黄金角绕 `(1, phi, phi²)` 轴。得到常量 3×3 矩阵 `GOLD`，最终函数 `dot_noise(p) = dot(cos(GOLD*p), sin(PHI*p*GOLD))`，范围 [-3, +3]，大约 5–7 条 ALU 指令。代价：大尺度下仍能看到 underlying 正弦结构；但**分层做 fractal** 就能掩盖。推荐用于云、湍流、fluid，不推荐用于需要 isotropic 外观的地形高度场——那些仍应用 Simplex/Perlin。无 hash / 无插值 / 无梯度，是最"傻"且最快的方案。

## 关键要点

- Gyroid `dot(cos(p), sin(p.yzx))` 是起点——周期 τ 明显。
- **加 $\phi$ 频率** → aperiodic，但轴线仍相同、结构化明显。
- **加黄金角旋转矩阵** → 两层最大去相关，视觉瑕疵显著降低。
- 5–7 条 ALU、无 hash / 插值 / 梯度。
- 适合高采样率场景（volumetric），不适合低采样、大尺度平面。

## 链接到的概念

- [[dot-gyroid-noise]]
- [[classic-shader-noise]]
- [[layered-grid-noise]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/dot-noise
- 本地：`raw/articles/mini.gmshaders.com/2025-09-05_dot-noise.md`
