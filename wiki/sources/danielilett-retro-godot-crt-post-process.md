---
tags: [source, godot, shader, crt, vhs, post-process, resolution-scale]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for Godot - CRT (Post Process)（Daniel Ilett）

[[daniel-ilett]] 为 Godot 版 *Retro Shaders Pro* 撰写的 CRT 全屏后处理变体参数手册。该 shader 以屏幕滤镜形式把现代高清 LCD/LED 面板的画面转换成 CRT 外观，并叠加 VHS 磁带做旧层。

## 摘要

与 Mesh 版同源，参数结构几乎一致：*Pixel Size* 做整数级像素化；Barrel Distortion 段落用 *Distortion Strength / Smoothing* 做桶形畸变 + 圆角黑边；RGB Subpixels & Scanlines 通过 *Subpixel Texture / Scanline Texture* 两张 mask 叠加子像素条纹与滚动扫描线；VHS Artifacts 用 *Random Wear / Aberration / Tracking Texture (RGB 编码)/ Tracking Color Damage (YIQ 色空间)* 等一整套做旧；Color Adjustments 给 *Tint / Brightness / Contrast* 全局整饬。相对 Mesh 版，Post Process 版多出两个关键参数：**Scale In Screen Space** 和 **Reference Resolution (Vertical)**——开启后所有涉及屏幕大小的参数（像素大小、RGB 子像素间距、扫描线宽度等）会相对一个"设计时的参考垂直分辨率"等比例缩放，这样在不同分辨率的显示器上"视觉密度"保持一致，不会因为换机就让扫描线突然变粗或变细。这是任何全屏后处理在跨分辨率发布时必须解决的问题，也是它相比 Mesh 版的主要差异点——Mesh 版贴在网格 UV 上，天然无此问题。

## 关键要点

- Post Process 版独有 *Scale In Screen Space* + *Reference Resolution*，把设计分辨率作为参考系，让像素/扫描线密度跨分辨率视觉一致
- CRT + VHS 组合在同一 shader 内分层：Pixelation → Barrel → Subpixel/Scanline → VHS Wear/Tracking → Color Grade，是典型的"多 trick 叠加"后处理管线
- *Tracking Color Damage* 走 YIQ 色空间只扰动色度——与 Mesh 版共用相同真实物理建模

## 链接到的概念

- [[crt-shader-effects]]
- [[color-quantization-retro]]
- [[urp-volume-post-processing]]

## 原文

- 链接：https://danielilett.com/retro-shaders-godot/crt-post-process/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-godot-crt-post-process.md`
