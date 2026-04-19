---
tags: [source, unity, urp, hdrp, shader, hologram, noise, film-grain]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Noise（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的 Noise 变体参数手册，对应 Godot 版的 Noise 子 shader。

## 摘要

Noise 变体在 Emission 上叠加一层时变随机噪声，模拟胶片颗粒与老式全息投影的不稳定感，让全息体"不那么完美"。核心噪声接口是经典的"时间 × 空间 × 强度 × 色彩"四件套：*Noise Speed* 控制每一帧噪声值刷新的速度，*Noise Scale* 控制单粒噪声在世界/屏幕空间中的尺寸，*Noise Strength* 控制叠加权重，*Noise Color* 给整层噪声上一个 tint。Noise 子模块也附带独立的 *Use Unscaled Time* 开关，原因与 Gradient/Uber 变体相同——Unity 不向 shader 内置 unscaled time，必须由脚本每帧推送 uniform，这样即使 `Time.timeScale=0`（暂停菜单、子弹时间）全息颗粒仍按真实节奏闪烁。其余段落（Basic PBR、Vertex / Segment Glitches、Fresnel）与 [[godot-hologram-shader-effects]] 共享底座完全对齐。参数语义已在 Godot 版整合页里说清，本页仅作 Pro 版产品文档归档。

## 关键要点

- Noise 接口 = Speed + Scale + Strength + Color，是把"随机纹样"产品化的通用四件套
- 噪声直接作用在 Emission 而非 Albedo——与全息"亮度几乎全来自自发光"的前提一致
- *Use Unscaled Time* 的必要性反复出现，是 Unity/Godot shader 对 timeScale 无感知这一引擎级约束的副产物

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[classic-shader-noise]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/noise/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-noise.md`
