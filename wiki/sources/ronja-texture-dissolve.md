---
tags: [source, rendering, shader, vfx, unity]
date: 2026-04-14
sources: 1
---

# Texture Dissolve（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 于 2018 年 12 月发表的 Unity surface shader 教程，讲如何用一张灰度纹理驱动网格按 pattern 渐进溶解，并在消失边缘加一圈 HDR 发光带。

## 摘要

核心是一个三行公式：从 dissolve 纹理读单通道灰度 → 乘 0.999 避免纯白永不消失 → 减去全局 `_DissolveAmount` → 把结果喂给 `clip()`。负值的像素被 `discard`，形状由 dissolve 纹理决定——只改纹理就能切换出「水流蔓延 / 扫描线 / 同心圆扩散」等各种演出观感，是典型的**数据驱动 VFX**。文章第二部分加入「边缘发光」：用 `smoothstep(_GlowRange + _GlowFalloff, _GlowRange, isVisible)`（注意端点反向）识别「即将被 clip」的像素，赋予它们一份 HDR emission，配合 bloom 就能得到「正在烧焦的灰烬边缘」。整套 shader 写在 Unity 的 Standard surface shader 框架下，自动继承阴影 pass 里的 clip 行为。文章明确指出 dissolve 纹理的 UV 来源可以是模型 UV、屏幕空间、[[planar-mapping|triplanar world]] 或程序化噪声——坐标源和采样函数解耦是本教程的隐藏教学点。

## 关键要点

- `clip(x)`：x < 0 时 discard 当前 fragment，是二值化的淡出路径（对比 alpha blending 的半透明淡出）。
- `dissolve * 0.999`：把最亮的像素推到 1 以下，确保 dissolve 推到 1 时模型彻底消失——一个小但实用的数值稳定性技巧。
- `smoothstep(high, low, x)`：两个端点反向可以直接得到「离临界越近越亮」的反向渐变，是 shader 里常用的表达式节省。
- surface shader 自动生成的 shadow caster pass 继承 `clip`——换成手写 vertex/fragment 的话需要自己在 shadow pass 里重复这个逻辑。
- dissolve 纹理的坐标来源可灵活替换：模型 UV / 屏幕 / 世界 / triplanar / 程序化。

## 链接到的概念

- [[texture-dissolve]]
- [[fizzle-lod-fading]]
- [[fragment-shader]]
- [[alpha-blending]]
- [[planar-mapping]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/038-dissolve/>
- 本地：`raw/articles/ronja-tutorials.com/2018-12-15_texture-dissolve.md`
