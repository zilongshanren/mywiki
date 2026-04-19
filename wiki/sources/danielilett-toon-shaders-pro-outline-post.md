---
tags: [source, shader, outline, post-process, urp, unity]
date: 2026-04-19
sources: 1
---

# Toon Shaders Pro for URP — Outline (Post Process)（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 的 *Toon Shaders Pro for URP* 里的**描边后处理**——不是单一算法，而是**六种描边路径**并列暴露给用户选择。这是目前 wiki 里见过最完整的 toon outline 策略目录。

## 摘要

面板顶层的 **Outline Type** 是一个六选一枚举：*No Outlines*（占位）/ *Depth Normal Outlines*（屏幕空间 Sobel-like 检测 depth + normals + color 梯度）/ *High Quality Masked Object Outlines*（单独渲染物体到 mask 纹理上，支持可变厚度）/ *Pixel Width Masked Object Outlines*（mask 版但 1 像素硬描边，最便宜）/ *Hull Outlines*（inverted hull，再画一遍放大的 mesh）/ *Debug Outline Mask*（把 mask 可视化）。每种算法有一组独立参数，其他隐藏。Render Pass Event 可选在 URP 内置 post（color grading / bloom）前或后；前者会让描边被 bloom 模糊成柔和风格，后者保留纯色。Light Modes 字段决定哪些 shader 被画进 mask——`UniversalForwardOnly`（包中的 Toon shader 用这个 tag）、`UniversalForward`（URP Lit）、`SRPDefaultUnlit`（unlit，没显式 tag 时默认）、`UniversalGBuffer`（deferred）。

## 关键要点

- **六种算法一站式**：屏幕空间 depth-normals edge 检测 / 物体 mask 两档（高质量 + 1 像素）/ inverted hull / debug / 关闭。
- **Depth Normal Outlines**：Color/Depth/Normal 三路梯度独立敏感度 + 强度 + Depth Threshold（剔除远处被误判）。与 [[sources/danielilett-snapshot2-outline]] 是同一思路，参数更细。
- **Masked Object Outlines** 优势：支持 *Masked Outline Thickness*、*Fade Start/End* 距离衰减、*Outline Draw Sides*（内/外/两侧）、*Mask Drawing Mode*（mesh 外缘 / 每三角 / 集体区域 / 按顶点色分区）、*Mask Ignore Depth*（透墙描边）。
- **Hull Outlines** 参数：*Outline Thickness*（沿法线外推距离）、*Outline Transparency*（透明度排序影响）、*Outline Lighting*（给 outline 本身加 diffuse 阴影，反向则让 outline 变暗的一侧朝光源——卡通颜色分区效果）、*Outline Min Lighting*。
- **Light Modes 清单**：`UniversalForwardOnly` / `UniversalForward` / `SRPDefaultUnlit` / `UniversalGBuffer` —— 渲染谁进 mask 由 shader 的 pass tag 决定，**作者自己的 Toon shader 用 `UniversalForwardOnly`**。
- **Render Pass Event 取舍**：before = 描边被 bloom 影响（柔边）；after = 硬纯色。
- **Vertex Color mask**：*VertexColorRandom* demo script 配合 *Mask Drawing Mode = vertex color* 能给每个三角形独立描边。

## 链接到的概念

- [[cel-shader-outline]]
- [[sobel-edge-detection]]
- [[depth-texture-silhouette]]
- [[stencil-buffer]]
- [[blit-render-feature]]

## 原文

- 链接：<https://danielilett.com/toon-shaders-pro/outline-post-process/>
- 本地：`raw/articles/danielilett.com/2026-01-01_toon-shaders-pro-for-urp-outline-post-process.md`
