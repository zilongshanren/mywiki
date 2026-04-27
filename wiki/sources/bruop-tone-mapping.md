---
tags: [source, rendering, hdr, tone-mapping, post-processing]
date: 2026-04-27
sources: 1
---

# Tone Mapping（bruop.github.io）

[[bruno-opsenica|Bruno Opsenica]] 2019 年 4 月的文章，是其 [[luminance-histogram-exposure|自动曝光]] 系列的第二篇，专门讲解将曝光调整后的 HDR 值映射到 [0, 1] 的各种 [[tone-mapping|色调曲线]]。

## 摘要

文章定义色调映射算子（tone operator）的三个组成部分：shoulder（让高光趋近 1）、foot（控制低光表现）、线性段（保持中间调）。从 Reinhard 两种变体入手：简单版 `L_d = L/(1+L)` 和引入白点 `L_white` 的改良版。代码示例在 BGFX fragment shader 中先转换到 CIE xyY 空间，仅对亮度 Y 做曝光缩放，再应用曲线，再变换回 RGB，最后 gamma 变换写 backbuffer。进一步对比电影曲线：ACES（Narkowicz 近似）、UE4 的 ACES 变体、Hajime Uchimura 的 Gran Turismo 曲线、Timothy Lottes 曲线——电影曲线的"感"比 Reinhard 更有层次。作者还实验了逐亮度 vs 逐通道应用，认为逐通道（John Hable 的主张）效果更好，因为高光处会自然饱和变白，而逐亮度保色相但高光出现异常蓝色残留。最后提及局部色调映射（参考 Wronski 博文）、pre-exposure 以及 HDR 显示支持作为进阶方向。

## 关键要点

- 色调曲线三要素：shoulder / linear section / foot
- Reinhard 改良版加白点参数，控制何时输出达到 1.0
- 电影曲线（ACES / GT / Lottes）比 Reinhard 更少"洗白"高光
- 逐亮度应用保色相但在极端高光出现颜色残留；逐通道应用允许高光自然变白
- gamma 变换（`toGamma`）是色调映射流程的最后一步，不可省略
- 本文特意把全局色调映射与 [[local-tonemapping]] 区分开来，指出全局方案在大动态范围场景的局限

## 链接到的概念

- [[tone-mapping]]
- [[luminance-histogram-exposure]]
- [[local-tonemapping]]
- [[color-space]]

## 原文

- 链接：https://bruop.github.io/tonemapping/
- 本地：`raw/articles/bruop.github.io/2019-04-19_tone-mapping.md`
