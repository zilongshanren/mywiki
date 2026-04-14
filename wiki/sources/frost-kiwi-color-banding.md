---
tags: [source, 渲染, 颜色, dither, shader]
date: 2026-04-14
sources: 1
---

# How to (and how not to) fix color banding（Frost / frost.kiwi）

[[frost-kiwi|Frost]] 发表于 2023 年 10 月的长文，以一个 WebGL 半径向渐变作为最小示例，一步步展开「色带是什么 / 怎么用一行 GLSL 灭掉它 / 大厂都是怎么做的」。全文嵌入十几个可交互 WebGL canvas，读者可以直接在自己的屏幕上看到色带、dither 和 interleaved gradient noise 的叠加效果。

## 摘要

文章围绕 **[[color-banding]]**（color banding / posterization）展开。Frost 先演示一个极小、极深色的径向渐变就能在 8-bit 面板上制造明显色带；然后祭出 Jorge Jimenez 在 *Call of Duty: Advanced Warfare* presentation slide 123 公布的 **Interleaved Gradient Noise**——一行 `fract(52.9829189 * fract(dot(uv, vec2(0.06711056, 0.00583715))))` 搞定的 GPU 友好 dither，以 `1.0/255.0` 的幅度直接叠加到渐变上，视觉上噪点几乎不可见却彻底打散色阶。接着他吐槽 6-bit 面板 + FRC 的「double dither」会和 shader dither 形成干涉条纹，这种面板没救。文章后半部分横向对比了五家业界实现：Valve Portal 2/The Lab 的 7 指令 animated RGB dither、Alien: Isolation 的 film grain / Deep Color 10-bit / 什么都不做三条路、ReShade Deband.fx 基于 Weber ratio 检测的 post-process dither、After Effects Gradient Ramp 的 Ramp Scatter、KDE Plasma KWin 的 Dual Kawase blur + noise、Windows 11 Acrylic 的 blur + noise。最后附录了一个 16-bit 灰度测试 PNG，用来通过相机翻拍屏幕实测面板真实位深。

## 关键要点

- 色带根源是量化精度不足，深色大面积渐变最易受害
- Interleaved Gradient Noise：一行 GLSL，单 fragment 不 tap 贴图，以量化步长为幅度叠加到渐变
- 「proper」方法是 error diffusion，但它是顺序算法，GPU 上没法并行
- Ordered dither（Bayer）便宜但静态画面下图案易见
- 6-bit 面板 + FRC 和 shader dither 会干涉产生可见斜纹——别硬调，认倒霉
- Valve dither 用三个质数 `(103, 71, 97)` 给三通道去相关，并用 `g_flTime` 每帧抖动
- Alien: Isolation 的 Deep Color 10-bit 开启后反走样会被迫关闭——大多数 AA shader 会砸回 8-bit
- ReShade Deband 先检测平坦区域（Weber ratio + 标准差）再只对带内像素 dither
- KDE KWin blur 和 Windows 11 Acrylic 都走 blur + noise 的后处理组合
- 附录的 16-bit 测试 PNG 可以直接手机翻拍屏幕读面板真实位深（3 条 = 8-bit、9 条 = 10-bit、33 条 = 12-bit）

## 链接到的概念

- [[color-banding]]
- [[dither-alpha-clipping]]
- [[color-space]]
- [[display-edid-colorspace]]
- [[frost-kiwi]]

## 原文

- 链接：<https://blog.frost.kiwi/GLSL-noise-and-radial-gradient/>
- 本地：`raw/articles/blog.frost.kiwi/2023-10-19_how-to-and-how-not-to-fix-color-banding.md`
