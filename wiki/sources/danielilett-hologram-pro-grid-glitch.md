---
tags: [source, unity, urp, hdrp, shader, hologram, grid, glitch]
date: 2026-04-19
sources: 1
---

# Hologram Shaders Pro - Grid + Glitch（Daniel Ilett）

[[daniel-ilett]] 为 Unity 版 *Hologram Shaders Pro* 撰写的"网格 + 故障"组合变体参数手册。

## 摘要

这是纯 Grid 变体的扩展版：在世界空间网格（*Per Axis Strength / Grid Density / Line Thickness / Line Falloff / Grid Offset / Grid Velocity / Rotation Axis + Radians*）基础上，额外接入完整的 Vertex Glitches 与 Segment Glitches 两个子系统，各自带 *Use …* 布尔开关可独立关闭。PBR 底座与 Fresnel 子模块（含深度相交）与 Pro 其它变体一致。该变体的存在本身传达了一条产品决策：Ilett 没有在基础 Grid 里藏一堆 glitch 开关，而是把"Grid + Glitch"拆成独立 shader，让不要 glitch 的用户拿到更小的编译体积与更干净的 Inspector；同时又为想同时要两样的用户提供组合版——这是 [[shader-combination-strategies|uber vs variant]] 策略在产品端的妥协方案，介于"一个 Uber 管全部"和"每个变体严格单功能"之间。参数与 Godot 版对齐，本页仅作产品文档归档。

## 关键要点

- 组合变体比 Uber 更窄（只挑 Grid + Glitch 一种组合），比单功能变体更宽——是"实用组合预烘焙"的中间形态
- 两个 glitch 子系统的 *Use Vertex Glitches / Use Slice Glitches* 布尔位在 GPU 上退化为条件分支，开销与零值 uniform 接近
- Per-axis Strength + Grid Density + Line Thickness + Line Falloff 构成世界空间网格的"四参数最小接口"，其它 Pro 变体与 Godot 端保持一致
- 组合变体**不含** Dot Matrix / Gradient / Noise / Scanline——要那些组合需另择 Uber

## 链接到的概念

- [[godot-hologram-shader-effects]]
- [[shader-combination-strategies]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：https://danielilett.com/hologram-shaders-pro/grid-glitch/
- 本地：`raw/articles/danielilett.com/2026-01-01_hologram-shaders-pro-grid-glitch.md`
