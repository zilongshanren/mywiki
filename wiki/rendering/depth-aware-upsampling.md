---
tags: [渲染, 采样, 上采样, stencil]
date: 2026-04-14
sources: 1
---

# Depth-Aware Upsampling

**把半分辨率计算的屏幕空间效果升采样回全分辨率，同时尊重几何不连续性**。几乎所有的 AAA 引擎都需要这个基础设施——SSAO、SSR、volumetric fog、particles、ambient lighting 都会在低分辨率下计算以节省带宽，然后升采样回来合成。

## 为什么 bilinear 不够

最简单的 upsampling 是把相邻 4 个低分辨率像素 bilinear 插值。这在**连续表面**上是合理的——误差可控。但在**深度不连续**处（物体边缘、物体和背景的交界），bilinear 会把两个完全无关的颜色值混在一起，产生光晕（halo）或渗色。

## 标准做法：depth-weighted 重建

改进做法是在 upsampling shader 里额外读取**全分辨率深度 buffer**和**低分辨率深度 buffer**，比较样本深度与目标像素的深度差。差得太远的样本就不参与插值，权重置 0 —— 相当于把 bilinear 换成「只用在相同表面上的样本」做加权平均。

这个算法是对的，但有个问题：**所有像素都要跑这个复杂 shader**，即使大多数像素其实在连续区域里。带宽和算术都被浪费了。

## ROTR 的 stencil discard trick

Foundation 引擎用了一个更省的方案：

1. **法线 pass 结束后**，跑一个全屏 pass，扫描深度 buffer，把所有**深度不连续的像素**标记到 stencil buffer 里。
2. **Upsample 时提交两次 draw**：
   - 第一次用**简单 shader**，stencil test 只让「连续」像素通过——这些像素跑几条指令的 bilinear 插值
   - 第二次用**复杂 shader**，stencil test 只让「不连续」像素通过——这些像素跑带深度权重的版本
3. **Early stencil discard** 保证每个 pixel 只付它那一档的成本。

这是一个漂亮的**按场景内容特化工作量**的例子。大部分像素落在连续区域，复杂 shader 只跑在少数边缘像素上。

## 在 ROTR 中的应用场合

同一套 stencil 结构在多处被复用：

- 半分辨率 ambient lighting 的重建
- 半分辨率 particle 的重建（大量 overdraw 粒子都在半分辨率渲染）
- 半分辨率 motion blur 的重建

一次 stencil 分类、多处享受——典型的「基础设施一次投资，上层多处受益」的工程组织。

## 相关

- [[stencil-buffer]]
- [[early-z-late-z]]
- [[z-buffer]]
- [[hbao-interleaved-sampling]]
- [[image-resampling-filters]]
- [[rendering-pipeline-taxonomy]] — upsampling 是所有低分辨率效果管线的基础设施

## Sources

- [[sources/elopezr-rotr-rendering]]
- [[sources/bartwronski-ssr-gdc-followup]] — 反射率（gloss × Fresnel）权重上采样作为深度权重的替代
- [[sources/c0de517e-low-res-upsampling]] — Pesce 2016：COD:BO3 的 bilateral→nearest-depth 切换方案 + 棋盘格 min/max 降采样
