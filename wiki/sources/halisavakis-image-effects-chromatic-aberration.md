---
tags: [source, 渲染, unity, shader, 后处理, 色差]
date: 2026-04-14
sources: 1
---

# My take on shaders: Chromatic Aberration (Harry Alisavakis)

[[harry-alisavakis]] 在 *My take on shaders* 系列的第四篇（2017-05-10）做了一支自己写的全屏色差后处理。

## 摘要

Alisavakis 不喜欢 Unity 内置色差「绿—品红」二色调色盘的滥用，想要一个能看到独立 R/G/B 三个通道分别偏移的版本，灵感来自 *Layers of Fear*。实现的核心非常朴素：fragment shader 里对同一张 `_MainTex` 做三次采样，红通道用 `(uv - amount, uv - amount)`、绿通道用原 `uv`、蓝通道用 `(uv + amount, uv + amount)`，再合成成一个 `fixed4`。`_Amount` 用 `Range(0.0, 1)` 做 slider 限制，作者特别提醒这个效果非常强烈，实际值往往要小于 0.001。文末他强调：色差适合用来强化关键事件（命中、传送、破甲），而不是常驻全屏滤镜——他自己在 *Liches and Crawls* 里就是这么用的。文章写完没多久 Unity 官方 Post-Processing Stack 就出了内置色差，但「全屏均匀偏移」依然是他这个写法独占的细分。

## 关键要点

- **核心算法**：三次纹理采样、每个色通道用不同的 UV 偏移、合成回 `fixed4(R, G, B, 1)`。
- 这是「全屏均匀偏移」型色差，和 Deadlight / Black Mesa 那种**径向梯度**的「光学色差」是不同口味——参见 [[chromatic-aberration-post]] 对两类的区分。
- 偏移方向可以任意改：对角线（本文）、纯水平、按噪声扰动……每种风格都不一样。
- 数值要小：`Range(0.0, 1)` 只是 slider 上限，实际美术值通常 0.0005 量级。
- 美术上的红线：色差是「事件强化器」而不是常驻滤镜，常和命中反馈、传送、破甲这类瞬时事件配合。

## 链接到的概念

- [[chromatic-aberration-post]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-chromatic-aberration-introduction-to-image-effects-part-iv/>
- 本地：`raw/articles/halisavakis.com/2017-05-10_my-take-on-shaders-chromatic-aberration-introduction-to-imag.md`
