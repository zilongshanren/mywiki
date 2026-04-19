---
tags: [source, 渲染, unity, urp, 后处理, color-quantization, retro]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - SNES（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 SNES 色阶量化后处理的两个参数。

## 摘要

SNES 是一个 per-channel 的 [[color-quantization-retro|色阶量化]]后处理：把 RGB 每通道的连续值截断到 `N` 级，产生 `N³` 色的离散调色板。参数极简：`Enabled`（开关）、`Banding Levels`（每通道级数）。`N=6` 给出 216 色，近似真实 SNES 的观感；`N=4` 降到 64 色，约等于 NES。数学一行：`int(c * N) / (N-1)`，和 Daniel 在 *Image Effects Part 5* 里的教程实现**完全一致**，只是 Pro 版把它做成了 Volume override。相比那张教程页还额外支持 NES/SNES/Game Boy 三种风格，Pro 版只暴露 "通用每通道级数" 一个旋钮，想做 Game Boy 风（luminance 量化 + 4 色 palette）需要另外的 override 或自写 shader。

## 关键要点

- 数学：`quantized = floor((c - ε) * N) / (N-1)`——无 `if`、fragment shader 一行
- `Banding Levels = 6` 近似 SNES、`= 4` 近似 NES
- 远少于真机调色板的**色带感**正是风格
- 不处理亮度空间——纯 RGB 截断，想做 Game Boy 那种灰阶 4 级需额外 override
- 像素化下采样不包含在 SNES override 里——要靠 camera 或独立节点配合 `FilterMode.Point`
- 搭 [[crt-shader-effects|CRT]] / [[bloom-threshold-blur-composite|Bloom]] / [[dither-alpha-clipping|dither]] 是复古管线的典型链

## 链接到的概念

- [[color-quantization-retro]]
- [[color-banding]]
- [[crt-shader-effects]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/snes/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-snes.md`
