---
tags: [source, 渲染, 光谱渲染, 颜色]
date: 2026-04-14
sources: 1
---

# Spectral rendering, part 1: Spectra（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2025 年 11 月发表的**光谱渲染三部曲**的第一篇，为后续 Part 2（实时渲染）和 Part 3（结果对比）奠定数据侧的基础——光谱从哪来、怎么存、怎么让它能嫁接到 sRGB 美术管线上。

## 摘要

RGB 渲染本质上是一种粗糙的近似：它假装光源只在三个特定波长（红/绿/蓝）处发射能量，这显然和真实光源——日光平滑谱、荧光灯尖峰、钠灯单色线——不符。很多「颜色看起来不对」的问题被艺术家用 color grading 蒙过去了。光谱渲染的目标是直接在波长域做积分，解耦「人眼感知」和「光传输物理」。本篇解决两件事：**发射光谱**从哪来（光谱仪、欧盟能效标签数据库、LSPDD 公开库，存储成本完全可忽略）；**反射率光谱**——这是真正的瓶颈，每纹素一条谱会把 4K 纹理集膨胀到几百 GB，不现实。Peters 给出的解法是 **Fourier sRGB**：对每张 sRGB 纹理做一次离线 3D LUT 预处理，把它转成一套「三通道、BC1 可压、硬件采样兼容」的新 texture，但在运行时可以用三次 `arctan` 加几条线性组合出一条平滑的反射率谱，满足能量守恒（$a(\lambda) \in [0, 1]$），精确还原原 sRGB 颜色，形状类似真实测量谱。

## 关键要点

- **像素颜色 = 对整个可见光谱积分**，被积函数是「色匹配函数 × 光源谱 × 各次反射谱」连乘。
- **RGB 渲染 = 假设光源是三条单色 delta** 的极端退化。
- **发射光谱数据**轻松获得：LSPDD 有 300+ 条测量谱；欧盟强制公开的能效标签里都有谱图。500 条谱总共不到 1 MB。
- **反射率光谱**必须用上采样方案解决，否则显存爆炸。
- **Fourier sRGB**（[[fourier-srgb-spectral-upsampling]]）是 Peters SIGGRAPH 2019 论文的「可读版」：离线 $256^3$ LUT，运行时用 Lagrange 乘子 + arctan 重建平滑谱。
- **为什么不直接存 Lagrange 乘子**：数值范围极大，必须 FP16 + 不支持 BC1，硬件不友好；而且双线性过滤语义崩。Fourier sRGB 的胜利在于「看起来像 sRGB，所以所有硬件路径都复用」。

## 链接到的概念

- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[color-space]]
- [[color-lut]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/SpectralRendering1Spectra.html
- 本地：`raw/articles/momentsingraphics.de/2025-11-06_spectral-rendering-part-1-spectra.md`
