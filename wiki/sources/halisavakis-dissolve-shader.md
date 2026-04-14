---
tags: [source, 渲染, unity, shader, vfx, dissolve]
date: 2026-04-14
sources: 1
---

# My take on shaders: Dissolve shader (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列 2017-07-22 的一篇，用一支 Unity surface shader 复刻「物体按噪声纹理逐点消失 + 边缘烧焦」的经典 VFX。

## 摘要

核心做法是典型的 [[texture-dissolve|texture dissolve]] 模板：`tex2D(_SliceGuide, uv) - _SliceAmount` 得到 `[-1, 1]` 的 test 值，`clip(test)` 丢弃负的像素，同时 `if (test < _BurnSize)` 用一张 color ramp 把还没丢但接近边界的像素加 emission，得到烧焦色带。Alisavakis 自己把两个坑写得非常诚实：第一是必须 `Cull Off`，否则从 dissolve 洞里看不到背面会穿帮；第二是 `#pragma surface surf Lambert addshadow` 中的 `addshadow` 不能漏——Unity surface shader 默认的 shadow caster pass 不会跟着 `clip`，需要显式让阴影 pass 复用 surf 的 clip 逻辑，否则"物体消失了但影子还在"。burn ramp 是一张灰度 / 彩色 lut，Alisavakis 把 `test * (1 / _BurnSize)` 映射到 ramp 的 X 轴上，靠 `_BurnColor * _EmissionAmount` 再乘色调。

## 关键要点

- `clip(tex2D(slice, uv) - amount)` 是 [[texture-dissolve|texture dissolve]] 的最小骨架。
- **`Cull Off` 必选**，否则 dissolve 出的洞看不见背面。
- **surface shader 的 shadow caster 需要显式 `addshadow`**，否则 clip 不会同步到阴影 pass。
- Burn 边缘通过"`test - _BurnSize < 0` 的像素加 emission"实现，和 dissolve 本身共用同一张 `_SliceGuide`，只是阈值不同——一个做丢弃、一个做发光，形成连贯的烧焦带。
- Color ramp 是一张 1D 贴图，把 `test / _BurnSize` 当 U 坐标去采样；换 ramp 就是换颜色走向（橘红 → 白、黄 → 黑、等等）。
- 代码诚实写了 "I figured that out after quite a lot of time experimenting" —— surface shader 的 shadow + clip 组合在 2017 年 Unity 手册里没有明确写，属于踩坑才知道。

## 链接到的概念

- [[texture-dissolve]]
- [[unity-surface-shaders]]
- [[fragment-shader]]
- [[shadow-mapping-basics]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-dissolve-shader/>
- 本地：`raw/articles/halisavakis.com/2017-07-22_my-take-on-shaders-dissolve-shader.md`
