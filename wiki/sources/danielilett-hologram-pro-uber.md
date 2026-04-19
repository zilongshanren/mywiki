---
tags: [source, unity, urp, hdrp, shader, hologram, uber, combination]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Uber（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的 Uber 变体参数手册，对应 Godot 版的 Uber 子 shader。

## 摘要

Uber 变体把 Scanline + Vertex / Segment Glitches + Noise + Fresnel 四类子系统合进同一份 shader，每个段落独立布尔开关（*Scanline Mode=None*、*Use Vertex Glitches=false* 等）；作者同时保留独立的单功能 shader 作为"更便宜、更专注"的降级选项，这是典型的 [[shader-combination-strategies|uber shader vs 多变体]] 产品化取舍——一份 uber 好管理、好组合、美术可实时切换，但未开启段落的 uniform 采样与分支仍会占 GPU 成本；拆成独立 shader 变体最轻量，但运行时无法互相切换，必须换材质。Uber 同样引入 *Use Unscaled Time*，由脚本推送 unscaled time uniform，保证 `Time.timeScale=0` 下 UI 全息继续动。其余段落与 Godot 版 Uber 完全对齐，本页仅作产品文档归档。

## 关键要点

- Uber 合并 Scanline / Glitch / Noise / Fresnel 四子系统，每子系统独立开关
- 产品同时提供独立单功能 shader，给成本敏感场景一个"少买点"的选项——这是 uber vs variant 的标准取舍姿态
- *Use Unscaled Time* 再次出现，再次是"shader 无法感知 timeScale"这一引擎约束的产物

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[shader-combination-strategies]]
- [[classic-shader-noise]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/uber/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-uber.md`
