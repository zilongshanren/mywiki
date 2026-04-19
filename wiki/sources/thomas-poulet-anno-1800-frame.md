---
tags: [source, 渲染, frame-analysis, anno-1800, terrain, 粒子, 2025]
date: 2026-04-19
sources: 1
---

# Anno 1800: Frame Analysis（Thomas Poulet / 2025）

[[thomas-poulet]] 2025 年 8 月写的帧分析。Anno 1800 用 Ubisoft Mainz 的自研 Anno 系列引擎——以城建 top-down 视角、多岛海域、高密度资产和长视距为约束。文章借一帧从 **地形 VT → 天空 cubemap → depth prepass → shadow → color → particles → post → UI → async FFT ocean / SSAO** 走一圈，是目前公开资料里最完整的 Anno 引擎解剖。

## 摘要

Anno 管线**前向渲染 + 4× MSAA、R16G16B16A16_FLOAT HDR**，不走 deferred。开帧先更新**地形 node-texture array（763 × 512²，BC7 压缩 + mip 自生成）** —— 这是它的 virtual-texture 变体，每 tile 用 bitfield material map 挑层 + 贴 decal + 烘焙压缩，详见 [[terrain-virtual-node-texture]]。接着渲 64³ 的**动态 sky cubemap** 给 IBL。shadow 用两摄像机包 vertical 的 atlas、compute cull + ExecuteIndirect，但非 bindless 导致每个 mesh 实例一次 ExecuteIndirect（engine 侧看到优化空间）。color pass 走 forward+（cluster + LightIndex texture + 2048 point / 4096 元素 spot buffer）。**粒子系统极精简**：quad + 4 张「时间×粒子」动画纹理 + 1 个 instanced drawcall，vertex shader 做 350 条指令的查表动画，详见 [[texture-driven-gpu-particles]]。post 只有 7 个 draw（bloom + separable blur + MSAA resolve + tone map + LUT grading）。UI 用共享的 **Phoenix**（R6 Siege 也用），500 个 `DrawIndexedInstanced` 每个 instance count 1，核心技巧是**九宫格 mesh + 单通道 SDF 字体**。async compute 上跑 **FFT 海洋 + 岸边模拟 + SSAO**。全文还嵌了一篇迷你 DXBC IR 导读讲 mip generator。

## 关键要点

- **Forward + 4× MSAA HDR**：和多数 deferred AAA 走不同路径。
- **Terrain node-texture**：[[terrain-virtual-node-texture]]；不是 quadtree VT，是 763 slice 的 array + runtime BC7 bake。
- **8K tint + 8K grit 大图**做低频覆盖 + 海岸破碎。
- **Sky cubemap**：64³ 动态生成（shadertoy 有 Poulet 的复现）。
- **Depth prepass**：depth + normal + stencil (material ID)。
- **Shadow atlas**：两相机包在一张 atlas 里上下排（不同倾角权衡远近阴影可读性）。
- **Forward+ light**：cluster buffer + indirection texture + 2048 point + ≤1365 spot。
- **Particles**：quad + 4 动画纹理 + per-type / per-instance / per-draw config buffer；[[texture-driven-gpu-particles]]。
- **Post 只 7 draw**：bloom + sep blur + resolve + tone map + LUT grading。
- **Phoenix UI**：9-slice mesh + 单通道 SDF 字体；[[nine-slice-ui]]。
- **Async compute**：FFT ocean（大/小波 + 梯度 map）+ 岸边 local sim + SSAO（1/4 → full + 两 pass 模糊）。
- **未优化点**：indirect draw 非 bindless，一个 ExecuteIndirect 一个 mesh；bindless + descriptor indexing 能大幅压缩。

## 链接到的概念

- [[thomas-poulet]]
- [[terrain-virtual-node-texture]]
- [[texture-driven-gpu-particles]]
- [[nine-slice-ui]]
- [[simonschreibt-anno-1800-shadows]] — 同一游戏的 shadow tricks
- [[tiled-light-prepass]] / [[deferred-rendering]]
- [[msaa-ssaa]]
- [[bindless-rendering]] / [[multidraw-indirect-occlusion-culling]]
- [[bloom-threshold-blur-composite]] / [[local-tonemapping]]
- [[slug-gpu-glyph-rendering]] / [[sdf-number-atlas-text]]
- [[mipmap-generation-sampling]]
- [[async-compute]]

## 原文

- 链接：<https://blog.thomaspoulet.fr/posts/anno-1800-frame-analysis/>
- 本地：`raw/articles/blog.thomaspoulet.fr/2025-08-16_anno-1800-frame-analysis-thomas-poulet.md`
