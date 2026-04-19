---
tags: [source, unity, urp, shader, crt, vhs, mesh]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for URP - CRT (Mesh)（Daniel Ilett）

[[daniel-ilett]] 为 URP 版 *Retro Shaders Pro* 撰写的 **CRT Mesh** 参数手册——把 CRT/VHS 滤镜从全屏 post-process 搬到普通 mesh 上的变体，适合游戏内 CCTV/监视器一类的场景对象。

## 摘要

与 [[sources/danielilett-retro-godot-crt-mesh|Godot 版 CRT Mesh]] 几乎同款参数结构：*Base Color / Base Texture / Pixel Size / Force Point Filtering* 控制像素化基础；Barrel Distortion 段用 *Distortion Strength / Smoothing / Background Color* 做桶形畸变 + 圆角黑边；RGB Subpixels & Scanlines 叠加 *RGB Subpixel Texture / Strength / Scanline Texture / Strength / Size / Scroll Speed* 实现子像素条纹 + 滚动扫描线——两个参考贴图（*RGBTexture.png* / *ScanlineTexture.png*）随 pack 提供。VHS Artifacts 段是这个 shader 的"做旧层"：*Random Wear*（水平 UV 扰动）、*Aberration Strength*（屏幕边缘色差增强）、*Tracking Texture*（x-by-1 的控制贴图，R 通道控 UV 偏移强度、G 通道控 tracking 线的出现）、*Tracking Size/Strength/Speed/Jitter*、*Tracking Color Damage*（画面转到 YIQ 色空间后只扰动 I/Q 两通道，模拟 NTSC 磁带色度损伤）、*Tracking Lines Threshold/Color*。Color Adjustments 给 *Tint / Brightness / Contrast / Color Ramp Mode / Color Ramp Texture*；Color Ramp 预设覆盖 16 台历史主机（Game Boy / Gameboy Advance / NES / SNES / MSX2 / IBM PS/2 / Amstrad CPC / Teletext / ZX Spectrum / Sega Master System / Genesis / Game Gear 等），每档位精确列出 "每通道几 bit、共多少色"——只实现 palette restriction 不实现 simultaneous color restriction。相对 Post Process 版，Mesh 版少了 Scale In Screen Space、Reference Resolution、Use VHS Tracking toggle 等 screen-level 控制。

## 关键要点

- Mesh 版贴在网格 UV 上，适合 CCTV 屏、游戏内监视器、HUD 小电视等**场景对象**而非全屏滤镜
- Tracking Texture 的 RG 双通道编码：R 控 UV 偏移、G 控扫描线出现率——一张 x-by-1 贴图塞两套控制曲线，节省参数和 texture slot
- *Tracking Color Damage* 把颜色转到 **YIQ 色空间**再扰动 I/Q（色度）——这是模拟 NTSC 磁带色度损伤的物理正确路径，不是随便乘个 tint
- Color Ramp 的 16 种预设只还原 **palette restriction** 不还原 **simultaneous color restriction**——SNES 实际只能同屏 256 色但 palette 是 15-bit RGB，这个 mapper 只做后者
- 相比 Post Process 版少 Scale In Screen Space / Reference Resolution——mesh 的 UV 是对象自身的，天然无需跨分辨率视觉一致处理

## 链接到的概念

- [[crt-shader-effects]]
- [[color-quantization-retro]]
- [[chromatic-aberration-post]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/crt-mesh/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-crt-mesh.md`
