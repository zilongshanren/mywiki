---
tags: [source, rendering, unity, 后处理, 体积雾]
date: 2026-04-14
sources: 1
---

# Adventures in postprocessing with Unity（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 于 2015 年 7 月发表的 Unity 后处理实验笔记：在 Unity 开放免费版的低层图形接口后，重新评估它作为 shader 原型环境的可用性，具体做法是实现一条多步体积光束后处理 pipeline。

## 摘要

文章先讲怎么用 Unity 最小代价写自定义后处理（继承 `PostEffectsBase`、重写 `OnRenderImage`、用 `Graphics.Blit` 触发全屏 pass、靠 `_MainTex` / `_TexelSize` 约定拿输入），然后逐步推到一个完整的体积光束后处理 pipeline：四分之一分辨率 raymarching 算雾、interleaved sampling 提升等效采样数、bilateral-depth 加权的 7-tap 可分离高斯、nearest-depth 上采样合成。关键 Unity-side trick：通过 `CommandBuffer.SetGlobalTexture` 在 `LightEvent.AfterShadowMap` 时刻把 shadow map 暴露成全局采样器名字，给后处理 shader 使用。阴影坐标则按 `_LightSplitsNear/Far` 的 cascade 权重重组。结论是：有了低层图形访问后，Unity **可以**作为一个严肃的原型环境——比自己从零起 DX11 省很多胶水代码。

## 关键要点

- Unity 的 `OnRenderImage(source, destination)` + `Graphics.Blit(source, destination, material)` 是最轻的自定义后处理 API。
- `_MainTex_TexelSize` 会被自动填充成 `(1/w, 1/h, w, h)`，非常省事。
- Deferred 模式下 `_CameraGBufferTexture0..3` 和 `_CameraDepthTexture` 是全局可采样的。
- Shadow map 需要 CommandBuffer 在 `LightEvent.AfterShadowMap` 时 `SetGlobalTexture` 才暴露给 shader。
- **深度降采样必须用 min/max 不能 avg**——平均会伪造边缘深度。
- **Interleaved sampling** 把 32 样本摊到 8×8 网格上，等效 2048 virtual samples/ray。
- **Bilateral Gaussian**：用低分辨率 depth 差做指数权重 `exp(-(Δz·falloff)²)`，边缘权重迅速衰减。
- **Nearest-depth upsample**：low-res 邻域 depth 接近 hi-res 则 bilinear，否则取最接近的 low-res texel。
- 合成公式：`colour * fogSample.a + fogSample.rgb`（alpha 存透射率）。

## 链接到的概念

- [[unity-postprocessing-adventures]]
- [[volumetric-raymarching-intro]]
- [[volumetric-fog-froxels]]
- [[bilateral-filter]]
- [[depth-aware-upsampling]]
- [[unity-image-effect-basics]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2015/07/03/adventures-in-postprocessing-with-unity/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2015-07-03_adventures-in-postprocessing-with-unity.md`
