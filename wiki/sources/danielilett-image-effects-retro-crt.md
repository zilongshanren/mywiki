---
tags: [source, rendering, shader, unity, retro, crt, post-processing, color-quantization]
date: 2026-04-14
sources: 1
---

# Image Effects Part 5 — Retro Arcade（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 5 篇，通过三只 shader 复刻 Super Mario Odyssey Snapshot Mode 的 NES / SNES / Game Boy 滤镜，并且在 SNES 之后额外实现了一个手写的 [[crt-shader-effects|CRT 扫描线效果]]——同时涉及 [[color-quantization-retro|复古色彩量化]]与像素化下采样这两组核心技术。

## 摘要

文章先分别讨论三种老机器的色彩限制：NES 的 64 色 YIQ 调色板、SNES 的 15-bit 加减混合色、Game Boy 的 4 级绿/灰。作者主动放弃精确还原调色板，改为在 RGB 空间**按通道量化**：NES 每通道 4 级（共 64 色），SNES 每通道 6 级（216 色），Game Boy 则先算亮度再量化为 4 级后用一组 `_GBDarkest/Dark/Light/Lightest` 颜色 property 通过**级联 `lerp + saturate`** 切换选色——这是 GPU 里"多路选择避免 if"的典型习语。核心公式是 `int r = (tex.r - EPSILON) * N` 再除以 `N-1`，`EPSILON` 防止 `1.0 * N` 被截断到 `N` 越界。像素化部分用 `RenderTexture.GetTemporary(w/p, h/p, ...)` + `Graphics.Blit(src, temp)` 先下采样再跑 shader，上采样回屏幕之前**必须**把临时 RT 的 `filterMode` 改成 `FilterMode.Point`，否则 bilinear 会把像素边缘糊成渐变。CRT 部分示范了一个简化的子像素/扫描线合成：顶点着色器用 `ComputeScreenPos` 拿到屏幕坐标并通过 `TEXCOORD1` semantic 传到片元，然后用 `sp.x % 3` / `sp.y % 3` 索引到两个 `float3x3` 矩阵里——一个 `colorMap` 存 "红/绿/蓝列"配色，一个 `scanlineMap` 存"两白一黑"的扫描行——相乘得到子像素格子。为了补偿扫描线带来的整体变暗，引入 `_Brightness` / `_Contrast` 两个参数做线性提亮和非线性对比度拉升。作者最后推荐的叠加顺序是 **PixelNES/SNES → CRT → Bloom** 依次挂相机组件。

## 关键要点

- **颜色量化**用整数截断技巧：`int c = (tex.c - EPSILON) * N` 然后 `/ (N-1)`；每通道级数 N 决定"多像哪一代机器"。
- NES 的真实限制在 YIQ + 查表，shader 里用 RGB 每通道 4 级做近似，够用不精确。
- Game Boy 用亮度 `dot(tex, (0.3, 0.59, 0.11))` 先降维到灰度再量化，4 个颜色用 `lerp+saturate` 级联选。
- **像素化 = 下采样 + 跑 shader + 上采样**，上采样之前 **`filterMode = FilterMode.Point`** 是必须的。
- CRT 子像素模拟通过"矩阵行作为 palette"的技巧：`colorMap[x%3]` + `scanlineMap[y%3]` 相乘，完全不需要 branch。
- `ComputeScreenPos(clipPos)` 配合 `TEXCOORD1` semantic 把屏幕坐标从 vert 传到 frag——`TEXCOORD` 比 `COLOR` 精度高，适合存非颜色的额外数据。
- `_ScreenParams.xy` 是相机目标的像素尺寸；`screenPos * _ScreenParams.xy` 得到屏幕整像素坐标。
- 扫描线会把画面整体压暗，必须额外加 brightness / contrast 补偿——这是所有 CRT 后处理的通病。

## 链接到的概念

- [[color-quantization-retro]]
- [[crt-shader-effects]]
- [[retro-rendering-techniques]]
- [[unity-image-effect-basics]]
- [[image-effect-colour-transform]]
- [[sampler-filter-wrap-modes]]

## 原文

- 链接：https://danielilett.com/2019-05-15-tut1-5-smo-retro/
- 本地：`raw/articles/danielilett.com/2019-05-15_image-effects-part-5-retro-arcade.md`
