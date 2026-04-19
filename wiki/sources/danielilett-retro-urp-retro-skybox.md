---
tags: [source, unity, urp, shader, 复古, psx, skybox]
date: 2026-04-19
sources: 1
---

# Retro Shaders Pro for URP - Retro Skybox（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 URP 版 *Retro Shaders Pro* 撰写的 **Retro Skybox** 参数手册。

## 摘要

这是 Unity 内置 Skybox (Cubemap) shader 的 PSX 风衍生品，在原有 cubemap 采样之外叠了两层控制：一是复古量化（*Resolution Limit* 向下取到 2 次幂、*Color Depth* + *Color Depth Offset*、*Use Point Filtering*、*Dithering Mode* 提供 screen / texture / off 三档），和 [[retro-rendering-techniques|Retro Lit]] 的色深段参数一致；二是 Sky Background 双档——*Cubemap* 模式从 cubemap 采样（带 *Rotation* 绕 y 旋转），*Gradient* 模式用 *Ground Color* / *Sky Color* + *Color Mix Power* 控制地平线到天顶的 lerp 曲线。两者之上再叠一层可开关的程序云（*Use Clouds*）：两份独立噪声（*Cloud Sizes* 是两个值）通过 *Combine Mode*（add/subtract/multiply/divide）合成；*Cloud Height Threshold* 以一对值控制仰角衰减（云从多高开始出现 → 多高满不透明）；*Cloud Density Threshold* 对噪声做双阈值 smoothstep；*Cloud Velocity* 驱动 UV 时间滚动；*Cloud Color* 做整体染色。整个 shader 是「复古量化工具 + 经典程序云」的参数化拼接。

## 关键要点

- *Resolution Limit* 向下 round 到最近 2 的幂——避免非整数缩放的亚像素噪点
- Sky Background 两档——*Cubemap*（传统）或 *Gradient*（无贴图纯程序天空）；*Color Mix Power* 控制地平线/天顶混合曲线陡峭度
- 程序云是**两份独立噪声**通过 *Combine Mode* 合并——快慢/大小不同的叠加让云从「单调斑块」变成「有层次的云团」
- 两对阈值正交：*Height Threshold* 管「哪里能看到云」，*Density Threshold* 管「云占噪声空间百分比」
- 色深量化 + dither 组合搬到天空盒，主要解决天空大面积渐变的 [[color-banding|色带]] 问题

## 链接到的概念

- [[procedural-retro-skybox]]
- [[retro-rendering-techniques]]
- [[color-quantization-retro]]
- [[dither-alpha-clipping]]
- [[classic-shader-noise]]

## 原文

- 链接：https://danielilett.com/retro-shaders-pro/skybox-cubemap/
- 本地：`raw/articles/danielilett.com/2026-01-01_retro-shaders-pro-for-urp-retro-skybox.md`
