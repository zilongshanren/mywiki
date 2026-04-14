---
tags: [source, 渲染, color-lut, webgl]
date: 2026-04-14
sources: 1
---

# How video games use LUTs and how you can too（Frost / frost.kiwi）

[[frost-kiwi|Frost]] 发表于 2024 年 2 月的长文，用一串可交互 WebGL 演示把 1D 和 3D 颜色查找表（[[color-lut|LUT]]）在游戏中的实际用途讲透——从热成像的 palette 着色，到 **Left 4 Dead** 里「一张车辆贴图 + 一张 mask 得到 4 种车身颜色」的 tinting 技巧，再到用 DaVinci Resolve 离线烘焙 3D LUT 做整套电影级色彩分级。

## 摘要

文章围绕一句话展开：**预计算进查找表，代价几乎为零**。在 fragment shader 里，一次贴图采样的延迟远大于任何算术——因此把 tinting、gamma 修正、饱和度、色相分离、胶片 look 等所有「只看当前像素颜色就能算出新颜色」的操作**全部烘焙进 LUT** 是工程上最划算的路。Frost 先用 1D LUT 把灰度热成像映射成彩色，然后逐步递进：1D LUT 的游戏用法（Valve 的 Source Engine 用 mask 通道对同一辆车 tinting）、1D LUT 的软件 gamma ramp（Redshift 的夜间暖色滤镜）、3D LUT cube（33³ 或 32³ 的完整 RGB→RGB 映射）、以及标准游戏行业工作流：截屏 + 初始 LUT → 在 Photoshop/Resolve 里调色 → 导出 LUT → shader 里采样。文章还解释了为什么**不能用卷积类滤镜**（blur/sharpen）调 LUT——它们会把本应按像素独立重映射的颜色互相污染。最后他分享了一个极端用途：《Tomb Raider》GBA 移植里有一张 LUT **被当作整数除法的查找表**放在 ROM 开头——连 load 指令都省了。

## 关键要点

- GPU 上的 texture tap 延迟远高于 ALU，因此 LUT 路径基本是「免费」的
- 1D LUT 的经典游戏用途：tinting mask 让一个模型贴图变成多种外观（Left 4 Dead 的车辆、服装）
- 3D LUT 用来承载无法用 1D 分离的颜色变换：饱和度、色相、颜色隔离
- 电影级调色的标准流程是 DaVinci Resolve → .cube → shader，shader 端只是一次 3D 纹理采样
- 3D LUT 只要 32³–33³ 的大小就足够——连 Panasonic 的专业级相机都只用 17³
- WebGL 1 没有 3D 纹理，要手动把 3D 采样降为两次 2D 采样 + 一次 mix（Gregg Tavares 的经典代码，2019 年修过一个 Z 轴 bug）
- 卷积滤镜（blur/sharpen）**不能** 用在 LUT 上——它们会混合本应独立映射的颜色样本
- Redshift 夜间滤镜的 gamma ramp 是「零开销」的：它不是 shader 在画面上跑，而是送到显示器固件里——可惜这个 API 在各平台上都在退役

## 链接到的概念

- [[color-lut]]
- [[fragment-shader]]
- [[alpha-blending]]
- [[display-edid-colorspace]]
- [[frost-kiwi]]

## 原文

- 链接：<https://blog.frost.kiwi/WebGL-LUTS-made-simple/>
- 本地：`raw/articles/blog.frost.kiwi/2024-02-28_how-video-games-use-luts-and-how-you-can-too.md`
