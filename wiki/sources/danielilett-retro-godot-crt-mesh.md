---
tags: [source, godot, shader, crt, vhs, mesh, post-process]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for Godot - CRT (Mesh)（Daniel Ilett）

[[daniel-ilett]] 为 Godot 版 *Retro Shaders Pro* 撰写的 CRT Mesh 变体参数手册。与 CRT Post Process 变体同源，只是把整套 CRT 滤镜从屏幕后处理迁移到**一张普通网格材质**上，典型用例是游戏中实时 CCTV 监视器、电视机道具或游戏内子屏幕——推荐给材质配一张高细节贴图，以便 CRT 的像素化/扫描线/VHS tracking 等装饰层有足够原始信息可"做旧"。

## 摘要

参数结构与 CRT Post Process 几乎一一对应：*Pixel Size* 做整数像素化；Barrel Distortion 段落用 *Distortion Strength / Smoothing* 把边缘向内扭成 CRT 玻璃凸面，*Background Color* 填充畸变外的黑边；RGB Subpixels & Scanlines 段落通过两张纹理 *Subpixel Texture* 与 *Scanline Texture*（均作为乘法 mask）叠加红绿蓝子像素条纹与滚动扫描线，*Scanline/RGB Size* 控制条纹大小、*Scanline Scroll Speed* 控制滚动速度；VHS Artifacts 段落最丰富——*Random Wear* 注入水平 UV 噪声、*Aberration Strength* 在边缘做色散、*Use VHS Tracking* 开关后以一张 x×1 控制贴图 *Tracking Texture*（R 通道控 UV 偏移强度、G 通道控 tracking 线可见度）配合 *Tracking Size / Strength / Speed / Jitter* 模拟老磁带抖动，*Tracking Color Damage* 把画面转到 **YIQ 色空间**后只扰动 I/Q 色度通道——这是真实 NTSC 磁带损伤的正确建模；Color Adjustments 段落给一个全局 *Tint / Brightness / Contrast*。与 Post Process 变体相比，Mesh 版**缺少** *Scale In Screen Space / Reference Resolution* 两项——因为贴在网格上时，所有参数直接以 UV 空间解读，没有"相对屏幕分辨率"的问题。

## 关键要点

- Mesh 版 = Post Process 同款 CRT 滤镜 + 普通 PBR albedo（*Base Color / Base Texture*），可贴到任意网格
- *Tracking Color Damage* 走 **YIQ 色空间**扰动 I/Q 通道——这是模拟 NTSC 磁带损伤的正确路线，单纯在 RGB 上抖会丢掉"只是色度漂、亮度没坏"的特征
- Tracking 控制用 x×1 控制贴图把多条属性（UV 偏移强度、tracking 线可见度）压进 RGB 通道，是经典"把 1D 曲线塞进小贴图"的数据驱动做法
- 相对 Post Process 版少了 *Scale In Screen Space*——因为网格 UV 与屏幕分辨率无关

## 链接到的概念

- [[crt-shader-effects]]
- [[color-quantization-retro]]

## 原文

- 链接：https://danielilett.com/retro-shaders-godot/crt-mesh/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-godot-crt-mesh.md`
