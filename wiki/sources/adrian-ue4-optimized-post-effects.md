---
tags: [source, 渲染, unreal, 移动端, 性能优化, 后处理, 2018]
date: 2026-04-19
sources: 1
---

# UE4 Optimized Post-Effects（Adrian Courrèges / 2018）

[[adrian-courreges]] 2018 年 12 月的文章，面向 Tegra X1（Nintendo Switch / NVIDIA Shield）上跑 Unreal Engine 4 的项目——公开了他工作中三组 drop-in 优化补丁，并附上 4.18 到 4.22 各版本的 patch 文件，双 license（CC0 / MIT），已有《Dragon Quest XI S》《Pikmin 4》等 Switch 游戏出货采用。

## 摘要

三组补丁、各自独立可裁：

1. **GatherDOF**（BokehDOF 替代）——BokehDOF 在 1080p 上要撒约 2 百万 quad 做 bokeh 精灵，overdraw 爆带宽。GatherDOF 改用 gather 方式：每输出像素采 N 个邻居按 bokeh 形状做 weighted average，再加一次 McIntosh max-filter flood-fill 降噪。形状支持 n 边形（Shirley 方形→圆盘映射 + 圆盘→多边形半径缩放）。大半径场景比 BokehDOF 快到 **10×**。CoC 计算完全沿用 BokehDOF 的逻辑，艺术家参数无感迁移。见 [[gather-bokeh-dof]]。
2. **半分辨率 SSAO**——UE4 原生 SSAO 在大半径 + 720p 上能跑到 4~6 ms（Tegra X1@768 MHz）。补丁在半分辨率跑 SSAO + 加一个 depth-aware Gaussian blur 降噪，大半径下 **~2× 加速**，且没有 TAA 时观感反而更好。代价：用了 TAA 的项目反而不如原生版。
3. **反应式 dynamic resolution**（UE4.18 前）——UE4.19 才引入官方 dynamic resolution + 时域上采，4.18 及更早完全没有。补丁基于 `GGPUFrameTime` 的上一帧 GPU 时长，在 min / max 两档 screen percentage 之间跳，配合 `r.SceneRenderTargetResizeMethod 2` 避免重新分配 RT 抖动。反应式、不能预判、和 TAA/motion-blur/SSR 切分辨率时有 glitch。见 [[ue4-reactive-dynamic-resolution]]。

文末更新披露《Dragon Quest XI S》的 Switch 版用了 **dynamic resolution + half-res SSAO**（Unreal-Fest Japan 2019 的 slides 在 Famitsu 有），以及《Pikmin 4》用了改版 GatherDOF（miniature tilt-shift 是其视觉 signature）。

## 关键要点

- **目标硬件**：Tegra X1（Switch / Shield），移动级 GPU 带宽受限。
- **GatherDOF**：gather + flood-fill，多边形 bokeh 通过 `r = cos(π/n)/cos((θ mod 2π/n)−π/n)` 极坐标半径缩放实现；技术来自 DOOM 2016 和更早的 CryEngine 3。
- **Half-res SSAO**：纯 resolution trick + depth-aware blur；和 compute 版本 (`r.AmbientOcclusion.Compute`) 不兼容，走像素 shader 路径。
- **Reactive dynamic res**：只在 min/max 两档间跳；`r.SceneRenderTargetResizeMethod 2` 关键 flag。
- **ShipProof**：DQ XI S / Pikmin 4 等 AAA Switch 版实际出货采用。
- **License**：CC0 + MIT 双 license，明确"公司内也能直接用"。

## 链接到的概念

- [[gather-bokeh-dof]]
- [[ue4-reactive-dynamic-resolution]]
- [[scatter-bokeh-dof]] — GatherDOF 替代的那个 scatter 路线
- [[dynamic-resolution-scaling]] — 通用思路
- [[thin-lens-model]]
- [[adrian-courreges]]
- [[unreal-frame-breakdown]]

## 原文

- 链接：<http://www.adriancourreges.com/blog/2018/12/02/ue4-optimized-post-effects/>
- 本地：`raw/articles/adriancourreges.com/2018-12-02_ue4-optimized-post-effects-adrian-courreges.md`
