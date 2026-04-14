---
tags: [source, rendering, shader, 光谱, 颜色]
date: 2026-04-14
sources: 1
---

# Improving the Rainbow – Part 2（Alan Zucconi）

[[alan-zucconi|Alan Zucconi]] 2017 年 7 月的文章，在 GPU Gems 原版"bump 方案"基础上用数值拟合得到显著更准的 **branchless 波长→RGB 映射**函数 `spectral_zucconi` / `spectral_zucconi6`。

## 摘要

GPU Gems 书中给出用三条抛物线（bump）拼接 R、G、B 分量的波长→颜色函数，好处是没有分支、GPU 友好，坏处是原作者手调的系数拟合误差很明显。Zucconi 保留 bump 的结构，用 Python 数值优化重拟合 9 个常量，得到的 `spectral_zucconi` 已经在紫、橙段明显优于 GPU Gems。再用**6 条 bump 叠加**得到的 `spectral_zucconi6` 精度更高，代价只是多一组常量和一次 `bump3y`。整个函数完全 branchless——非常适合衍射光栅、薄膜干涉这类需要在单个像素里对多个波长并行求值的 shader。文末附有 Shadertoy WebGL 链接与 Python 拟合脚本。

## 关键要点

- GPU Gems 的 bump 方案只需要 `bump(x) = max(0, 1 - x²)` + 三个偏移，structure 正确但常量手调
- Zucconi 用 Python 数值优化 9 个常量，得到 `spectral_zucconi`
- 6-bump 版本 `spectral_zucconi6` 在紫/橙段继续改善
- 所有方案都是完全 branchless（纯乘加 + `saturate`），避免 warp divergence
- 这是 shader art 下对"波长可视化"的廉价近似，不等同于真正的 CIE XYZ → sRGB

## 链接到的概念

- [[spectral-zucconi-rainbow]]
- [[spectral-rendering]]
- [[hero-wavelength-spectral-sampling]]
- [[diffraction-grating-shader]]

## 原文

- 链接：<https://www.alanzucconi.com/2017/07/15/improving-the-rainbow-2/>
- 本地：`raw/articles/alanzucconi.com/2017-07-15_improving-the-rainbow-part-2-alan-zucconi.md`
