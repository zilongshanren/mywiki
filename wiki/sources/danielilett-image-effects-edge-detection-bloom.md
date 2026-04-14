---
tags: [source, rendering, shader, unity, edge-detection, bloom, post-processing]
date: 2026-04-14
sources: 1
---

# Image Effects Part 4 — Edgy Talk（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 4 篇，讲了如何在屏幕空间用 [[sobel-edge-detection|Sobel-Feldman 算子]]检测边缘、如何把边缘图变成 Neon 滤镜、以及如何搭一个最小的 [[bloom-threshold-blur-composite|三步 Bloom]] 让 Neon 发光，最终复刻 Super Mario Odyssey Snapshot Mode 的 Line Drawing / Neon 两种滤镜。

## 摘要

文章先从"什么是边"谈起：没有几何信息时，屏幕空间里**颜色剧烈变化**的地方就是边。Sobel 用一对 3x3 核 `Gx` / `Gy` 分别估算水平/竖直梯度，合成时取勾股模长 `sqrt(Gx² + Gy²)`——两个方向核无法合并成一个矩阵，但因为尺寸小，作者直接把 12 条有效 tap 硬编码展开而不写循环。得到的"边缘强度"可以反相做 Line Drawing，也可以作为**亮度掩膜**乘到原图上做 Neon——为了让颜色炸起来，顺手塞进一段来自 `lolengine.net` 的 `rgb2hsv` / `hsv2rgb` HLSL 实现，把饱和度和明度强制推到 1.0。第二半文章实现了简易 Bloom：**Step 1** 阈值 pass 只保留亮度高于 `_Threshold` 的像素，**Step 2** 用 `UsePass "Shader/PASSNAME"` 直接复用前一篇的高斯模糊 pass（单 pass 或可分离多 pass 可切换），**Step 3** 合成 pass 读两张纹理（模糊结果走 `_MainTex`，原图用 `material.SetTexture("_SrcTex", src)` 显式绑）相加输出。C# 脚本 `ImageEffectBloom` 负责编排临时 RT、pass 索引、`BlurMode` 枚举切换。结尾演示多个 image effect 组件按序叠在相机上即可链成 Neon Bloom 完整效果。

## 关键要点

- **Sobel 算子**用两个 3x3 核分别做水平/竖直梯度，合成用 `sqrt(Gx²+Gy²)`；两核不能合成一个矩阵。
- 边缘检测效果很便宜，但会把**阴影边**也识别为物体边，需要关影或拥抱它当风格。
- Neon = Sobel 掩膜 × HSV 饱和度推满；`rgb2hsv/hsv2rgb` 没有内置，用第三方 GLSL 改 HLSL。
- Bloom 的三步：**亮度阈值 → 模糊 → 原图 + 模糊合成**；每一步都是一个 Blit 到临时 RT。
- **`UsePass "Shader/PASSNAME"`**：跨 shader 复用 pass，pass 名必须大写、Properties 必须在当前 shader 重声明，不会继承。
- 合成 pass 的第二张纹理要用 `material.SetTexture("_SrcTex", src)` 手动绑——`Graphics.Blit` 只管 `_MainTex`。
- GPU shader 里用**三目运算符** `(a > b) ? x : y` 替代 `if` 避免分化。
- 多个 image effect 组件按"从上到下"的顺序在相机上串联执行，这是 built-in 管线后处理链的基本机制。

## 链接到的概念

- [[sobel-edge-detection]]
- [[bloom-threshold-blur-composite]]
- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[unity-image-effect-basics]]
- [[image-effect-colour-transform]]

## 原文

- 链接：https://danielilett.com/2019-05-11-tut1-4-smo-edge-detect/
- 本地：`raw/articles/danielilett.com/2019-05-11_image-effects-part-4-edgy-talk.md`
