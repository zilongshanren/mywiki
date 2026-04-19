---
tags: [source, 渲染, unity, urp, 后处理, posterize, color-quantization]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Posterize（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Posterize 色阶量化后处理的四个参数。

## 摘要

Posterize 和同包的 [[sources/danielilett-snapshot-pro-snes|SNES]] 同属 [[color-quantization-retro|per-channel 色阶量化]]家族，但接口更通用：`Red Levels` / `Green Levels` / `Blue Levels` **三通道分别独立控制**级数，不强制等级。另外暴露一个 `Power Ramp` 在量化前对输入做 `pow(c, p)` 曲线调整，`p > 1` 偏暗、`p < 1` 偏亮——等价于一个单点 tone curve，用来控制调色板中深浅色的分布密度。和 SNES override 相比，Posterize 更像通用版：不锁 RGB 等级、额外给一个 gamma 旋钮。

## 关键要点

- 三通道独立级数——可做"绿多红少"的偏色风格（SNES override 强制等级）
- `Power Ramp` 是量化前的 gamma curve，重分配色阶在感知空间的疏密
- `Enabled` 单开关——Volume override 的标配
- 数学：`out = floor(pow(c, p) * N) / (N-1)`，和 SNES 的差别仅在 `pow` 和三参数
- 不处理像素化下采样——配合 [[pixelate-postfx|Pixelate]] 或 camera Point filter 才成完整复古链

## 链接到的概念

- [[color-quantization-retro]]
- [[color-banding]]
- [[color-lut]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/posterize/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-posterize.md`
