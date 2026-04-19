---
tags: [source, rendering, shader, noise, fluid]
date: 2026-04-19
sources: 1
---

# Turbulence（Xor / GM Shaders Mini）

[[xor-shader-artist|Xor]] 发表于 2025-03-17 的短篇：用**叠加旋转正弦波**在单 pass fragment shader 里伪装湍流，用来做流体、火焰、烟雾、魔法等 VFX。

## 摘要

真 Navier-Stokes 模拟要多 pass、中间纹理、显存、分辨率受限，对实时背景效果通常太重。Xor 给出的近似是一个形式极简的循环：每次对坐标做一次 `pos += amp * rot[0] * sin(freq * (pos*rot).y + speed*time)`，随后把 `rot` 再旋转一次、频率按 `*1.4` 递增、振幅按 `/freq` 衰减——和 fBm 一样的「高频低幅」能量分布。8–10 次迭代就能产生视觉上可信的漩涡和流动感。火焰版本在此基础上增加纵向压缩 + 向上滚动（模拟热气上升）和高处横向拉伸（横向扩散）。本质是一种廉价的 **domain warping**，非物理但对 shader art 足够用。

## 关键要点

- 核心公式只有一行 sin，关键是旋转角别取 45° / 90°，避免对齐纹路。
- 振幅和频率反向变化（`amp/freq`）维持视觉能量守恒。
- 火焰只是把同一算法加上各向异性的缩放 + 时间驱动的上升。
- 不是 Navier-Stokes，但是以极少指令撑起大部分「看起来像流体」的需求。
- 文末推荐了 Gijs 的最小 NS、Nimitz 的 Chimera's Breath、wyatt 的 3D cloud、Harris 的 GPU fluid 经典 tutorial。

## 链接到的概念

- [[turbulence-domain-warping]]
- [[layered-grid-noise]]
- [[fractal-texturing]]
- [[classic-shader-noise]]

## 原文

- 链接：https://mini.gmshaders.com/p/turbulence
- 本地：`raw/articles/mini.gmshaders.com/2025-03-17_turbulence.md`
