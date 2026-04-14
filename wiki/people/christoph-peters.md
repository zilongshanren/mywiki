---
tags: [人物, 作者, 渲染, 光谱渲染, 数学]
date: 2026-04-14
sources: 3
---

# Christoph Peters

**Christoph Peters** 是德国图形学研究者，博客 [momentsingraphics.de](http://momentsingraphics.de/) 写的是「把漂亮的数学工具稳稳塞进实时渲染器」这类题目。他的研究主线是**用矩（moments）和傅里叶系数来压缩带界信号**——阴影、光谱、体积——从而用极少的系数就能在 GPU 上高效重建。

## 风格

- **数学驱动 + 工程意识**：他的论文通常从一个古典数学问题（矩问题、最大熵谱估计、Lagrange 乘子）出发，但每篇都会交代「为什么 GPU 可以跑」、「寄存器够不够」、「带宽代价几何」。
- **每个博客配可玩的 Shadertoy / 代码仓**：读者可以直接点开看反射谱长什么样，或者拉一个 path tracer 跑起来。
- **和 Siggraph / i3D / EGSR 接轨**：博客里的长文几乎都对应一篇学术论文，博客是论文的「走心版」——没有审稿人限制的充分解释。
- **关心稳定性和性能边界**：特别爱讨论 [[register-spilling-avoidance|寄存器溢出]]、numerical stability、误差边界证明。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Spectral rendering, part 1: Spectra | [[spectral-rendering]]、[[fourier-srgb-spectral-upsampling]] |
| Spectral rendering, part 2: Real-time rendering | [[hero-wavelength-spectral-sampling]]、[[spectral-brdf]] |
| Finding Real Polynomial Roots on GPUs | [[polynomial-root-finding-gpu]]、[[register-spilling-avoidance]] |
| Sampling Projected Spherical Caps in Real Time | [[projected-solid-angle-sampling]] |

## 相关

- [[spectral-rendering]]
- [[color-space]]
- [[polynomial-root-finding-gpu]]
- [[projected-solid-angle-sampling]]

## Sources

- [[sources/peters-spectral-rendering-1-spectra]]
- [[sources/peters-spectral-rendering-2-real-time]]
- [[sources/peters-gpu-polynomial-roots]]
- [[sources/peters-projected-spherical-caps]]
