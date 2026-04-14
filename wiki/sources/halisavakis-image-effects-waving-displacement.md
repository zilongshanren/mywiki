---
tags: [source, 渲染, unity, shader, 后处理, displacement, 动画]
date: 2026-04-14
sources: 1
---

# My take on shaders: Waving Displacement (Harry Alisavakis)

[[harry-alisavakis]] 在 *My take on shaders* 系列的第七篇（2017-06-01）把上一篇的位移 shader 改成了一个会随时间漂动的水波纹后处理。

## 摘要

和 [[sources/halisavakis-image-effects-simple-displacement|前一篇]]的主要区别有两处：（1）位移贴图不再当灰度遮罩、而是当 RG 双通道的二维向量场——红通道驱动 X 偏移、绿通道驱动 Y 偏移；（2）纹理本身的采样 UV 加上 Unity 内置的 `_Time.x`，让位移场每帧都在屏幕上漂动，从而产生持续的扰动。关键的一行算术 `displ = (displ * 2 - 1) * _DisplAmount` 把纹理像素的 `[0, 1]` 范围拉到正负，否则位移永远只是单方向偏置，做不出真正的「波动」感。Alisavakis 介绍 `_Time` 是 Unity 内置的 `(t/20, t, 2t, 3t)` 四分量 float4，工程师可以选不同分量得到不同滚动速度。整支 shader 还是十几行的 image effect，但已经能糊弄出一个伪水面 / 玻璃热浪的视觉。这个 trick 的源头他归功于 Dan Moran 的 *Makin' Stuff Look Good In Unity* YouTube 系列。

## 关键要点

- 位移贴图按 R/G 通道存二维向量场，和 normal map 的 packing 思路同构。
- **`(x * 2 - 1)` 把无符号纹理像素 `[0,1]` 拉成有符号 `[-1,1]`**，这是几乎所有「贴图当向量场」用法的标配。
- **`_Time = (t/20, t, 2t, 3t)`**：Unity 内置的时间 uniform，不同分量对应不同滚动速度；选 `_Time.x` 得到最慢的漂动。
- 同一张静态贴图 + 时间滚动 UV → 输出是动态的扰动场。
- 是 2D 水面 / 折射 / 热浪等效果的「最便宜起步形态」，可以叠在物体或全屏上。
- 灵感来源：Dan Moran 的 *Makin' Stuff Look Good In Unity* YouTube 频道。

## 链接到的概念

- [[uv-displacement-image-effect]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-waving-displacement/>
- 本地：`raw/articles/halisavakis.com/2017-06-01_my-take-on-shaders-waving-displacement.md`
