---
tags: [source, shader, shadergraph, 后处理, vfx, 复古]
date: 2026-04-14
sources: 1
---

# Retro CRT Shader Breakdown（Cyan）

[[cyanilux|Cyan]] 2020 年 9 月发表的拆解教程，讲解一个用 URP Shader Graph 实现的复古 **CRT（阴极射线管）显示器**效果。作品原本是为 [[harry-alisavakis|Harry Alisavakis]] 的 `#TechnicallyAChallenge` "Retro" 主题做的，代码开源在 [`URP_RetroCRTShader`](https://github.com/Cyanilux/URP_RetroCRTShader)。

## 摘要

文章把最终效果拆成 5 个彼此独立的 shader trick：(1) **CRT 弯曲**——用 `Spherize` 节点把 UV 按球面映射，再用 `Rounded Rectangle` 蒙板盖掉四角的溢出；(2) **扫描线**——对 UV 的 Y 分量做 `Fraction` 拿到周期，配合 `Abs(x-0.5)` 变成 V 形塑形再乘回颜色；(3) **RGB 子像素条纹**——用 `Modulo 3` 造周期、`Step` 切 R/G/B 三段，相乘前 `Add` 一个亮度补偿避免画面变暗；(4) **水平抖动和静电**——用 `Simple Noise` 做 X 偏移，用 `Random Range` 做逐帧像素噪声叠加；(5) **滚动水平亮带**——对 Y+Time 做 `Fraction + Power 5` 得到陡峭的滚动带，再通过 HSV→RGB 转换上色，同时给 distortion 的振幅加一次调制。

整个效果通过 [[blit-render-feature|Blit Render Feature]] 插进 Forward Renderer，pass event 设为 *Before Rendering Post Processing*。Shader Graph 的 `Keyword` 节点让每个效果都能单独 toggle，用 `shader_feature` 定义时未使用的变体会从构建里剥离。

## 关键要点

- 复杂的 shader 效果可以被拆成数个正交的小 trick，每个 trick 都是"造周期（Fraction/Modulo）+ 塑形（Step/Abs/Power）+ 合成（乘或加）"的组合。
- `Spherize` 节点是模拟 CRT 球面弯曲的简洁方案；输出的 UV 要替代所有下游采样的 UV 输入。
- RGB 条纹分辨率应该是 3 的倍数（如 384 = 128×3），否则会出现 moiré；子像素相乘会让画面变暗，需要事先 `Add` 一个 brightness 常量补偿。
- `Random Range` 产生的静电应**加**到颜色上（叠加高光噪点），而不是乘（会把暗区压得更暗）。
- Shader Graph 的 Keyword 数量会让变体数翻倍，同时使用不同变体的材质无法被 SRP Batcher 合批，是性能陷阱。

## 链接到的概念

- [[crt-shader-effects]]
- [[blit-render-feature]]
- [[urp-volume-post-processing]]
- [[uv-manipulation-nodes]]
- [[harry-alisavakis]]

## 原文

- 链接：https://cyangamedev.wordpress.com/2020/09/10/retro-crt-shader-breakdown/
- 本地：`raw/articles/cyangamedev.wordpress.com/2020-09-10_retro-crt-shader-breakdown.md`
