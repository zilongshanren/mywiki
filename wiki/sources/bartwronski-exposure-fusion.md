---
tags: [source, 渲染, hdr, 色调映射]
date: 2026-04-14
sources: 1
---

# Exposure Fusion – local tonemapping for real-time rendering（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2022 年 2 月发表的长文，把他在 Sony Santa Monica（God of War）和 Google Pixel HDR+ 两段经历串起来，介绍 **Exposure Fusion** 算法——一个简单到可以在 300 行 WebGL 里实现、又足以替代 bilateral grid / Local Laplacian Filter 这类复杂方案的局部色调映射方法。文章配了一个浏览器在线 demo。

## 摘要

文章先说明实时渲染为什么需要 [[local-tonemapping]]：物理光照管线必然产生大动态范围，全局 tonemapping 在「亮处不过曝、暗处不死黑」之间无解。作者回顾自己在 God of War 上做的「Gaussian 模糊亮度后决定曝光」简陋版，承认会有 halo；推到极限会非常难看。然后系统地比较 per-pixel blending、Gaussian blending、bilateral、bilateral + Gaussian（Jasmin Patry 在 Ghost of Tsushima 用的方案）、guided filter blending 几种思路的优缺点。

正题是 **Mertens 等人的 Exposure Fusion**：为每张合成曝光建 [[laplacian-pyramid]]，为权重图建 Gaussian 金字塔，**在每一层用对应分辨率的权重 blend Laplacian**——曝光过渡的频率自动跟随图像内容的频率。文章给了完整算法步骤、关键参数（最粗 mip 层、shadows / highlights、exposure preference sigma）、一个可选的 local contrast boost（与 Lightroom 「Clarity」滑块本质相同）、GPU 实现要点（多曝光打包、Laplacian = Gaussian 之差），以及用 [[guided-filter]] 在 1/4 × 1/4 分辨率算完再升采样的优化路径——HDRNet、Pixel Portrait Mode、HDR+ 都用这套套路。

## 关键要点

- **核心洞察**：曝光变化的频率应当和图像内容的频率相关——平坦区大半径柔和过渡，强边缘附近小半径锐利切换，让变化「藏在边缘里」。
- **Laplacian 金字塔分尺度融合**：每层 Laplacian 用对应分辨率的权重 blend，几乎完全消除 halo，又比 bilateral 没有振铃。
- **权重只用「曝光适当性」就够**：原论文的 contrast / saturation / exposedness 三件套里，后两个会让画面偏向 toxic HDR look。
- **参数有点反直觉**：行为依赖图像频率内容，同样的 shadows 设置在不同场景下亮度不同——需要艺术家调参。
- **算法可以在 1/4 分辨率算完再 guided upsample**——成本大约 < 1ms。
- **历史连贯性**：Ansel Adams 的 dodge & burn、Lightroom 默认开图、Pixel HDR+「look」都是同一个家族。

## 链接到的概念

- [[local-tonemapping]]
- [[exposure-fusion]]
- [[laplacian-pyramid]]
- [[guided-filter]]
- [[color-space]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2022/02/28/exposure-fusion-local-tonemapping-for-real-time-rendering/
- demo：https://bartwronski.github.io/local_tonemapping_js_demo/
- 本地：`raw/articles/bartwronski.com/2022-02-28_exposure-fusion-local-tonemapping-for-real-time-rendering.md`
